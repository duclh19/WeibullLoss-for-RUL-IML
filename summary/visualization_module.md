# Phân tích Module Trực quan hóa (Visualization Module)

### 1. Mục đích chính
Thư mục `src/visualization/` (với 3 file `.py` lớn) là hệ thống vẽ báo cáo và phân tích đồ thị tự động của toàn bộ pipeline từ lúc đưa dữ liệu vào đến kết quả train ra. Được dùng nhiều nhất bởi các Notebook.

### 2. Cấu trúc và Các file bên trong

#### A. `visualize_data.py` (Trực quan hóa Dữ liệu thô)
- **Hàm `create_time_frequency_plot` & `plot_freq_peaks`**: Vẽ tín hiệu rung động (vibration) trên 2 miền: Miền thời gian (để xem biên độ giật lắc) và Miền tần số (Phổ tần số - xem tần số nào đang cộng hưởng - ứng dụng FFT).
- **Hàm `plot_weibull_example`**: Trực quan hóa Hàm phân phối Weibull (PDF và CDF).
  - *Main point*: Giúp người đọc báo cáo hiểu về hình dáng của hàm phân phối sống còn (thường được dùng để dự báo hư hỏng máy móc) trước khi đưa nó vào làm Loss Function.
- **Hàm `ims_data_processed_fig` & `femto_data_processed_fig`**: Vẽ tổng quan các file tín hiệu sau khi đã làm mịn để cho thấy rõ xu hướng từ bình thường -> trước khi hỏng -> hỏng hóc.

#### B. `visualize_results.py` (Trực quan hóa Đánh giá Hiệu năng)
- **Hàm `loss_function_percentage_fig`**: So sánh giữa Knowledge-Informed Loss (Weibull) với Standard Loss (RMSE thông thường). Đồ thị dạng Bar-chart (Cột) hiển thị *tỉ lệ % cải thiện*.
- **Hàm `early_stop_distribution_fig`**: Vẽ Histogram phân bố số epoch tại điểm mà mô hình dừng học (Early Stopping) nhằm đánh giá xem Knowledge-Informed Loss có giúp mạng hội tụ nhanh và ổn định hơn không.
- **Hàm `ims_results_rul_fig` & `femto_results_rul_fig`**: Vẽ biểu đồ đường (Line plot). Trục X là thời gian, Trục Y là tuổi thọ còn lại (RUL). Nó plot đường "Ground Truth" (giảm dần bậc thang / tuyến tính) cắt với đường "Dự đoán" của Model. Từ đó thấy được Model bám sát thực tế thế nào.
- **Hàm `calc_r2_avg`**: Đo độ đo $R^2$ làm mịn theo cửa sổ thời gian (window size). 

#### C. `visualize_training.py` (Trình bày chi tiết Quá trình Training)
- **Hàm `plot_trained_model_results_ims` & `plot_trained_model_results_femto`**: Hàm gộp chung. Khi chạy sẽ văng ra một "Dashboard" toàn diện bao gồm:
  1. Learning Curve (Train Loss vs Val Loss qua các Epochs).
  2. RUL dự báo cho một loạt các mẫu thử nghiệm khác nhau.

### 3. Thông tin quan trọng
- Tác giả sử dụng `matplotlib.pyplot` và `seaborn` là 2 thư viện lõi. Code khá dài do các thiết lập format chuẩn báo cáo khoa học (font chữ, cỡ chữ, DPI, nhãn trục LaTeX...).

### 4. Điểm cần lưu ý
- Để gọi các file script này từ CLI (Command Line), bạn có thể gõ lệnh `make figures_data` hoặc `make figures_results`. Đồ thị sẽ tự động được sinh ra và ghi vào thư mục `reports/figures/` dưới định dạng chuẩn bài báo (PDF/PNG). 
