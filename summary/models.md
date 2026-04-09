# Thư mục `models`

### 1. Mục đích chính
Thư mục lưu trữ tĩnh cho các trọng số mạng Nơ-ron (weights/checkpoints) và các file kết quả dự đoán của mô hình sau/trong quá trình train.

### 2. Cấu trúc và Các file bên trong
- **`models/interim/`**: Nơi lưu các mô hình tạm thời trong quá trình tối ưu siêu tham số (Hyperparameter tuning / Random search). Tại đây có thể chứa hàng chục đến hàng trăm biến thể kiến trúc bị vứt bỏ sau khi so sánh.
- **`models/final/`**: Chứa các checkpoint của mô hình tốt nhất hoặc mô hình đã được xác nhận (bằng đuôi `.pt` cho PyTorch). Đi kèm là các file báo cáo dạng `.csv` lưu trữ logs tổng kết (ví dụ sai số RMSE, MAPE, các tham số loss function Weibull).

### 3. Thông tin quan trọng
- Những models ở đây được dùng trực tiếp bởi các script trong `src/models/summarize_model_results.py` hoặc module `visualization/` để tải lên (load state_dict) mà không cần phải chạy đào tạo (train) lại từ đầu tốn thời gian.

### 4. Điểm cần lưu ý
- Nếu bạn kéo (git clone) repo này, các file mô hình có thể không được đính kèm (bị ignore bởi `.gitignore`) do dung lượng lớn. Bạn cần tự chạy `make train_ims` hoặc `make train_femto` để sinh ra các file kết quả trong thư mục này.
