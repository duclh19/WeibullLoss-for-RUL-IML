# Giải đáp về Loss Function và Kết quả huấn luyện

**Câu hỏi:** Vậy bài toán này có thể train dựa trên 3 loss hả? tức là kết hợp weibullLoss và RMSE/RMSLE/MSE? có thể chạy để so sánh với các loss không kết hợp với weibullLoss không? bài toán đã chạy chưa, đã so sánh kết quả chưa?

**Trả lời:**
Đúng như bạn phân tích! Câu trả lời cho cả 3 câu hỏi của bạn đều là **CÓ**. Chi tiết như sau:

### 1. Có thể train kết hợp WeibullLoss và RMSE/RMSLE/MSE không?
**Có.** Tác giả thiết kế mã nguồn cho phép mạng Nơ-ron tối ưu hóa cùng lúc cả sai số thời gian (Time-domain error) và sai số dựa trên tính chất vật lý vòng bi (Knowledge-informed error).
Trong file `src/models/train_models.py`, việc tính tổng Loss được định nghĩa rất rõ ràng (kết hợp theo phép cộng tuyến tính). Các tùy chọn bao gồm:
- `weibull_rmse` = `RMSELoss(y_hat, y)` + `WeibullLossRMSE(y_hat, y, y_days, ...)`
- `weibull_rmsle` = `RMSLELoss(y_hat, y)` + `WeibullLossRMSLE(...)`
- `weibull_mse` = `MSELoss(y_hat, y)` + `WeibullLossMSE(...)`

### 2. Có thể so sánh với các Loss KHÔNG kết hợp WeibullLoss không?
**Hoàn toàn có thể.** Không những có thể, mà tác giả đã viết sẵn một vòng lặp (loop) tự động chạy qua toàn bộ **9 loại Loss Function** khác nhau để đảm bảo sự so sánh là công bằng nhất. Cụ thể, vòng lặp trong `train_models.py` sẽ train liên tục mô hình với danh sách các Loss sau:
* **Nhóm cơ bản (Không Weibull)**: `"mse"`, `"rmse"`, `"rmsle"`
* **Nhóm lai (Kết hợp Weibull)**: `"weibull_mse"`, `"weibull_rmse"`, `"weibull_rmsle"`
* **Nhóm chỉ dùng Tri thức miền (Chỉ có Weibull)**: `"weibull_only_mse"`, `"weibull_only_rmse"`, `"weibull_only_rmsle"`

Điều này cho phép đánh giá xem việc thêm kiến thức vật lý (`weibull`) vào làm tăng hay giảm hiệu năng so với việc chỉ dùng toán học thuần túy.

### 3. Bài toán đã chạy chưa, và đã có kết quả so sánh chưa?
**Bài toán đã được chạy hoàn chỉnh và kết quả đã được lưu trữ sẵn.**
Trong thư mục `models/final/` đang chứa sẵn các file tổng hợp kết quả (lên tới hàng triệu thông số, định dạng `.csv` và `.csv.gz`), bao gồm:
1. `ims_results_filtered.csv` và `femto_results_filtered.csv`: Kết quả sau khi đã lọc qua hàng ngàn Iterations.
2. `ims_correlation_results.csv` & `femto_correlation_results.csv`: Sự tương quan giữa các loss.
3. `ims_count_results.csv` & `femto_count_results.csv`: Đếm số lần nhóm "Weibull Loss" đánh bại nhóm "Loss thông thường".

**Nơi xem kết quả so sánh:**
Tác giả đã trực quan hóa sẵn các kết quả so sánh này trong 2 file Notebook:
- `notebooks/1.0_best_results_ims_2021.04.05.ipynb`
- `notebooks/1.0_best_results_femto_2021.04.07.ipynb`
