# Thư mục `docs`

### 1. Mục đích chính
Thư mục này phục vụ việc tự động tạo tài liệu dự án. Mặc định nó được khởi tạo dựa trên công cụ `Sphinx` (một tool phổ biến trong Python để build Documentations từ docstrings).

### 2. Cấu trúc và Các file bên trong
- **`conf.py`**: File cấu hình lõi của Sphinx. Định nghĩa tên dự án, tác giả, phiên bản, cũng như các extensions cần dùng (như autodoc để tự động kéo docstring từ code vào tài liệu).
- **`index.rst`** & **`getting-started.rst`**: Các trang nội dung được viết bằng định dạng reStructuredText (RST). Đây là trang chủ và trang Hướng dẫn bắt đầu cho docs.
- **`commands.rst`**: Liệt kê các dòng lệnh hữu ích (thường trích từ Makefile) cho người mới bắt đầu.
- **`Makefile`** và **`make.bat`**: Các script hỗ trợ việc tự động build docs thành dạng HTML hoặc PDF trên Linux/Mac (`Makefile`) hoặc Windows (`make.bat`).

### 3. Thông tin quan trọng
- Bạn có thể chuyển đổi tất cả nội dung trong thư mục này thành một trang web HTML hoàn chỉnh bằng cách chạy lệnh `make html` trong thư mục `docs/`. Trang web xuất ra sẽ nằm ở `docs/_build/html`.

### 4. Điểm cần lưu ý
- Hiện tại, tài liệu trong dự án chưa được tác giả mở rộng nhiều (nội dung đang khá tĩnh và chỉ có sườn cơ bản). Nó sẽ cực kỳ hữu ích nếu bạn muốn xuất bản repo này dưới dạng package.
