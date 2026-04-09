# Thư mục `src` (Mã nguồn Lõi)

### 1. Mục đích chính
Đây là trái tim của hệ thống máy học. Toàn bộ logic ETL (Trích xuất, Biến đổi, Nạp dữ liệu), định nghĩa thuật toán, kiến trúc Neural Network (PyTorch), và các script chạy tự động hóa đều nằm tại đây. Mã được cấu trúc dưới dạng một module Python (có thể được import bằng `import src`).

### 2. Cấu trúc và Chi tiết Từng Phân hệ
#### A. `src/data/` (Quản lý Dữ liệu)
- **`dataset_ims.py` & `dataset_femto.py`**: Định nghĩa logic kết nối, parsing cấu trúc file csv/txt thô rườm rà của IMS/FEMTO thành các DataFrame pandas dễ xử lý.
- **`make_dataset.py`**: Script thực thi chính. Chạy để tạo các bộ dữ liệu `processed/` (phân chia train/val/test).
- **`download_data_*` / `extract_data_*`**: Các bash script (`.sh`) và python script giúp crawl tự động dữ liệu từ internet (local và HPC - High Performance Computing clusters).

#### B. `src/features/` (Khai phá Đặc trưng - Feature Engineering)
- **`build_features.py`**: Chứa logic xử lý tín hiệu (Signal Processing). Hàm quan trọng: `create_fft` dùng biến đổi Fast Fourier Transform, và các hàm xây dựng phổ đồ (Spectrogram) biến tín hiệu chuỗi thời gian 1 chiều (1D time-series) thành dữ liệu ảnh (2D) thể hiện mức năng lượng theo thời gian và tần số, giúp Mạng nơ-ron dễ bắt được dấu hiệu bất thường.

#### C. `src/models/` (Huấn luyện & Suy luận Mô hình)
- **`model.py`**: Chứa định nghĩa lớp `Net(nn.Module)`. Đây là một kiến trúc Đa Tầng Perceptron (Multilayer Perceptron - MLP) đơn giản gồm các lớp Fully Connected (`nn.Linear`), Dropout, kích hoạt ReLU, và đầu ra dùng Sigmoid để dự báo RUL nằm trong khoảng 0-1.
- **`loss.py`**: **Phần quan trọng nhất của bài báo!** Tại đây tác giả định nghĩa "Knowledge-Informed Loss". Bên cạnh RMSE hay MAPE thuần túy, tác giả tạo ra hàm loss dựa trên phân phối Weibull (`WeibullLossRMSE`, `WeibullLossRMSLE`, `WeibullLossMSE`). Cụ thể, nó tính toán độ chênh lệch CDF của phân phối Weibull giữa Nhãn thực (`y_days`) và Dự đoán (`y_hat_days`). Điều này ép mô hình tuân thủ theo tính chất vật lý của chu kỳ sống vòng bi.
- **`train_models.py`**: Mã chính vòng lặp huấn luyện (train loop, validation, early stopping).
- **`summarize_model_results.py`**: Script phân tích và lưu file kết quả.

#### D. `src/visualization/` (Đồ thị & Báo cáo)
- Chứa `visualize_data.py`, `visualize_results.py`, `visualize_training.py` dùng để trích xuất các thông tin số liệu khô khan thành biểu đồ cho báo cáo.

### 3. Thông tin quan trọng (Main point)
- **Kiến trúc ML:** Đây là mô hình PyTorch (Deep Learning). Kiến trúc không quá cầu kỳ (chỉ là MLP) nhưng trọng tâm nằm ở **Loss Function có chứa tri thức miền (Knowledge-Informed)**.
- Bài toán giải quyết là **Regression** (Dự đoán số liên tục - Thời gian sử dụng RUL).

### 4. Điểm cần lưu ý
- Khi chạy train trên máy Local (Mac/Windows), chú ý các file cấu trúc `.sh` có ghi chú rõ `_hpc` là dành cho Cluster (như Compute Canada dùng slurm), và `_local` là dành cho máy cá nhân. Hãy dùng đúng file script.
