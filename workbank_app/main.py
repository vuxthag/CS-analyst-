"""Main Streamlit orchestration for the WORKBank report."""

import pandas as pd
import streamlit as st

from .components import render_argument_map, render_metric_card
from .constants import EXPERIENCE_MAP, GENDER_MAP, OCC_COL, OCCUPATION_MAP
from .data import load_data, prepare_csit_data, train_logistic_model
from .styles import inject_custom_css
from .views import render_recommendations, render_tab1, render_tab2, render_tab3

def main():
    inject_custom_css()

    # Load data
    desires, metadata, expert, tasks = load_data()
    full_merged = prepare_csit_data(desires, metadata, tasks)
    # Pre-populate filters in session state if not present
    all_occs = sorted(full_merged[OCC_COL].unique())
    all_genders = sorted(full_merged['Gender'].dropna().unique())
    all_exp = ['Less than 1 year', '1-2 year', '3-5 years', '6-10 years', 'More than 10 years']
    available_exp = [e for e in all_exp if e in full_merged['Experience'].unique()]

    if "all_occs_check" not in st.session_state:
        st.session_state["all_occs_check"] = True
        for occ in all_occs:
            st.session_state[f"occ_{occ}"] = True

    if "all_genders_check" not in st.session_state:
        st.session_state["all_genders_check"] = True
        for gender in all_genders:
            st.session_state[f"gender_{gender}"] = True

    if "all_exp_check" not in st.session_state:
        st.session_state["all_exp_check"] = True
        for exp in available_exp:
            st.session_state[f"exp_{exp}"] = True

    # Callback functions for filters
    def toggle_all_occs():
        val = st.session_state.all_occs_check
        for occ in all_occs:
            st.session_state[f"occ_{occ}"] = val

    def update_select_all_occ():
        st.session_state.all_occs_check = all(
            st.session_state[f"occ_{occ}"] for occ in all_occs
        )

    def toggle_all_genders():
        val = st.session_state.all_genders_check
        for gender in all_genders:
            st.session_state[f"gender_{gender}"] = val

    def update_select_all_gender():
        st.session_state.all_genders_check = all(
            st.session_state[f"gender_{gender}"] for gender in all_genders
        )

    def toggle_all_exps():
        val = st.session_state.all_exp_check
        for exp in available_exp:
            st.session_state[f"exp_{exp}"] = val

    def update_select_all_exp():
        st.session_state.all_exp_check = all(
            st.session_state[f"exp_{exp}"] for exp in available_exp
        )

    # ── SIDEBAR ──
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1.5rem; padding: 10px 0;">
            <div style="background: linear-gradient(135deg, #8B5CF6, #3B82F6); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.4rem; font-weight: bold; box-shadow: 0 4px 10px rgba(139, 92, 246, 0.2);">
                📊
            </div>
            <div>
                <h2 style="margin: 0; font-size: 1.1rem; font-weight: 800; color: #0F172A; line-height: 1.2;">
                    WORKBank CS/IT
                </h2>
                <p style="color: #64748B; font-size: 0.72rem; margin: 0; font-weight: 500;">
                    Bảng điều khiển phân tích tự động hóa
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.sidebar.markdown("<div style='font-size: 0.75rem; font-weight: 800; color: #475569; letter-spacing: 0.05em; margin-top: 0.5rem; margin-bottom: 0.2rem;'>ĐIỀU HƯỚNG</div>", unsafe_allow_html=True)
        
        views = [
            "Bức tranh Nghịch lý",
            "Hiệu ứng LLM",
            "Kiến trúc AI Agent",
            "Khuyến nghị chiến lược"
        ]
        icons = ["📊", "🔥", "🏗️", "🎯"]
        view_labels = [f"{icon} {view}" for icon, view in zip(icons, views)]
        
        selected_view_label = st.sidebar.radio(
            "NAV",
            options=view_labels,
            index=0,
            label_visibility="collapsed"
        )
        selected_view = selected_view_label.split(" ", 1)[1]

        st.sidebar.markdown("<div style='font-size: 0.75rem; font-weight: 800; color: #475569; letter-spacing: 0.05em; margin-top: 1rem; margin-bottom: 0.5rem;'>BỘ LỌC</div>", unsafe_allow_html=True)

        # Occupation filter
        st.markdown("<div style='font-size: 0.72rem; font-weight: 700; color: #475569; letter-spacing: 0.05em; margin-top: 0.8rem; margin-bottom: 0.2rem; text-transform: uppercase;'>🏢 NGHỀ NGHIỆP CS/IT</div>", unsafe_allow_html=True)
        st.checkbox("Chọn tất cả nghề nghiệp", key="all_occs_check", on_change=toggle_all_occs)
        selected_occs = []
        with st.container(height=200):
            for occ in all_occs:
                if st.checkbox(OCCUPATION_MAP.get(occ, occ), key=f"occ_{occ}", on_change=update_select_all_occ):
                    selected_occs.append(occ)

        # Gender filter
        st.markdown("<div style='font-size: 0.72rem; font-weight: 700; color: #475569; letter-spacing: 0.05em; margin-top: 0.8rem; margin-bottom: 0.2rem; text-transform: uppercase;'>👤 GIỚI TÍNH</div>", unsafe_allow_html=True)
        st.checkbox("Chọn tất cả giới tính", key="all_genders_check", on_change=toggle_all_genders)
        selected_genders = []
        with st.container(height=120):
            for gender in all_genders:
                if st.checkbox(GENDER_MAP.get(gender, gender), key=f"gender_{gender}", on_change=update_select_all_gender):
                    selected_genders.append(gender)

        # Experience filter
        st.markdown("<div style='font-size: 0.72rem; font-weight: 700; color: #475569; letter-spacing: 0.05em; margin-top: 0.8rem; margin-bottom: 0.2rem; text-transform: uppercase;'>📅 KINH NGHIỆM</div>", unsafe_allow_html=True)
        st.checkbox("Chọn tất cả kinh nghiệm", key="all_exp_check", on_change=toggle_all_exps)
        selected_exp = []
        with st.container(height=150):
            for exp in available_exp:
                if st.checkbox(EXPERIENCE_MAP.get(exp, exp), key=f"exp_{exp}", on_change=update_select_all_exp):
                    selected_exp.append(exp)


        # Scope info box
        st.sidebar.markdown(f"""<div class="sidebar-info-box">
        <h4>TỔNG QUAN DỮ LIỆU</h4>
        <ul>
        <li><strong>{full_merged['User ID'].nunique()}</strong> kỹ sư tham gia</li>
        <li><strong>{len(full_merged)}</strong> phản hồi tác vụ</li>
        <li><strong>{full_merged[OCC_COL].nunique()}</strong> nhóm ngành CNTT</li>
        <li>WORKBank · Tháng 1–5/2025</li>
        </ul>
        </div>
        <div style="text-align: center; margin-top: 1.2rem; padding: 0.5rem;">
        <p style="color: #94A3B8; font-size: 0.68rem; margin: 0; line-height: 1.4;">
        Nguồn dữ liệu: <strong>WORKBank</strong><br>
        Stanford SALT Lab · 2025
        </p>
        </div>""", unsafe_allow_html=True)

    # Apply filters
    df = full_merged.copy()
    df = df[df[OCC_COL].isin(selected_occs)]
    df = df[df['Gender'].isin(selected_genders)]
    df = df[df['Experience'].isin(selected_exp)]

    if len(df) == 0:
        st.warning("⚠️ Không có dữ liệu phù hợp. Vui lòng điều chỉnh bộ lọc ở thanh bên.")
        return

    paradox_count = df['is_paradox'].sum()
    total_count = len(df)
    paradox_pct = paradox_count / total_count * 100 if total_count > 0 else 0
    avg_auto = df['Automation Desire Rating'].mean()
    avg_has = df['Human Agency Scale Rating'].mean()

    std_auto = df['Automation Desire Rating'].std()
    std_has = df['Human Agency Scale Rating'].std()

    std_auto_str = f"σ = {std_auto:.2f}" if not pd.isna(std_auto) else "σ = N/A"
    std_has_str = f"σ = {std_has:.2f}" if not pd.isna(std_has) else "σ = N/A"

    # Train model on full data
    lr_model, scaler, p_values = train_logistic_model(full_merged)
    is_intro_view = selected_view == "Bức tranh Nghịch lý"

    # ── HERO HEADER ──
    col_header_left, col_header_right = st.columns([7, 3])
    
    with col_header_left:
        st.markdown("""<div style="padding-top: 10px;">
<div class="hero-title">Nghịch lý Tự động hóa × Hiệu ứng LLM</div>
<div class="hero-subtitle" style="margin-bottom: 0.8rem;">
Phân tích hành vi kỹ sư CNTT và thiết kế hệ thống AI có kiểm soát — WORKBank 2025
</div>
</div>
""", unsafe_allow_html=True)
        if is_intro_view:
            st.markdown(f"""
<div style="display: inline-flex; align-items: center; gap: 10px; background: rgba(249, 115, 22, 0.05); border: 1px solid rgba(249, 115, 22, 0.18); border-radius: 12px; padding: 8px 16px; margin-bottom: 1.5rem; max-width: 90%;">
    <span style="font-size: 1.1rem; line-height: 1;">💡</span>
    <span style="font-size: 0.8rem; color: #475569; line-height: 1.45;">
        <strong>MỤC TIÊU:</strong> Lý giải vì sao <strong>{paradox_pct:.1f}%</strong> phản hồi đồng thời mong muốn tự động hóa lẫn quyền kiểm soát — từ đó đề xuất nguyên tắc thiết kế AI Agent, quy trình quản trị và KPI đo lường.
    </span>
</div>
""", unsafe_allow_html=True)
        
    with col_header_right:
        st.markdown("""<div style="display: flex; justify-content: flex-end; align-items: center; gap: 8px; margin-bottom: 8px; margin-top: 10px;">
<div style="display: flex; align-items: center; gap: 6px; background: rgba(34, 197, 94, 0.1); padding: 4px 10px; border-radius: 20px; font-size: 0.72rem; color: #22C55E; font-weight: 600;">
<span style="display: inline-block; width: 6px; height: 6px; background-color: #22C55E; border-radius: 50%;"></span>
SẴN SÀNG
</div>
</div>""", unsafe_allow_html=True)


    if is_intro_view:
        # ── TOP METRICS ──
        mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)
        with mcol1:
            render_metric_card(f"{total_count:,}", "TỔNG PHẢN HỒI", "quan sát", "blue", "👥")
        with mcol2:
            render_metric_card(f"{paradox_count}", "NHÓM NGHỊCH LÝ", "phản hồi Paradox", "purple", "🧩")
        with mcol3:
            render_metric_card(f"{paradox_pct:.1f}%", "TỶ LỆ NGHỊCH LÝ", "trên tổng mẫu", "pink", "📈")
        with mcol4:
            render_metric_card(f"{avg_auto:.2f} / 5", "MONG MUỐN TỰ ĐỘNG HÓA", std_auto_str, "orange", "🎯")
        with mcol5:
            render_metric_card(f"{avg_has:.2f} / 5", "QUYỀN TỰ QUYẾT", std_has_str, "green", "🤝")

        st.markdown("")
        render_argument_map(total_count, paradox_pct, avg_auto, avg_has)

    # ── VIEW SWITCHING ──
    if selected_view == "Bức tranh Nghịch lý":
        render_tab1(df)
        
    elif selected_view == "Hiệu ứng LLM":
        render_tab2(df, lr_model, scaler, p_values)
        
    elif selected_view == "Kiến trúc AI Agent":
        render_tab3(df, lr_model, scaler)

    elif selected_view == "Khuyến nghị chiến lược":
        render_recommendations(df)
