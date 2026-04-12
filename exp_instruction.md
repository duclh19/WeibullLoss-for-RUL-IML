# Hướng dẫn Cài đặt, Chạy thử nghiệm nghiệm và Sử dụng Demo (Experiment Instruction)

Tài liệu này hướng dẫn chi tiết từng bước để bạn có thể thiết lập dự án dự đoán Tuổi thọ còn lại (Remaining Useful Life - RUL) với phương pháp Knowledge-Informed Machine Learning (Weibull Loss), chạy thử nghiệm mô hình, đánh giá kết quả và khởi chạy giao diện Web Demo.

---

## 1. Thiết lập Môi trường với `uv` (Package Manager)

Dự án này sử dụng `uv` - một trình quản lý package cực kỳ nhanh và mạnh mẽ bằng Rust, giúp việc cài đặt các thư viện Python (như PyTorch, Pandas, Streamlit) trở nên dễ dàng và hạn chế xung đột.

### Bước 1.1: Cài đặt `uv` (nếu chưa có)
MacOS hoặc Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Bước 1.2: Tạo môi trường ảo (Virtual Environment)
Dự án yêu cầu Python 3.8+ (khuyến nghị 3.8 để đảm bảo tính tương thích của thư viện cũ). Chạy lệnh sau tại thư mục gốc của dự án:
```bash
uv venv --python 3.8
```

### Bước 1.3: Kích hoạt và Cài đặt thư viện
Kích hoạt môi trường ảo:
- Trên macOS/Linux: `source .venv/bin/activate`
- Trên Windows: `.venv\Scripts\activate`

Tiến hành cài đặt toàn bộ dependencies và package nội bộ `src` bằng lệnh:
```bash
uv pip install -e .
uv pip install streamlit plotly  # Cài đặt thêm các thư viện cho Web UI
```
*(File `pyproject.toml` đã được cấu hình sẵn để cài đặt tự động).*

---

## 2. Chuẩn bị Dữ liệu (Data Preparation)
(Hiện tại đang sử dụng processed data luôn)
Dự án hỗ trợ 2 tập dữ liệu là IMS và FEMTO (PRONOSTIA). Bạn có 2 lựa chọn:

- **Cách 1 (Nhanh nhất): Dùng dữ liệu đã xử lý sẵn.**
  Khi bạn clone repository này, tác giả đã cung cấp sẵn các file dữ liệu dạng `.hdf5` cực nhẹ (đã qua bước tiền xử lý Fast Fourier Transform) bên trong thư mục `data/processed/IMS` và `data/processed/FEMTO`. Bạn **không cần làm gì thêm** và có thể nhảy ngay sang Bước 3!

- **Cách 2 (Làm từ đầu): Tải và xử lý dữ liệu thô.**
  Nếu bạn muốn tự mình trích xuất đặc trưng từ dữ liệu gốc (RAW data hàng GB):
  ```bash
  make download    # Tải file nén từ nguồn NASA về data/raw
  make extract     # Giải nén các thư mục
  make data        # Chạy tiền xử lý và chuyển đổi sang data/processed
  ```

---

## 3. Chạy Thử nghiệm Huấn luyện Mô hình (Training)

Mã nguồn được thiết kế tự động tìm kiếm siêu tham số (Random Search Hyperparameter Tuning). Nó sẽ tạo ra ngẫu nhiên hàng ngàn kiến trúc mạng khác nhau (Layer, Dropout, Learning Rate,...) và train chúng qua 9 hàm Loss (MSE, RMSE, Weibull...).

### Bước 3.1: Bắt đầu Huấn luyện (Đãi cát tìm vàng)
Chạy lệnh sau để train trên tập IMS:
```bash
python src/models/train_models.py --data_set ims --path_data data/processed --proj_dir .
```
*(Thay `ims` bằng `femto` nếu muốn train tập PRONOSTIA).*

**Lưu ý quan trọng:** Mặc định, vòng lặp này sẽ chạy 3000 kiến trúc mạng khác nhau (mất nhiều ngày). Nếu bạn chỉ muốn **chạy thử nhanh (test run)**, hãy thêm tham số:
```bash
python src/models/train_models.py --data_set ims --path_data data/processed --proj_dir . --random_search_iter 2
```
Tất cả các file weights mô hình `.pt`, đồ thị `Learning Curve`, và "Bảng điểm nháp" `.csv` sẽ được ném vào thư mục: `models/interim/`. **(Chưa có Final Model nào ở bước này!)**

---

## 4. Đánh giá và Chọn ra "Best Model" (Summary)

Sau khi train xong (hoặc bạn tự ngắt ngang tiến trình), bạn phải gọi "Ban Giám Khảo" để đánh giá các mô hình nháp, loại bỏ các mô hình bị Overfit/Underfit và vinh danh những người chiến thắng.

### Bước 4.1: Chạy Script Tổng hợp
```bash
python src/models/summarize_model_results.py --data_set ims
```
*(Hoặc dùng lệnh ngắn gọn: `make summarize_ims_models`)*

### Bước 4.2: Kiểm tra kết quả
Script trên sẽ tự động:
1. Lọc và xếp hạng (Sort) điểm $R^2$ của các mô hình trên tập Test.
2. Copy 2 file `.pt` của mô hình Top 1 và Top 2 vào thư mục VIP:
   👉 `models/final/top_models_ims/`
3. Xuất bảng xếp hạng vĩnh viễn lưu tại:
   👉 `models/final/ims_results_filtered.csv`

**Làm sao để biết cấu hình của Best Model?**
Mở file `ims_results_filtered.csv` vừa được tạo ra. **Dòng đầu tiên (Row 1)** của file này chứa toàn bộ thông số của mô hình xuất sắc nhất:
- `loss_func` (Hàm loss), `n_layers` (Số layer ẩn), `n_units` (Số nơ-ron), `learning_rate` (Tốc độ học), `prob_drop` (Dropout), và tên file `.pt` tương ứng.

---

## 5. Sử dụng Ứng dụng Demo (Streamlit Web UI)

Sau khi đã có "Best Models" nằm trong thư mục `final`, bạn có thể khởi chạy giao diện Web để tương tác và trực quan hóa kết quả dự đoán của các mô hình.

### Bước 5.1: Khởi chạy App
Tại thư mục gốc, chạy lệnh:
```bash
streamlit run app.py
```

### Bước 5.2: Tương tác với Demo
1. Giao diện web sẽ tự động quét thư mục `models/final/top_models_[ims/femto]`.
2. Tại cột Sidebar bên trái, chọn **Dataset** bạn vừa train.
3. Chọn các Mô hình / Hàm Loss (VD: `weibull_rmse`, `mse`) mà bạn muốn đưa ra thi đấu.
4. Kéo thanh trượt (Slider) để chọn dải thời gian của dữ liệu Validation (từ lúc bình thường đến khi hỏng hóc).
5. Bấm nút **🚀 Run Inference**.

Ứng dụng sẽ nạp file `.pt` của các mô hình vào PyTorch, đưa dữ liệu vào dự đoán và hiển thị biểu đồ đường (Line Chart) so sánh trực quan giữa RUL thực tế (Ground Truth) và RUL do các mô hình dự đoán. Các chỉ số $R^2$ và $RMSE$ cũng sẽ hiển thị ở bảng bên dưới!
