"""Reusable visual components for the WORKBank Streamlit report."""

import streamlit as st

from .constants import COLORS

def get_plotly_layout(title="", height=500, showlegend=True):
    """Standard light-themed plotly layout."""
    return dict(
        title=dict(
            text=title,
            font=dict(size=14, color='#0F172A', family='Inter', weight='bold'),
            x=0.5,
            xanchor='center',
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#64748B', family='Inter'),
        showlegend=showlegend,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(size=10, color='#64748B'),
        ),
        xaxis=dict(
            gridcolor='#F1F5F9',
            zerolinecolor='#E2E8F0',
            linecolor='#E2E8F0',
            tickfont=dict(size=11, color='#64748B'),
        ),
        yaxis=dict(
            gridcolor='#F1F5F9',
            zerolinecolor='#E2E8F0',
            linecolor='#E2E8F0',
            tickfont=dict(size=11, color='#64748B'),
        ),
        margin=dict(l=60, r=30, t=60, b=70),
        height=height,
        hoverlabel=dict(
            bgcolor='white',
            font_size=12,
            font_family='Inter',
            font_color='#0F172A',
            bordercolor='#E2E8F0',
        ),
    )


def render_metric_card(value, label, subtext, color="blue", icon=""):
    """Render a compact KPI card used across the report."""
    safe_color = color if color in {"blue", "purple", "green", "orange", "pink"} else "blue"
    st.markdown(
        f"""
<div class="metric-card">
    <div class="metric-content">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtext">{subtext}</div>
    </div>
    <div class="metric-icon-container circle-{safe_color}">{icon}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_argument_map(total_count, paradox_pct, avg_auto, avg_has):
    """Render the report's central thesis so all chapters read as one argument."""
    st.markdown(f"""
<div class="chart-card">
<div class="section-header" style="margin-top: 0;">🧭 Tổng quan luận điểm</div>
<div class="section-desc" style="text-align: justify; line-height: 1.55;">
Luận điểm trung tâm: <strong>Nghịch lý tự động hóa không phải là sự mâu thuẫn, mà là tín hiệu phân tầng trách nhiệm giữa AI và con người.</strong>
Khi kỹ sư đồng thời mong muốn tự động hóa cao và giữ quyền tự quyết, dữ liệu cho thấy nhu cầu thiết kế hệ thống AI theo nguyên tắc: AI mở rộng năng lực thực thi, con người giữ quyền phán quyết tại các điểm rủi ro.
</div>
<div class="evidence-chain">
<strong>Dẫn chứng:</strong> Với <strong>{total_count:,}</strong> phản hồi, nhóm Nghịch lý chiếm <strong>{paradox_pct:.1f}%</strong>; điểm mong muốn tự động hóa trung bình là <strong>{avg_auto:.2f}/5</strong> và quyền tự quyết trung bình là <strong>{avg_has:.2f}/5</strong>. Báo cáo không dừng ở câu hỏi "kỹ sư có muốn AI hay không" mà chuyển sang: <strong>tác vụ nào nên giao cho AI, tác vụ nào cần cơ chế kiểm soát của con người, và kiến trúc nào phù hợp?</strong>
</div>
<div class="argument-rail">
    <div class="argument-step">
        <div class="step-label">Chương 1</div>
        <div class="step-title">Nhận diện Nghịch lý</div>
        <div class="step-body">Xác định nhóm kỹ sư đồng thời mong muốn tự động hóa lẫn quyền kiểm soát — điểm xuất phát cho bài toán quản trị AI.</div>
    </div>
    <div class="argument-step">
        <div class="step-label">Chương 2</div>
        <div class="step-title">Phân tích cơ chế</div>
        <div class="step-body">Phân biệt trải nghiệm LLM nông và sâu: tác vụ đơn giản tạo kỳ vọng ủy thác, tác vụ kỹ thuật sâu kích hoạt nhu cầu giám sát.</div>
    </div>
    <div class="argument-step">
        <div class="step-label">Chương 3</div>
        <div class="step-title">Thiết kế kiến trúc</div>
        <div class="step-body">Dùng xác suất Paradox để chọn mô hình tác tử: tự trị, đồng hành hai tác tử, hoặc giám sát có cổng phê duyệt.</div>
    </div>
    <div class="argument-step">
        <div class="step-label">Chương 4</div>
        <div class="step-title">Hành động cụ thể</div>
        <div class="step-body">Gắn từng phát hiện với can thiệp, chủ thể chịu trách nhiệm và KPI kiểm chứng khả năng cải thiện quy trình.</div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)
