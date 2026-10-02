# 🚀 HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY DỰ ÁN

Tài liệu này hướng dẫn chi tiết từng bước thiết lập môi trường và chạy ứng dụng web **Lao OCR & Educational Translation System** trên hệ điều hành **Windows (PowerShell)**.

---

## 📌 1. Yêu cầu Hệ thống & Chuẩn bị

- **Hệ điều hành:** Windows 10 / 11 (hỗ trợ PowerShell 5.1+ hoặc PowerShell 7)
- **Python:** Phiên bản khuyến nghị là `Python 3.10` hoặc `Python 3.11` (tránh 3.12+ nếu một số thư viện torch/paddleocr chưa tối ưu).
- **RAM:** Tối thiểu 4GB (Khuyến nghị 8GB+ để chạy mượt mô hình học sâu LaoCRNN).
- *(Tùy chọn)* **Tesseract OCR:** Nếu bạn muốn chạy thêm động cơ so sánh Tesseract 5 (P4/P5).

---

## ⚙️ 2. Quy trình Cài đặt Từng bước trên PowerShell

Mở cửa sổ **PowerShell** tại thư mục dự án:  
*(Đường dẫn hiện tại: `c:\Users\maiduc.vinh\OneDrive - VietCredit\Desktop\XLA`)*

### Bước 2.1: Cài đặt Python (Nếu máy chưa có)
Nếu máy bạn chưa nhận lệnh `python`, bạn có thể cài đặt tự động bằng Windows Package Manager (`winget`):

```powershell
winget install Python.Python.3.11
```

> ⚠️ **Quan trọng:** Sau khi cài đặt hoàn tất, hãy **tắt hoàn toàn PowerShell và mở lại** để Windows cập nhật biến môi trường `PATH`.  
> Kiểm tra lại bằng lệnh:
> ```powershell
> python --version
> ```

---

### Bước 2.2: Cho phép chạy Script trên PowerShell
Mặc định Windows PowerShell chặn chạy script `.ps1`. Hãy cấp quyền cho người dùng hiện tại:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
*(Bấm `Y` hoặc `A` rồi nhấn Enter nếu được hỏi xác nhận).*

---

### Bước 2.3: Tạo và kích hoạt Môi trường ảo (Virtual Environment)
Khuyến nghị luôn sử dụng môi trường ảo để cô lập các thư viện của dự án:

```powershell
# 1. Tạo môi trường ảo mang tên .venv
python -m venv .venv

# 2. Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1
```

> ✅ Khi kích hoạt thành công, bạn sẽ thấy tiền tố `(.venv)` xuất hiện ở đầu dấu nhắc lệnh:  
> `(.venv) PS C:\Users\...\XLA>`

---

### Bước 2.4: Nâng cấp pip và cài đặt thư viện
Chạy lệnh cài đặt toàn bộ phụ thuộc từ file [requirements.txt](file:///c:/Users/maiduc.vinh/OneDrive%20-%20VietCredit/Desktop/XLA/requirements.txt):

```powershell
# Nâng cấp pip lên bản mới nhất
python -m pip install --upgrade pip

# Cài đặt tất cả thư viện cần thiết
pip install -r requirements.txt
```

---

## 🌐 3. Lệnh Khởi chạy Ứng dụng Web

Sau khi môi trường ảo đã được kích hoạt và cài đặt thư viện đầy đủ, chạy lệnh sau:

```powershell
streamlit run app.py
```

hoặc:
```powershell
python -m streamlit run app.py
```

### 🖥️ Kết quả mong đợi:
PowerShell sẽ xuất ra thông báo:
```text
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```
Trình duyệt web mặc định của bạn sẽ tự động mở trang web ứng dụng. Nếu không tự mở, bạn chỉ cần copy đường dẫn `http://localhost:8501` dán vào Chrome/Edge.

Để **dừng ứng dụng**, nhấn tổ hợp phím `Ctrl + C` trên cửa sổ PowerShell.

---

## ⚡ 4. Cách Chạy Nhanh (Shortcut Script)

Để không phải gõ lại từng lệnh kích hoạt mỗi lần làm việc, dự án cung cấp script tiện ích:

### Cách 1: Chạy file PowerShell
```powershell
.\run_app.ps1
```

### Cách 2: Chạy file Batch (hoặc nhấp đúp chuột)
```cmd
.\run_app.bat
```
*(File này sẽ tự động kiểm tra `.venv`, tự kích hoạt và khởi chạy Streamlit).*

---

## 🧪 5. Các Lệnh Thực nghiệm & Kiểm thử Khác

Nếu bạn muốn chạy kiểm thử hoặc chạy các script huấn luyện / tiền xử lý:

```powershell
# Chạy toàn bộ Unit Tests của dự án
pytest tests/ -v

# Kiểm tra phân tích các bước tiền xử lý ảnh
python scripts/inspect_preprocessing_stages.py

# Kiểm tra độ tương thích font tiếng Lào
python -c "from src.utils.font_check import check_lao_fonts; print(check_lao_fonts())"
```

---

## 🛠️ 6. Khắc phục Sự cố Thường gặp (Troubleshooting)

| Vấn đề / Lỗi | Nguyên nhân | Cách xử lý |
| :--- | :--- | :--- |
| `Python was not found...` | Windows chưa cài Python hoặc chưa tick `Add Python to PATH` | Cài đặt lại bằng `winget install Python.Python.3.11` hoặc tải từ [python.org](https://www.python.org/downloads/), chú ý tick chọn **"Add python.exe to PATH"**. Sau đó mở lại PowerShell. |
| `File ... Activate.ps1 cannot be loaded because running scripts is disabled` | Chính sách bảo mật ExecutionPolicy của PowerShell | Chạy lệnh: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `streamlit: The term 'streamlit' is not recognized...` | Chưa kích hoạt môi trường ảo hoặc chưa `pip install -r requirements.txt` | Kích hoạt môi trường ảo: `.\.venv\Scripts\Activate.ps1`, sau đó kiểm tra lại bằng lệnh `pip list`. |
| `tesseract is not installed or it's not in your PATH` | Tesseract OCR chưa được cài đặt | Động cơ mặc định **LaoCRNN** vẫn hoạt động bình thường mà không cần Tesseract. Nếu muốn dùng Tesseract: Cài đặt qua `winget install UB-Mannheim.TesseractOCR` và thêm đường dẫn cài đặt vào PATH. |
| Lỗi font chữ tiếng Lào bị ô vuông hoặc mất dấu | Hệ điều hành thiếu font Unicode tiếng Lào | Cài đặt font `Saysettha OT`, `Noto Sans Lao`, hoặc `Phetsarath OT` vào Windows Fonts. |

---

*Mọi thắc mắc và đóng góp vui lòng xem thêm tài liệu chi tiết tại thư mục [docs/](file:///c:/Users/maiduc.vinh/OneDrive%20-%20VietCredit/Desktop/XLA/docs).*
