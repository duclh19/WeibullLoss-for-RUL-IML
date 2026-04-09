# Thư mục `notebooks`

### 1. Mục đích chính
Thư mục chứa các file Jupyter Notebook (`.ipynb`). Đây là không gian tương tác (interactive workspace) được dùng để khám phá dữ liệu ban đầu, thử nghiệm thuật toán và trình bày trực quan luồng suy nghĩ của tác giả.

### 2. Cấu trúc và Các file bên trong
- **`1.0_IMS_explore.ipynb` & `1.0_PRONOSTIA_explore.ipynb`**: Notebook tập trung vào việc đọc dữ liệu thô từ 2 dataset là IMS và FEMTO (PRONOSTIA), phân tích tính chất vật lý của tín hiệu rung động.
- **`1.0_best_results_ims_2021.04.05.ipynb` & `1.0_best_results_femto_2021.04.07.ipynb`**: Các notebook tổng hợp lại những kết quả tốt nhất. Nơi này biểu diễn so sánh loss function truyền thống và Knowledge-informed loss.
- **`example.ipynb`**: Một notebook hướng dẫn (tutorial) từng bước cơ bản.
- **`scratch/`**: Thư mục chứa các file nháp (scratchpads). Tác giả thường code dạo các cell nháp ở đây để check bug hoặc test hàm nhanh trước khi đưa chúng vào mã nguồn chuẩn (`src`).

### 3. Thông tin quan trọng
- Những notebooks này là chìa khóa dễ nhất để hiểu dự án. Bạn nên bắt đầu bằng việc đọc `example.ipynb` hoặc các file `explore.ipynb` thay vì nhảy ngay vào file `.py`. Nó chứa đồ thị, markdown và text giải thích cụ thể cho từng khối lệnh.

### 4. Điểm cần lưu ý
- Thứ tự chạy Notebook thường được đặt tên theo quy ước (vd `1.0_...`). Tuy nhiên, để chạy được notebook, cần có bộ dữ liệu thô (raw data) nằm trong `data/raw`. Nếu không, các cell báo lỗi `FileNotFoundError`.
- Các file trong `scratch` không được cam kết về chất lượng code, có thể bị đứt gãy.
