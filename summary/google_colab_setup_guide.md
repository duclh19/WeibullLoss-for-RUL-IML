# Hướng dẫn từng bước chạy thử nghiệm (Experiment) trên Google Colab

Dự án này rất phù hợp để chạy trên Google Colab vì Colab cung cấp sẵn môi trường Linux (Ubuntu), Python và GPU miễn phí. Dưới đây là các bước chi tiết bạn cần copy/paste vào từng cell (ô lệnh) trong Google Colab để chạy toàn bộ pipeline.

### Bước 1: Khởi tạo môi trường và Clone mã nguồn
Mở một sổ tay (notebook) mới trên Google Colab. Bật GPU nếu cần thiết bằng cách vào `Runtime` -> `Change runtime type` -> Chọn `Hardware accelerator` là `GPU` (hoặc T4 GPU). Sau đó chạy cell sau:

```bash
# Clone repository về máy ảo Colab
!git clone https://github.com/tvhahn/weibull-knowledge-informed-ml.git

# Di chuyển vào thư mục dự án
%cd weibull-knowledge-informed-ml

# Colab đã có sẵn hầu hết các thư viện (PyTorch, Pandas, Numpy, v.v.).
# Chỉ cần cài đặt package nội bộ `src` của dự án vào môi trường hiện tại:
!pip install -e .
```

### Bước 2: Tải và Giải nén Dữ liệu (Download & Extract Data)
Dự án sử dụng các bash script tự động tải dữ liệu gốc từ kho của NASA (sử dụng gdown).

```bash
# Tải dữ liệu về thư mục data/raw (Mất một chút thời gian do dung lượng lớn)
!make download

# Giải nén dữ liệu đã tải
!make extract
```
*Lưu ý: Lệnh `make download` sẽ tự động gọi `bash src/data/download_data_local.sh`.*

### Bước 3: Tiền xử lý Dữ liệu (Data Processing)
Chuyển đổi dữ liệu thô dạng file rời rạc thành dữ liệu chuẩn bị cho huấn luyện (Processed data). Quá trình này sẽ biến đổi tín hiệu chuỗi thời gian bằng Fast Fourier Transform (FFT).

```bash
# Xử lý và tạo tập dữ liệu
!make data
```
*Script này chạy `python src/data/make_dataset.py data/raw data/processed`.*

### Bước 4: Chạy Huấn luyện Mô hình (Training)
Giờ đây bạn có thể bắt đầu huấn luyện. Bạn có thể chọn huấn luyện trên tập dữ liệu IMS hoặc FEMTO. Vòng lặp huấn luyện sẽ tự động duyệt qua cả 9 hàm Loss (bao gồm các nhóm RMSE thông thường và Weibull) để chạy so sánh.

```bash
# Cách 1: Huấn luyện trên tập IMS
!make train_ims

# Cách 2: Huấn luyện trên tập FEMTO (PRONOSTIA)
!make train_femto
```

*Nếu bạn chỉ muốn test nhanh mà không chờ chạy toàn bộ số vòng lặp (Random Search Iterations), bạn có thể gọi trực tiếp file python và thêm các cấu hình (arguments) hoặc sửa trực tiếp tham số trong `src/models/train_models.py` trước khi chạy lệnh:*
```bash
!python src/models/train_models.py --data_set ims --path_data data/processed --proj_dir .
```

### Bước 5: Tổng hợp và Xuất báo cáo (Summarize & Visualize)
Sau khi quá trình huấn luyện hoàn tất, các checkpoint của model và file `.csv` kết quả sẽ được lưu trong `models/final/` và `models/interim/`. Chạy các lệnh sau để tổng hợp số liệu và vẽ đồ thị:

```bash
# Tổng hợp kết quả thành các bảng phân tích (chọn ims hoặc femto)
!make summarize_ims_models

# Vẽ các biểu đồ dữ liệu và biểu đồ kết quả (sẽ lưu vào reports/figures/)
!make figures_data
!make figures_results
```

### Bước 6: Xem kết quả trực tiếp trên Colab
Để xem trực quan các đồ thị hoặc số liệu, bạn có thể tạo một cell mới bằng Python và hiển thị ảnh từ thư mục báo cáo:

```python
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Đọc và hiển thị một đồ thị kết quả
img = mpimg.imread('reports/figures/ims_data_processed.png') # Hoặc đổi tên file tùy ý
plt.figure(figsize=(15,10))
plt.imshow(img)
plt.axis('off')
plt.show()
```
