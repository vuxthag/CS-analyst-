# WORKBank CS/IT Analyst Dashboard

Dashboard Streamlit phân tích dữ liệu WORKBank cho nhóm nghề Computer Science / Information Technology, tập trung vào nghịch lý tự động hóa: kỹ sư vừa muốn AI tự động hóa tác vụ, vừa muốn giữ quyền kiểm soát và phê duyệt của con người.

## Tổng quan

Ứng dụng trực quan hóa dữ liệu khảo sát WORKBank để trả lời các câu hỏi chính:

- Nhóm CS/IT nào có mức "Automation Desire" và "Human Agency Scale" cùng cao?
- Tần suất sử dụng LLM theo từng loại tác vụ liên quan thế nào tới nhu cầu kiểm soát?
- Có thể dùng xác suất thuộc nhóm "Paradox" để gợi ý kiến trúc AI Agent phù hợp không?
- Từ dữ liệu có thể rút ra khuyến nghị triển khai AI có kiểm soát cho đội kỹ thuật như thế nào?

## Tính năng

- Dashboard Streamlit nhiều trang với điều hướng bên trái.
- Bộ lọc theo nghề CS/IT, giới tính và số năm kinh nghiệm.
- Biểu đồ Plotly tương tác cho phân bố Automation Desire / Human Agency Scale.
- Phân tích nhóm "Paradox" so với nhóm "Consistent".
- Mô hình Logistic Regression để ước lượng xác suất thuộc nhóm nghịch lý dựa trên tần suất dùng LLM.
- Gợi ý kiến trúc AI Agent và khuyến nghị chiến lược kèm KPI triển khai.

## Cấu trúc thư mục

```text
.
├── app.py
├── workbank_app/
│   ├── main.py
│   ├── data.py
│   ├── views.py
│   ├── components.py
│   ├── constants.py
│   └── styles.py
├── domain_worker_desires.csv
├── domain_worker_metadata.csv
├── expert_rated_technological_capability.csv
├── task_statement_with_metadata.csv
├── explore_deep.py
├── validate_csit.py
└── 2506.06576v3.pdf
```

## Cài đặt

Yêu cầu Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Trên Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Chạy dashboard

```bash
streamlit run app.py
```

Sau khi chạy, mở địa chỉ local mà Streamlit hiển thị, thường là:

```text
http://localhost:8501
```

## Dữ liệu

Ứng dụng đọc trực tiếp các file CSV ở thư mục gốc:

- `domain_worker_desires.csv`
- `domain_worker_metadata.csv`
- `expert_rated_technological_capability.csv`
- `task_statement_with_metadata.csv`

Các file này cần được giữ cùng cấp với `app.py` để dashboard chạy đúng.

## Script phân tích

Ngoài dashboard chính, repo có hai script hỗ trợ:

- `validate_csit.py`: kiểm tra nhanh dữ liệu CS/IT, tỷ lệ nhóm Paradox và hệ số mô hình.
- `explore_deep.py`: phân tích khám phá sâu hơn trên dữ liệu WORKBank.

Chạy ví dụ:

```bash
python validate_csit.py
```

## Chuẩn bị đẩy lên GitHub

Remote dự kiến:

```bash
git remote add origin https://github.com/vuxthag/CS-analyst-.git
git branch -M main
git push -u origin main
```

Nếu remote `origin` đã tồn tại, dùng:

```bash
git remote set-url origin https://github.com/vuxthag/CS-analyst-.git
```

## Ghi chú triển khai

- Không commit thư mục `__pycache__`, môi trường ảo, file `.env` hoặc secret Streamlit.
- Có thể deploy nhanh bằng Streamlit Community Cloud với entry point `app.py`.
- Khi deploy, đảm bảo các file CSV được đưa lên repo hoặc cấu hình nguồn dữ liệu thay thế.
