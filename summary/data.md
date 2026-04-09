# Thư mục `data`

### 1. Mục đích chính
Thư mục này là nơi lưu trữ toàn bộ dữ liệu của dự án, từ dữ liệu thô tải về từ các nguồn mở (NASA Prognostic Data Repository) cho tới dữ liệu đã qua tiền xử lý, sẵn sàng để nạp vào mô hình học máy. 

### 2. Cấu trúc và Các file/thư mục bên trong
- **`data/raw/`**: Chứa dữ liệu gốc, nguyên bản và không bao giờ được phép thay đổi (immutable). Dữ liệu này thường bao gồm các tín hiệu cảm biến rung động (vibration) của vòng bi từ hai bộ dữ liệu IMS (Intelligent Maintenance Systems) và FEMTO (PRONOSTIA).
- **`data/interim/`**: Nơi lưu tạm các file trung gian sinh ra trong quá trình biến đổi, ví dụ như cắt ghép time-series hoặc dữ liệu đã qua một bước làm sạch nhưng chưa hoàn chỉnh.
- **`data/processed/`**: Thư mục này hiện tại chứa dữ liệu đã được làm sạch và chuẩn hóa cuối cùng. Dữ liệu trong này thường được định dạng thành các ma trận tần số (đã qua thuật toán Fast Fourier Transform - FFT) hoặc phổ tần (Spectrogram), giúp mô hình ML dễ dàng trích xuất thông tin.

### 3. Thông tin quan trọng
- Dữ liệu ở đây là Time-Series dữ liệu từ vòng bi (bearings) bị mài mòn cho đến lúc hỏng hóc (Run-to-Failure).
- RUL (Remaining Useful Life) là biến mục tiêu cần dự đoán, được gán mác dựa trên số ngày hoặc thời gian (timestamps) còn lại cho đến khi máy móc dừng hoạt động.

### 4. Điểm cần lưu ý
- Nếu chạy dự án từ đầu, thư mục `raw` sẽ trống. Bạn phải sử dụng lệnh `make download` hoặc script `src/data/download_data_local.sh` để tải dữ liệu về.
- Kích thước dữ liệu gốc có thể khá lớn, vì vậy các file `.gitignore` thường bỏ qua các file trong thư mục này để tránh đẩy dữ liệu nặng lên Github.
