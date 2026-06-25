"""Shared constants and labels for the WORKBank Streamlit report."""

CS_IT_OCCUPATIONS = [
    'Computer Programmers',
    'Computer Systems Analysts',
    'Computer Systems Engineers/Architects',
    'Computer User Support Specialists',
    'Computer and Information Research Scientists',
    'Computer and Information Systems Managers',
    'Computer Network Support Specialists',
    'Database Administrators',
    'Information Security Analysts',
    'Information Technology Project Managers',
    'Network and Computer Systems Administrators',
    'Software Quality Assurance Analysts and Testers',
    'Web Administrators',
    'Web Developers',
    'Video Game Designers',
]

OCC_COL = 'Occupation (O*NET-SOC Title)'
FREQ_MAP = {'Never': 0, 'Monthly': 1, 'Weekly': 2, 'Daily': 3}
FREQ_VALUES = ['Never', 'Monthly', 'Weekly', 'Daily']
FREQ_LABELS = [
    'Không bao giờ (Never)',
    'Hàng tháng (Monthly)',
    'Hàng tuần (Weekly)',
    'Hàng ngày (Daily)',
]
FREQ_LABEL_TO_VALUE = dict(zip(FREQ_LABELS, FREQ_VALUES))
FREQ_DISPLAY_MAP = dict(zip(FREQ_VALUES, FREQ_LABELS))

OCCUPATION_MAP = {
    'Computer Programmers': 'Lập trình viên Máy tính (Computer Programmers)',
    'Computer Systems Analysts': 'Nhà phân tích Hệ thống Máy tính (Computer Systems Analysts)',
    'Computer Systems Engineers/Architects': 'Kỹ sư/Kiến trúc sư Hệ thống Máy tính (Computer Systems Engineers/Architects)',
    'Computer User Support Specialists': 'Chuyên viên Hỗ trợ Người dùng Máy tính (Computer User Support Specialists)',
    'Computer and Information Research Scientists': 'Nhà khoa học Nghiên cứu Máy tính & Thông tin (Computer and Information Research Scientists)',
    'Computer and Information Systems Managers': 'Quản lý Hệ thống Máy tính & Thông tin (Computer and Information Systems Managers)',
    'Computer Network Support Specialists': 'Chuyên viên Hỗ trợ Mạng Máy tính (Computer Network Support Specialists)',
    'Database Administrators': 'Quản trị viên Cơ sở Dữ liệu (Database Administrators)',
    'Information Security Analysts': 'Nhà phân tích An toàn Thông tin (Information Security Analysts)',
    'Information Technology Project Managers': 'Quản lý Dự án Công nghệ Thông tin (Information Technology Project Managers)',
    'Network and Computer Systems Administrators': 'Quản trị viên Hệ thống Mạng & Máy tính (Network and Computer Systems Administrators)',
    'Software Quality Assurance Analysts and Testers': 'Nhà phân tích & Kiểm thử Chất lượng Phần mềm (Software QA Analysts & Testers)',
    'Web Administrators': 'Quản trị viên Trang web (Web Administrators)',
    'Web Developers': 'Nhà phát triển Trang web (Web Developers)',
    'Video Game Designers': 'Nhà thiết kế Trò chơi Điện tử (Video Game Designers)',
}

GENDER_MAP = {
    'Male': 'Nam (Male)',
    'Female': 'Nữ (Female)',
    'Non-binary': 'Phi nhị nguyên (Non-binary)',
    'Other': 'Khác (Other)',
    'Prefer not to say': 'Không muốn trả lời (Prefer not to say)',
}

EXPERIENCE_MAP = {
    'Less than 1 year': 'Dưới 1 năm (Less than 1 year)',
    '1-2 year': 'Từ 1-2 năm (1-2 years)',
    '3-5 years': 'Từ 3-5 năm (3-5 years)',
    '6-10 years': 'Từ 6-10 năm (6-10 years)',
    'More than 10 years': 'Trên 10 năm (More than 10 years)',
}

REASON_MAP = {
    'Free Time': 'Giải phóng thời gian (Free Time)',
    'Repetitive': 'Tác vụ lặp lại (Repetitive)',
    'Human Error': 'Lỗi do con người (Human Error)',
    'Stress': 'Giảm căng thẳng (Stress)',
    'Difficulty': 'Độ khó cao (Difficulty)',
    'Scale': 'Quy mô (Scale)',
    'Speed': 'Tốc độ (Speed)',
    'Quality': 'Chất lượng (Quality)',
    'Enjoyment': 'Sự hứng thú (Enjoyment)',
    'Physical': 'Yếu tố thể chất (Physical)',
    'Control': 'Quyền kiểm soát (Control)',
    'Domain Knowledge': 'Tri thức miền chuyên môn (Domain Knowledge)',
    'Empathy': 'Sự thấu cảm (Empathy)',
    'Quality Oversight': 'Giám sát chất lượng (Quality Oversight)',
    'Dynamic': 'Môi trường biến động (Dynamic Environment)',
    'Ethical': 'Yếu tố đạo đức (Ethical)',
    'Critical': 'Trọng yếu (Critical)',
    'Privacy': 'Quyền riêng tư (Privacy)',
}

LLM_USAGE_COLS = [
    'LLM Usage by Type - Information Access',
    'LLM Usage by Type - Edit',
    'LLM Usage by Type - Idea Generation',
    'LLM Usage by Type - Communication',
    'LLM Usage by Type - Analysis',
    'LLM Usage by Type - Decision',
    'LLM Usage by Type - Coding',
    'LLM Usage by Type - System Design',
    'LLM Usage by Type - Data Processing',
]

LLM_SHORT_NAMES = {
    'LLM Usage by Type - Information Access': 'Truy cập Thông tin (Information Access)',
    'LLM Usage by Type - Edit': 'Chỉnh sửa / Viết lại (Edit / Rewrite)',
    'LLM Usage by Type - Idea Generation': 'Ý tưởng sáng tạo (Idea Generation)',
    'LLM Usage by Type - Communication': 'Giao tiếp (Communication)',
    'LLM Usage by Type - Analysis': 'Phân tích (Analysis)',
    'LLM Usage by Type - Decision': 'Ra quyết định (Decision Making)',
    'LLM Usage by Type - Coding': 'Lập trình (Coding)',
    'LLM Usage by Type - System Design': 'Thiết kế Hệ thống (System Design)',
    'LLM Usage by Type - Data Processing': 'Xử lý Dữ liệu (Data Processing)',
}

# Light theme color palette
COLORS = {
    'paradox': '#EC4899',       # Pink accent
    'consistent': '#3B82F6',    # Blue accent
    'bg_light': '#F8FAFC',
    'card_bg': 'rgba(255, 255, 255, 0.75)',
    'accent_cyan': '#0EA5E9',
    'accent_orange': '#F97316',
    'accent_green': '#22C55E',
    'accent_purple': '#8B5CF6',
    'text_primary': '#0F172A',
    'text_secondary': '#64748B',
    'grid': '#E2E8F0',
}

# ──────────────────────────────────────────────────
