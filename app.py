import streamlit as st
import pandas as pd
import numpy as np
import torch
import plotly.graph_objects as go
from pathlib import Path
import os
import sys

# Add root directory to python path
root_dir = Path(__file__).resolve().parent
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / "src" / "models"))

from src.data.data_utils import load_train_test_ims, load_train_test_femto
from src.models.utils import test
from sklearn.metrics import r2_score, mean_squared_error

st.set_page_config(page_title="RUL Prediction Visualization", layout="wide")
st.title("⚙️ Remaining Useful Life (RUL) Prediction")
st.markdown("Compare predictions from models trained with traditional losses vs. knowledge-informed (Weibull) losses.")

@st.cache_data
def load_data(dataset_type):
    folder_data = root_dir / f"data/processed/{dataset_type.upper()}"
    
    if dataset_type == "ims":
        (
            x_train, y_train, x_val, y_val, x_test, y_test,
            x_train_2, y_train_2, x_train_3, y_train_3
        ) = load_train_test_ims(folder_data)
        
        # We will use the validation set for visualization
        y_days = y_val[:, 0].numpy()
        y_true = y_val[:, 1].numpy()
        x_data = x_val
        
    else:  # femto
        (
            x_train, y_train, x_val, y_val, x_test, y_test,
            x_train1_1, y_train1_1, x_train2_1, y_train2_1, x_train3_1, y_train3_1,
            x_val1_2, y_val1_2, x_val2_2, y_val2_2, x_val3_2, y_val3_2,
            x_test1_3, y_test1_3, x_test2_3, y_test2_3, x_test3_3, y_test3_3,
        ) = load_train_test_femto(folder_data)
        
        # We will use the validation set for visualization
        y_days = y_val[:, 0].numpy()
        y_true = y_val[:, 1].numpy()
        x_data = x_val
        
    # Sort data chronologically based on y_true (remaining life goes down)
    index_sorted = np.argsort(y_true)[::-1]
    
    return x_data, y_true[index_sorted], y_days[index_sorted], index_sorted

@st.cache_resource
def load_models(dataset_type):
    model_dir = root_dir / f"models/final/top_models_{dataset_type.lower()}"
    
    if not model_dir.exists():
        return {}
        
    model_files = [f for f in os.listdir(model_dir) if f.endswith('.pt')]
    models = {}
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    for f in model_files:
        # Extract loss name from filename (e.g. 2021_04_05_17:06:26_weibull_rmse_3405377.pt)
        parts = f.split('_')
        if len(parts) >= 6:
            if 'only' in parts:
                loss_name = f"{parts[4]}_{parts[5]}_{parts[6]}"
            else:
                loss_name = f"{parts[4]}_{parts[5]}"
            
            # Load model
            try:
                model_path = model_dir / f
                net = torch.load(model_path, map_location=device, weights_only=False)
                net.eval()
                models[loss_name] = net
            except Exception as e:
                st.warning(f"Could not load {f}: {e}")
                
    return models

# --- Sidebar ---
with st.sidebar:
    st.header("Configuration")
    
    dataset = st.selectbox("Select Dataset", ["ims", "femto"])
    
    st.info("Loading models...")
    available_models = load_models(dataset)
    
    if not available_models:
        st.error(f"No trained models found in models/final/top_models_{dataset}/")
        st.stop()
        
    model_names = list(available_models.keys())
    selected_models = st.multiselect("Select Models to Compare", model_names, default=model_names)
    
    st.markdown("---")
    st.subheader("Data Slice")
    
    # Need to load data to get its length
    x_data, y_true, y_days, index_sorted = load_data(dataset)
    total_samples = len(y_true)
    
    sample_range = st.slider(
        "Select Sample Range (Chronological)", 
        0, total_samples, (0, total_samples),
        help="0 is start of life, max is failure point"
    )
    
    run_btn = st.button("🚀 Run Inference", type="primary", use_container_width=True)

# --- Main Logic ---
if run_btn and selected_models:
    with st.spinner('Running inference...'):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Get data slice
        start_idx, end_idx = sample_range
        
        # Slice the already chronologically sorted target data
        y_true_slice = y_true[start_idx:end_idx]
        y_days_slice = y_days[start_idx:end_idx]
        
        # Slice the original X data using the sorted index
        x_indices_to_use = index_sorted[start_idx:end_idx]
        x_data_slice = x_data[x_indices_to_use].to(device)
        
        predictions = {}
        metrics = []
        
        # Run inference for each selected model
        for model_name in selected_models:
            net = available_models[model_name]
            
            # Use test utility from src.models.utils
            with torch.no_grad():
                y_hats = test(net, x_data_slice, device, batch_size=100)
                # Squeeze to 1D array
                predictions[model_name] = y_hats.numpy().squeeze()
                
            # Calculate metrics
            try:
                r2 = r2_score(y_true_slice, predictions[model_name])
                rmse = np.sqrt(mean_squared_error(y_true_slice, predictions[model_name]))
                metrics.append({"Model": model_name, "R² Score": r2, "RMSE": rmse})
            except Exception as e:
                st.warning(f"Could not calculate metrics for {model_name}")

        # --- Visualization ---
        st.subheader("Prediction vs Ground Truth")
        
        fig = go.Figure()
        
        # Plot Ground Truth
        # X-axis will just be sequential points in the sliced range to show progression
        x_axis = np.arange(len(y_true_slice))
        
        fig.add_trace(go.Scatter(
            x=x_axis, 
            y=y_true_slice * 100, # Convert to percentage
            mode='lines',
            name='Ground Truth (Actual Life)',
            line=dict(color='black', width=3, dash='dash')
        ))
        
        # Plot Predictions
        colors = ['#d73027', '#4575b4', '#fc8d59', '#fee090', 'green', 'purple']
        for i, model_name in enumerate(selected_models):
            
            # Apply rolling average to smooth predictions (window=12, roughly 2 mins/hours)
            window_size = min(12, len(predictions[model_name]) // 10)
            if window_size > 0:
                y_smooth = np.convolve(predictions[model_name], np.ones(window_size)/window_size, mode='valid')
                x_smooth = x_axis[window_size-1:]
            else:
                y_smooth = predictions[model_name]
                x_smooth = x_axis
                
            fig.add_trace(go.Scatter(
                x=x_smooth, 
                y=y_smooth * 100, # Convert to percentage
                mode='lines',
                name=f'{model_name} (Smoothed)',
                line=dict(color=colors[i % len(colors)], width=2)
            ))
            
            # Optional: Add raw scatter points (lightly)
            fig.add_trace(go.Scatter(
                x=x_axis,
                y=predictions[model_name] * 100,
                mode='markers',
                name=f'{model_name} (Raw)',
                marker=dict(color=colors[i % len(colors)], size=2),
                opacity=0.2,
                showlegend=False
            ))
            
        fig.update_layout(
            xaxis_title="Time Progression (Data Points -> Failure)",
            yaxis_title="Remaining Useful Life (%)",
            hovermode="x unified",
            height=600,
            template="plotly_white",
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # --- Metrics Table ---
        st.subheader("Performance Metrics")
        if metrics:
            metrics_df = pd.DataFrame(metrics)
            # Highlight max R2 and min RMSE
            st.dataframe(
                metrics_df.style.highlight_max(subset=['R² Score'], color='lightgreen')
                              .highlight_min(subset=['RMSE'], color='lightgreen'),
                use_container_width=True
            )
            
elif not selected_models:
    st.info("Please select at least one model from the sidebar to begin.")
else:
    st.info("Click **Run Inference** to generate predictions.")
