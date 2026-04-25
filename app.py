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

from src.data.data_utils import load_train_test_femto
from src.models.utils import test
from sklearn.metrics import r2_score, mean_squared_error

st.set_page_config(page_title="RUL Prediction (FEMTO Dataset)", layout="wide")
st.title("⚙️ Remaining Useful Life (RUL) Prediction - FEMTO Dataset")
# st.markdown("Compare bearing life predictions using **Knowledge-Informed Loss (Weibull)** vs. **Traditional Math (MSE/RMSE)**.")

@st.cache_data
def load_data(split_name):
    folder_data = root_dir / "data/processed/FEMTO"
    
    (
        x_train, y_train, x_val, y_val, x_test, y_test,
        x_train1_1, y_train1_1, x_train2_1, y_train2_1, x_train3_1, y_train3_1,
        x_val1_2, y_val1_2, x_val2_2, y_val2_2, x_val3_2, y_val3_2,
        x_test1_3, y_test1_3, x_test2_3, y_test2_3, x_test3_3, y_test3_3,
    ) = load_train_test_femto(folder_data)
    
    mapping = {
        "Train (Bearing 1_1)": (x_train1_1, y_train1_1),
        "Train (Bearing 2_1)": (x_train2_1, y_train2_1),
        "Train (Bearing 3_1)": (x_train3_1, y_train3_1),
        "Validation (Bearing 1_2)": (x_val1_2, y_val1_2),
        "Validation (Bearing 2_2)": (x_val2_2, y_val2_2),
        "Validation (Bearing 3_2)": (x_val3_2, y_val3_2),
        "Test (Bearing 1_3)": (x_test1_3, y_test1_3),
        "Test (Bearing 2_3)": (x_test2_3, y_test2_3),
        "Test (Bearing 3_3)": (x_test3_3, y_test3_3),
    }
    
    x_target, y_target = mapping[split_name]
    
    y_days = y_target[:, 0].numpy()
    y_true = y_target[:, 1].numpy()
    x_data = x_target
    
    index_sorted = np.argsort(y_true)[::-1]
    
    return x_data, y_true[index_sorted], y_days[index_sorted], index_sorted

@st.cache_resource
def load_models():
    model_dir = root_dir / "iml/models/final/top_models_femto"
    
    target_models = [
        "2026_04_13_18:12:37_weibull_only_rmsle_4326813.pt",
        "2026_04_13_16:31:43_weibull_only_rmse_4326813.pt",
        "2026_04_14_04:16:34_weibull_only_rmsle_4326813.pt"
    ]
    
    models = {}
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    for f in target_models:
        model_path = model_dir / f
        if model_path.exists():
            try:
                net = torch.load(model_path, map_location=device, weights_only=False)
                net.eval()
                # Keep the full filename (with timestamp) to avoid duplicates
                models[f] = net
            except Exception as e:
                st.warning(f"Could not load {f}: {e}")
        else:
            st.warning(f"Model file not found: {f}")
                
    return models

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ System Configuration")
    
    split_options = [
        "Train (Bearing 1_1)", "Train (Bearing 2_1)", "Train (Bearing 3_1)",
        "Validation (Bearing 1_2)", "Validation (Bearing 2_2)", "Validation (Bearing 3_2)",
        "Test (Bearing 1_3)", "Test (Bearing 2_3)", "Test (Bearing 3_3)"
    ]
        
    data_split = st.selectbox("Select Bearing (Data Split)", split_options, index=6)
    
    st.info("Loading TOP 3 models...")
    available_models = load_models()
    
    if not available_models:
        st.error("No trained models found in iml/models/final/top_models_femto/")
        st.stop()
        
    model_names = list(available_models.keys())
    selected_models = st.multiselect("Select Models to Compare", model_names, default=model_names)
    
    st.markdown("---")
    st.subheader("Time Range Selection (Data Slice)")
    
    x_data, y_true, y_days, index_sorted = load_data(data_split)
    total_samples = len(y_true)
    
    sample_range = st.slider(
        "Select Sample Range (Chronological)", 
        0, total_samples, (0, total_samples),
        help="Slide to zoom into the final stages of the bearing's life"
    )
    
    run_btn = st.button("🚀 Run Inference", type="primary", use_container_width=True)

# --- Main Logic ---
if run_btn and selected_models:
    with st.spinner('Running inference system...'):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        start_idx, end_idx = sample_range
        
        y_true_slice = y_true[start_idx:end_idx]
        y_days_slice = y_days[start_idx:end_idx]
        
        x_indices_to_use = index_sorted[start_idx:end_idx]
        x_data_slice = x_data[x_indices_to_use.copy()].to(device)
        
        predictions = {}
        metrics = []
        
        for model_name in selected_models:
            net = available_models[model_name]
            
            with torch.no_grad():
                y_hats = test(net, x_data_slice, device, batch_size=100)
                predictions[model_name] = y_hats.numpy().squeeze()
                
            try:
                r2 = r2_score(y_true_slice, predictions[model_name])
                rmse = np.sqrt(mean_squared_error(y_true_slice, predictions[model_name]))
                metrics.append({"Model": model_name, "R² Score": r2, "RMSE": rmse})
            except Exception as e:
                st.warning(f"Could not calculate metrics for {model_name}")

        st.subheader(f"Prediction vs. Ground Truth on {data_split}")
        
        fig = go.Figure()
        
        x_axis = np.arange(len(y_true_slice))
        
        fig.add_trace(go.Scatter(
            x=x_axis, 
            y=y_true_slice * 100,
            mode='lines',
            name='Ground Truth (Actual Life)',
            line=dict(color='black', width=3, dash='dash')
        ))
        
        colors = ['#d73027', '#4575b4', '#fc8d59', '#fee090', 'green', 'purple', 'brown', 'pink', 'teal', 'cyan']
        for i, model_name in enumerate(selected_models):
            
            window_size = min(12, len(predictions[model_name]) // 10)
            if window_size > 0:
                y_smooth = np.convolve(predictions[model_name], np.ones(window_size)/window_size, mode='valid')
                x_smooth = x_axis[window_size-1:]
            else:
                y_smooth = predictions[model_name]
                x_smooth = x_axis
                
            fig.add_trace(go.Scatter(
                x=x_smooth, 
                y=y_smooth * 100,
                mode='lines',
                name=f'{model_name} (Smoothed)',
                line=dict(color=colors[i % len(colors)], width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=x_axis,
                y=predictions[model_name] * 100,
                mode='markers',
                name=f'{model_name} (Raw)',
                marker=dict(color=colors[i % len(colors)], size=2),
                opacity=0.15,
                showlegend=False
            ))
            
        fig.update_layout(
            xaxis_title="Life Cycle (Data Points -> Failure)",
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
        
        st.subheader("Performance Metrics")
        if metrics:
            metrics_df = pd.DataFrame(metrics)
            st.dataframe(
                metrics_df.style.highlight_max(subset=['R² Score'], color='lightgreen')
                              .highlight_min(subset=['RMSE'], color='lightgreen'),
                use_container_width=True
            )
            
elif not selected_models:
    st.info("Please select at least 1 model from the sidebar to begin.")
else:
    st.info("Click **🚀 Run Inference** on the left to see predictions.")
