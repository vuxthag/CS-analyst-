"""Chapter and section renderers for the WORKBank Streamlit report."""

from html import escape

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from .components import get_plotly_layout, render_metric_card
from .constants import (
    COLORS,
    EXPERIENCE_MAP,
    FREQ_DISPLAY_MAP,
    FREQ_LABELS,
    FREQ_LABEL_TO_VALUE,
    FREQ_MAP,
    LLM_SHORT_NAMES,
    LLM_USAGE_COLS,
    OCC_COL,
    OCCUPATION_MAP,
    REASON_MAP,
)

def render_tab1(df):
    # Prepare data with jitter
    plot_df = df.copy()
    np.random.seed(42)
    plot_df['AD_jitter'] = plot_df['Automation Desire Rating'] + np.random.uniform(-0.25, 0.25, len(plot_df))
    plot_df['HAS_jitter'] = plot_df['Human Agency Scale Rating'] + np.random.uniform(-0.25, 0.25, len(plot_df))

    # Fill missing wage with occupation median
    wage_col = 'Occupation Mean Annual Wage'
    if wage_col in plot_df.columns:
        occ_median_wage = plot_df.groupby(OCC_COL)[wage_col].transform('median')
        plot_df[wage_col] = plot_df[wage_col].fillna(occ_median_wage)
        plot_df[wage_col] = plot_df[wage_col].fillna(plot_df[wage_col].median())
        plot_df['Wage_display'] = (plot_df[wage_col] / 1000).round(1).astype(str) + 'K USD'
    else:
        plot_df[wage_col] = 100000
        plot_df['Wage_display'] = 'N/A'

    # Calculate paradox count and percentage
    paradox = plot_df[plot_df['Group'] == 'Paradox']
    consistent = plot_df[plot_df['Group'] == 'Consistent']
    paradox_count = len(paradox)
    paradox_pct = paradox_count / len(plot_df) * 100 if len(plot_df) > 0 else 0

    col_left, col_right = st.columns([35, 65])
    
    with col_left:
        st.markdown(f"""<div style="padding-right: 10px;">
<div class="section-header" style="margin-top: 0;">📊 Ma trận phân bổ kỳ vọng AI <span style="cursor: help;" title="Biểu đồ phân tán thể hiện sự kết hợp kỳ vọng của kỹ sư về tự động hóa và quyền kiểm soát">ⓘ</span></div>
<div class="section-desc" style="margin-bottom: 1.5rem; line-height: 1.5; text-align: justify;">
Trong lĩnh vực tương tác Người – Máy và Công thái học nhận thức, <strong>Nghịch lý tự động hóa của Bainbridge (1983)</strong> chỉ ra rằng: hệ thống tự động hóa càng tinh vi thì vai trò kiểm soát chiến lược của con người càng quan trọng. 
<br><br>
Khác với các mô hình chấp nhận công nghệ truyền thống, dữ liệu thực tế cho thấy <strong>{paradox_pct:.1f}% phản hồi</strong> của kỹ sư CNTT rơi vào vùng Nghịch lý: mong muốn tự động hóa ≥ 4 và quyền tự quyết ≥ 4. Nghịch lý ở đây là tín hiệu thiết kế — kỹ sư muốn AI xử lý nhiều hơn, nhưng hệ thống vẫn phải đảm bảo quyền kiểm soát, truy vết và phê duyệt của con người.
</div>
<div class="insight-mint">
<div style="font-weight: 700; color: #15803D; margin-bottom: 8px; font-size: 0.85rem; letter-spacing: 0.05em;">
    ✅ PHÁT HIỆN CHÍNH
</div>
<div style="display: flex; flex-direction: column; gap: 10px; font-size: 0.82rem; color: #166534; line-height: 1.45;">
<div style="display: flex; gap: 6px; align-items: flex-start;">
<span style="color: #22C55E;">✔️</span>
<span><strong>{paradox_count} quan sát ({paradox_pct:.1f}%)</strong> thuộc nhóm Nghịch lý.</span>
</div>
<div style="display: flex; gap: 6px; align-items: flex-start;">
<span style="color: #22C55E;">✔️</span>
<span>Nghịch lý không phải thái độ "chống AI" — đó là nhu cầu tách biệt phần việc tự động hóa được và phần việc cần trách nhiệm giải trình.</span>
</div>
<div style="display: flex; gap: 6px; align-items: flex-start;">
<span style="color: #22C55E;">✔️</span>
<span>Phát hiện này cung cấp tiêu chí thiết kế cổng phê duyệt cho các tác vụ rủi ro cao.</span>
</div>
</div>
</div>
</div>""", unsafe_allow_html=True)
        
    with col_right:
        fig = go.Figure()

        # Consistent group
        fig.add_trace(go.Scatter(
            x=consistent['AD_jitter'],
            y=consistent['HAS_jitter'],
            mode='markers',
            name='Nhất quán (Consistent)',
            marker=dict(
                size=np.clip(consistent[wage_col] / 15000, 5, 22),
                color=COLORS['consistent'],
                opacity=0.65,
                line=dict(width=0),
            ),
            customdata=np.stack([
                consistent[OCC_COL].map(OCCUPATION_MAP),
                consistent['Automation Desire Rating'],
                consistent['Human Agency Scale Rating'],
                consistent['Wage_display'],
            ], axis=-1),
            hovertemplate=(
                '<b>%{customdata[0]}</b><br>'
                'Mong muốn Tự động hóa (Automation Desire): %{customdata[1]}<br>'
                'Quyền tự quyết con người (Human Agency Scale): %{customdata[2]}<br>'
                'Mức lương (Wage): %{customdata[3]}<extra></extra>'
            ),
        ))

        # Paradox group
        fig.add_trace(go.Scatter(
            x=paradox['AD_jitter'],
            y=paradox['HAS_jitter'],
            mode='markers',
            name='Nghịch lý (Paradox)',
            marker=dict(
                size=np.clip(paradox[wage_col] / 12000, 7, 28),
                color=COLORS['paradox'],
                opacity=0.85,
                line=dict(width=1, color='rgba(255,255,255,0.6)'),
                symbol='diamond',
            ),
            customdata=np.stack([
                paradox[OCC_COL].map(OCCUPATION_MAP),
                paradox['Automation Desire Rating'],
                paradox['Human Agency Scale Rating'],
                paradox['Wage_display'],
            ], axis=-1),
            hovertemplate=(
                '<b>%{customdata[0]}</b><br>'
                'Mong muốn Tự động hóa (Automation Desire): %{customdata[1]}<br>'
                'Quyền tự quyết con người (Human Agency Scale): %{customdata[2]}<br>'
                'Mức lương (Wage): %{customdata[3]}<extra></extra>'
            ),
        ))

        # Paradox zone shading
        fig.add_shape(
            type='rect', x0=4.0, x1=5.5, y0=3.0, y1=5.5,
            fillcolor='rgba(239, 68, 68, 0.05)',
            line=dict(color='rgba(239, 68, 68, 0.4)', width=1.5, dash='dash'),
        )
        
        # Grid reference lines
        fig.add_shape(
            type='line', x0=4.0, x1=4.0, y0=0.4, y1=5.6,
            line=dict(color='rgba(15, 23, 42, 0.25)', width=1.5, dash='dash'),
        )
        fig.add_shape(
            type='line', x0=0.4, x1=5.6, y0=4.0, y1=4.0,
            line=dict(color='rgba(15, 23, 42, 0.25)', width=1.5, dash='dash'),
        )
        
        fig.add_annotation(
            x=4.75, y=5.35,
            text='<b>VÙNG NGHỊCH LÝ (PARADOX ZONE) (≥4, ≥4)</b>',
            showarrow=False,
            font=dict(size=10, color='#EF4444', family='Inter'),
            bgcolor='rgba(254, 242, 242, 0.95)',
            bordercolor='rgba(239, 68, 68, 0.3)',
            borderwidth=1,
            borderpad=5,
        )

        layout = get_plotly_layout(height=480)
        layout['xaxis']['title'] = 'Mong muốn Tự động hóa (AD) →'
        layout['yaxis']['title'] = '← Quyền tự quyết (HAS)'
        layout['xaxis']['range'] = [0.4, 5.6]
        layout['yaxis']['range'] = [0.4, 5.6]
        layout['xaxis']['dtick'] = 1
        layout['yaxis']['dtick'] = 1
        fig.update_layout(**layout)
        st.plotly_chart(fig, width='stretch')

    st.markdown("""
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-top: 10px; margin-bottom: 10px; font-size: 0.82rem; line-height: 1.5; color: #334155;">
<span style="font-weight: 700; color: #0F172A; text-transform: uppercase; font-size: 0.78rem; display: block; margin-bottom: 8px;">📖 HƯỚNG DẪN ĐỌC BIỂU ĐỒ</span>
<ul style="margin: 0; padding-left: 1.2rem;">
<li><strong>Trục hoành (AD):</strong> Thang Likert 1–5 đo mức độ kỹ sư muốn AI tự động hóa tác vụ.</li>
<li><strong>Trục tung (HAS):</strong> Thang Likert 1–5 đo mức độ kỹ sư đòi giữ quyền kiểm soát và quyền quyết định.</li>
<li><strong>Hiệu ứng Jittering:</strong> Dữ liệu khảo sát là số nguyên rời rạc 1–5 nên sẽ bị chồng chập nếu vẽ trực tiếp. Thêm nhiễu ngẫu nhiên giúp hiển thị mật độ phân bố thực tế mà không thay đổi giá trị trung bình.</li>
<li><strong>Kích thước bong bóng:</strong> Tỷ lệ với mức lương trung bình năm của ngành nghề. Bong bóng lớn hơn ở các ngành lương cao cho thấy xu hướng Nghịch lý tập trung mạnh ở nhóm kỹ sư có trình độ và thu nhập cao.</li>
<li><strong>Vùng nét đứt đỏ:</strong> Vùng Nghịch lý — nơi phản hồi đồng thời thỏa AD ≥ 4.0 và HAS ≥ 4.0.</li>
</ul>
</div>
""", unsafe_allow_html=True)
        
    # ── Chart 1.2: Dual Reasons Bar Chart ──
    st.markdown('<div class="section-header" style="margin-top: 0;">🔍 Động cơ kép của nhóm Nghịch lý</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">So sánh lý do lựa chọn giữa nhóm Nghịch lý và Nhất quán. Nhóm Nghịch lý muốn AI tự động hóa vì nhu cầu mở rộng quy mô và giảm lỗi con người, nhưng vẫn đòi giữ quyền quyết định vì môi trường phát triển phần mềm biến động liên tục — thuật toán tĩnh của AI không thể tự ứng phó nếu thiếu con người.</div>', unsafe_allow_html=True)

    auto_reason_cols = [c for c in df.columns if c.startswith('Reasons for Automation Desire -') and 'Other' not in c]
    human_reason_cols = [c for c in df.columns if c.startswith('Reasons for Human Agency -')]

    paradox_mask = df['is_paradox'] == 1
    consistent_mask = df['is_paradox'] == 0

    # Build reason data
    reasons_data = []
    for col in auto_reason_cols:
        short = col.replace('Reasons for Automation Desire - ', '')
        p_val = df.loc[paradox_mask, col].mean() * 100
        c_val = df.loc[consistent_mask, col].mean() * 100
        reasons_data.append({'Reason': f'🤖 {short}', 'Paradox': p_val, 'Consistent': c_val, 'Type': 'Automation'})

    for col in human_reason_cols:
        short = col.replace('Reasons for Human Agency - ', '')
        p_val = df.loc[paradox_mask, col].mean() * 100
        c_val = df.loc[consistent_mask, col].mean() * 100
        reasons_data.append({'Reason': f'🧑 {short}', 'Paradox': p_val, 'Consistent': c_val, 'Type': 'Human Agency'})

    reason_df = pd.DataFrame(reasons_data)
    reason_df['Gap'] = reason_df['Paradox'] - reason_df['Consistent']
    reason_df = reason_df.sort_values('Gap', ascending=True)

    fig2 = go.Figure()

    def translate_reason(r):
        prefix = '🤖 ' if '🤖' in r else ('🧑 ' if '🧑' in r else '')
        key = r.replace('🤖 ', '').replace('🧑 ', '')
        return f"{prefix}{REASON_MAP.get(key, key)}"

    fig2.add_trace(go.Bar(
        y=reason_df['Reason'].map(translate_reason),
        x=reason_df['Consistent'],
        orientation='h',
        name='Nhất quán (Consistent)',
        marker=dict(color=COLORS['consistent'], opacity=0.7),
        text=reason_df['Consistent'].apply(lambda x: f'{x:.1f}%'),
        textposition='auto',
        textfont=dict(size=9),
    ))

    fig2.add_trace(go.Bar(
        y=reason_df['Reason'].map(translate_reason),
        x=reason_df['Paradox'],
        orientation='h',
        name='Nghịch lý (Paradox)',
        marker=dict(
            color=COLORS['paradox'],
            opacity=0.9,
            line=dict(width=1, color='rgba(255,255,255,0.2)'),
        ),
        text=reason_df['Paradox'].apply(lambda x: f'{x:.1f}%'),
        textposition='auto',
        textfont=dict(size=9),
    ))

    layout2 = get_plotly_layout(height=520)
    layout2['barmode'] = 'group'
    layout2['xaxis']['title'] = 'Tỷ lệ phần trăm người chọn (%)'
    layout2['yaxis']['title'] = ''
    layout2['margin'] = dict(l=220, r=30, t=30, b=60)
    fig2.update_layout(**layout2)
    st.plotly_chart(fig2, width='stretch')

    st.markdown("""
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-top: 10px; margin-bottom: 10px; font-size: 0.82rem; line-height: 1.5; color: #334155;">
<span style="font-weight: 700; color: #0F172A; text-transform: uppercase; font-size: 0.78rem; display: block; margin-bottom: 8px;">📖 HƯỚNG DẪN ĐỌC BIỂU ĐỒ</span>
<ul style="margin: 0; padding-left: 1.2rem;">
<li><strong>Ý nghĩa so sánh:</strong> So sánh tỷ lệ lựa chọn động cơ giữa nhóm Nghịch lý và Nhất quán theo cả hai chiều: muốn tự động hóa (🤖) và muốn giữ quyền kiểm soát (🧑).</li>
<li><strong>Khoảng chênh lệch:</strong> Khoảng cách lớn nhất tập trung ở động cơ ngăn ngừa lỗi con người và tối ưu quy mô ở khía cạnh tự động hóa. Ở khía cạnh giữ quyền kiểm soát, lý do "Hệ thống biến động" ghi nhận sự đồng thuận vượt trội của nhóm Nghịch lý — thể hiện nhận thức rõ ràng rằng AI tối ưu ở tác vụ lặp chính xác, nhưng con người bắt buộc can thiệp khi có thay đổi cấu trúc liên tục.</li>
</ul>
</div>
""", unsafe_allow_html=True)

    # Get top reason values for insight
    auto_reasons_p = reason_df[reason_df['Type'] == 'Automation'].nlargest(3, 'Paradox')
    human_reasons_p = reason_df[reason_df['Type'] == 'Human Agency'].nlargest(2, 'Paradox')
    top_auto_1 = translate_reason(auto_reasons_p.iloc[0]['Reason']).replace('🤖 ', '').replace('🧑 ', '')
    top_auto_2 = translate_reason(auto_reasons_p.iloc[1]['Reason']).replace('🤖 ', '').replace('🧑 ', '')
    top_human_1 = translate_reason(human_reasons_p.iloc[0]['Reason']).replace('🤖 ', '').replace('🧑 ', '')

    if wage_col in df.columns:
        p_wage = paradox[wage_col].mean()
        c_wage = consistent[wage_col].mean()
        wage_diff = ((p_wage - c_wage) / c_wage * 100) if c_wage > 0 else 0
        wage_insight = f' Mức lương trung bình nhóm Nghịch lý (Paradox) (<span class="highlight-cyan">${p_wage/1000:.0f}K</span>) cao hơn nhóm Nhất quán (Consistent) (<span class="highlight-cyan">${c_wage/1000:.0f}K</span>) tới <span class="highlight-green">{wage_diff:+.1f}%</span>.' if wage_diff > 0 else ''
    else:
        wage_insight = ''

    st.markdown(f"""<div class="insight-box">
<strong>📌 PHÁT HIỆN CHÍNH:</strong> Kỹ sư nhóm Nghịch lý chọn lý do tự động hóa vì 
<span class="highlight-red">{top_auto_1} ({auto_reasons_p.iloc[0]['Paradox']:.1f}%)</span> và 
<span class="highlight-red">{top_auto_2} ({auto_reasons_p.iloc[1]['Paradox']:.1f}%)</span> — cao vượt trội so với nhóm Nhất quán. 
Tuy nhiên, họ giữ quyền kiểm soát con người vì môi trường hệ thống quá 
<span class="highlight-green">{top_human_1} ({human_reasons_p.iloc[0]['Paradox']:.1f}%)</span>.{wage_insight}
</div>
<div class="conclusion-box">
<strong>🧪 KẾT LUẬN:</strong> Nhóm Nghịch lý (Paradox) sở hữu tư duy <strong>phân rã tác vụ (task decomposition)</strong> sắc bén: họ bàn giao cho AI các tác vụ lặp có tính chuẩn hóa cao để loại bỏ sai sót của con người, nhưng kiên quyết giữ lại quyền phê duyệt cuối cùng do môi trường công nghệ biến động không ngừng, đòi hỏi chuyên môn thực tế của kỹ sư để tự thiết lập hoặc thích ứng.
</div>
<div class="bridge-box">
<strong>→ KẾT NỐI TIẾP THEO:</strong> Sự phân tách này chuyển trọng tâm sang việc tìm hiểu cơ chế hình thành mong muốn kiểm soát đó. Phần tiếp theo sẽ phân tích sâu hơn ảnh hưởng từ tần suất sử dụng LLM ở các mức độ tác vụ khác nhau.
</div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────
# TAB 2: THE LLM CATALYST
# ──────────────────────────────────────────────────
def render_tab2(df, lr_model, scaler, p_values):
    st.markdown('<div class="section-header" style="margin-top: 0;">🔥 Bản đồ tương quan đa nhiệm của LLM</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc" style="text-align: justify; line-height: 1.5;">Phân tích tương quan Pearson (r) làm rõ sự phân hóa trong hành vi: các tác vụ tra cứu thông tin cơ bản làm tăng kỳ vọng tự động hóa hoàn toàn, trong khi các tác vụ kỹ thuật chuyên sâu (lập trình, xử lý dữ liệu) lại làm tăng nhu cầu kiểm soát chất lượng và tính tự quyết của con người.</div>', unsafe_allow_html=True)

    # Build correlation matrix
    llm_num_cols = [c + '_num' for c in LLM_USAGE_COLS]
    corr_cols = llm_num_cols + ['Automation Desire Rating', 'Human Agency Scale Rating']
    corr_labels = [LLM_SHORT_NAMES[c] for c in LLM_USAGE_COLS] + ['Mong muốn\nTĐH (AD)', 'Quyền tự quyết\n(HAS)']

    corr_data = df[corr_cols].dropna()
    corr_matrix = corr_data.corr()

    # Create heatmap
    fig_hm = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_labels,
        y=corr_labels,
        colorscale=[
            [0.0, '#3B82F6'], # Strong blue (negative correlation)
            [0.3, '#DBEAFE'], # Light blue
            [0.5, '#F8FAFC'], # Off-white (neutral)
            [0.7, '#FCD34D'], # Muted orange
            [1.0, '#EC4899'], # Bright pink/red (positive correlation)
        ],
        zmin=-0.3,
        zmax=0.8,
        text=corr_matrix.values.round(3),
        texttemplate='%{text:.3f}',
        textfont=dict(size=10, family='JetBrains Mono', color='#0F172A'),
        hovertemplate='%{x} × %{y}<br>r = %{z:.3f}<extra></extra>',
        colorbar=dict(
            title=dict(text='Hệ số Pearson (r)', font=dict(size=11, color='#64748B')),
            tickfont=dict(size=10, color='#64748B'),
            len=0.85,
        ),
    ))

    layout_hm = get_plotly_layout(height=540, showlegend=False)
    layout_hm['margin'] = dict(l=150, r=30, t=30, b=150)
    layout_hm['xaxis']['tickangle'] = -35
    layout_hm['xaxis']['tickfont'] = dict(size=10, color='#64748B')
    layout_hm['yaxis']['tickfont'] = dict(size=10, color='#64748B')
    fig_hm.update_layout(**layout_hm)
    st.plotly_chart(fig_hm, width='stretch')

    st.markdown("""
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-top: 10px; margin-bottom: 10px; font-size: 0.82rem; line-height: 1.5; color: #334155;">
<span style="font-weight: 700; color: #0F172A; text-transform: uppercase; font-size: 0.78rem; display: block; margin-bottom: 8px;">📖 HƯỚNG DẪN ĐỌC BIỂU ĐỒ</span>
<ul style="margin: 0; padding-left: 1.2rem;">
<li><strong>Hệ số tương quan Pearson (r):</strong> Đo lường mức độ liên kết tuyến tính giữa tần suất sử dụng LLM cho từng nhóm tác vụ với Mong muốn Tự động hóa (AD) và Quyền tự quyết (HAS). Giá trị nằm từ [-1, 1], trị tuyệt đối càng cao tương quan càng mạnh.</li>
<li><strong>Cách đọc dải màu:</strong> Dải màu chuyển tiếp từ xanh dương (tương quan nghịch) sang trắng (trung tính) và kết thúc ở hồng/đỏ (tương quan thuận mạnh).</li>
<li><strong>Khác biệt bản chất:</strong> Tác vụ tra cứu thông tin (Information Access) chỉ liên kết với nhu cầu tự động hóa (AD) mà không ảnh hưởng đến kiểm soát (HAS). Ngược lại, các tác vụ kỹ thuật nặng (Coding, Data Processing) có tương quan thuận mạnh mẽ với cả hai chỉ số, chứng tỏ kinh nghiệm thực tế với tác vụ kỹ thuật phức tạp làm tăng ý thức kiểm soát chất lượng AI.</li>
</ul>
</div>
""", unsafe_allow_html=True)

    # Key correlations for insight
    auto_corr = corr_matrix.iloc[-2, :9]
    has_corr = corr_matrix.iloc[-1, :9]

    st.markdown(f"""<div class="insight-box">
<strong>📌 PHÁT HIỆN CHÍNH:</strong> Sử dụng LLM cho các tác vụ <span class="highlight-cyan">tra cứu thông tin (Information Access)</span> tương quan thuận rõ nét với mong muốn tự động hóa (<span class="highlight-red">r = {auto_corr.iloc[0]:.3f}</span>), nhưng gần như không ảnh hưởng đến nhu cầu giữ quyền kiểm soát (<span class="highlight-green">r = {has_corr.iloc[0]:.3f}</span>). 
Ngược lại, ứng dụng LLM sâu trong <span class="highlight-cyan">xử lý dữ liệu (Data Processing)</span> lại đồng hành cùng nhu cầu duy trì kiểm soát nghiêm ngặt của kỹ sư (<span class="highlight-green">r = {has_corr.iloc[8]:.3f}</span>).
</div>
<div class="conclusion-box">
<strong>🧪 KẾT LUẬN:</strong> Trải nghiệm LLM ở mức độ sơ cấp (tra cứu, soạn thảo văn bản) dễ tạo ra <strong>tâm lý lạc quan chuyển giao (naive automation)</strong> — xu hướng bàn giao toàn bộ công việc cho AI. Ngược lại, khi tham gia các tác vụ kỹ thuật sâu (xử lý dữ liệu, thiết kế hệ thống), việc thường xuyên đối mặt với các lỗi logic, hallucination và trường hợp biên (edge cases) của LLM đã hình thành phản xạ cảnh giác thực tế, đòi hỏi thiết lập các chốt kiểm soát chất lượng.
</div>
<div class="bridge-box">
<strong>💡 GIẢI PHÁP THỰC TIỄN:</strong> Không áp dụng một chính sách AI cào bằng cho tất cả loại hình công việc. Các tác vụ tra cứu thông tin có thể tối ưu theo hướng tự động hóa nhanh, trong khi tác vụ viết mã, phân tích và xử lý dữ liệu bắt buộc phải đi kèm cơ chế kiểm thử chéo và cổng phê duyệt.
</div>""", unsafe_allow_html=True)
    # ── Chart 2.2: Odds Ratio Plot ──
    st.markdown('<div class="section-header" style="margin-top: 0;">📐 Trọng số tác động qua hồi quy Logistic</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc" style="text-align: justify; line-height: 1.5;">Ước lượng tác động độc lập của từng tác vụ LLM lên xác suất kỹ sư rơi vào nhóm Nghịch lý (Paradox) bằng mô hình hồi quy Logistic đa biến. Tỷ số tỷ lệ chênh (Odds Ratio, eᵝ) phản ánh sự thay đổi cơ hội thuộc nhóm Nghịch lý khi tần suất dùng LLM tăng thêm 1 đơn vị độ lệch chuẩn (SD), đóng vai trò như công cụ phân loại mức độ rủi ro phục vụ thiết kế hệ thống.</div>', unsafe_allow_html=True)

    # Formula box
    st.markdown(r"""
    <div class="formula-box">
        Logit(P(Is_Paradox)) = β₀ + β₁·Info_Access + β₂·Edit + β₃·Idea_Gen + β₄·Communication + β₅·Analysis + β₆·Decision + β₇·Coding + β₈·Sys_Design + β₉·Data_Proc
    </div>
    """, unsafe_allow_html=True)

    # Build odds ratio data
    llm_short = [LLM_SHORT_NAMES[c] for c in LLM_USAGE_COLS]
    coefs = lr_model.coef_[0]
    odds_ratios = np.exp(coefs)

    or_df = pd.DataFrame({
        'Feature': llm_short,
        'Beta': coefs,
        'OR': odds_ratios,
        'p_value': p_values,
    })
    or_df['Significant'] = or_df['p_value'] < 0.05
    or_df['Color'] = or_df.apply(
        lambda r: COLORS['paradox'] if r['OR'] > 1 and r['Significant'] 
        else (COLORS['accent_green'] if r['OR'] <= 1 and r['Significant']
        else COLORS['text_secondary']),
        axis=1
    )
    or_df = or_df.sort_values('OR', ascending=True)

    fig_or = go.Figure()

    fig_or.add_trace(go.Bar(
        y=or_df['Feature'],
        x=or_df['OR'],
        orientation='h',
        marker=dict(
            color=or_df['Color'],
            opacity=0.85,
            line=dict(width=1, color='rgba(255,255,255,0.6)'),
        ),
        text=or_df.apply(
            lambda r: f"OR={r['OR']:.2f} (β={r['Beta']:+.3f}, p={r['p_value']:.3f})" if not np.isnan(r['p_value'])
            else f"OR={r['OR']:.2f} (β={r['Beta']:+.3f})",
            axis=1
        ),
        textposition='outside',
        textfont=dict(size=9, family='JetBrains Mono', color='#0F172A'),
        hovertemplate='%{y}<br>Tỷ số tỷ lệ chênh (Odds Ratio): %{x:.3f}<extra></extra>',
    ))

    # Reference line at OR=1 in slate
    fig_or.add_vline(
        x=1.0,
        line=dict(color='rgba(15, 23, 42, 0.3)', width=1.5, dash='dash'),
        annotation_text='OR = 1 (không có tác động - No Effect)',
        annotation_position='top',
        annotation_font=dict(size=9, color='#64748B'),
    )

    layout_or = get_plotly_layout(height=440, showlegend=False)
    layout_or['xaxis']['title'] = 'Tỷ số tỷ lệ chênh (Odds Ratio, eᵝ)'
    layout_or['yaxis']['title'] = ''
    layout_or['margin'] = dict(l=150, r=160, t=30, b=60)
    layout_or['xaxis']['range'] = [0, max(odds_ratios) * 1.4]
    fig_or.update_layout(**layout_or)
    st.plotly_chart(fig_or, width='stretch')

    st.markdown("""
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-top: 10px; margin-bottom: 10px; font-size: 0.82rem; line-height: 1.5; color: #334155;">
<span style="font-weight: 700; color: #0F172A; text-transform: uppercase; font-size: 0.78rem; display: block; margin-bottom: 8px;">📖 HƯỚNG DẪN ĐỌC BIỂU ĐỒ</span>
<ul style="margin: 0; padding-left: 1.2rem;">
<li><strong>Tỷ số tỷ lệ chênh (Odds Ratio - OR):</strong> Xác định qua eᵝ. Giá trị OR &gt; 1 đại diện cho nhân tố làm tăng khả năng kỹ sư thuộc nhóm Nghịch lý khi tần suất sử dụng LLM tăng lên. OR &lt; 1 thể hiện tác động giảm thiểu.</li>
<li><strong>Ý nghĩa trị số p (p-value):</strong> Khi p &lt; 0.05, mối liên hệ có ý nghĩa thống kê rõ rệt (biểu diễn bằng màu hồng/đỏ nếu thúc đẩy, xanh lá nếu giảm thiểu). Các thanh màu xám là các biến chưa đạt ý nghĩa thống kê.</li>
<li><strong>Nhận diện trọng tâm:</strong> Xác định tác vụ then chốt định hình tư duy của kỹ sư. Việc lập trình (Coding) hoặc phân tích hệ thống bằng LLM có mức ảnh hưởng vượt trội so với các hoạt động tra cứu cơ bản.</li>
</ul>
</div>
""", unsafe_allow_html=True)

    # Find top predictors
    sig_positive = or_df[(or_df['OR'] > 1) & (or_df['Significant'])].sort_values('OR', ascending=False)
    if len(sig_positive) > 0:
        top_pred = sig_positive.iloc[0]
        increase_pct = (top_pred['OR'] - 1) * 100
        st.markdown(f"""<div class="insight-box">
<strong>📌 PHÁT HIỆN CHÍNH:</strong> Tác vụ <span class="highlight-cyan">{top_pred['Feature']}</span> có β = <span class="highlight-red">{top_pred['Beta']:+.3f}</span> (p = {top_pred['p_value']:.3f}), nghĩa là tăng một mức tần suất sử dụng sẽ làm tăng xác suất rơi vào nhóm Nghịch lý lên <span class="highlight-red">{top_pred['OR']:.2f}</span> lần (tăng {increase_pct:.0f}%). Mối giao thoa giữa tiện ích tra cứu thông tin và rủi ro ở tác vụ kỹ thuật nặng là nhân tố cốt lõi hình thành nên tư duy Nghịch lý.
</div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class="bridge-box">
<strong>💡 GIẢI PHÁP THỰC TIỄN:</strong> Hồi quy Logistic giúp chuyển hóa kết quả phân tích thành bộ chỉ báo phân loại rủi ro tác vụ. Dựa vào tần suất tương tác của kỹ sư với LLM ở các tác vụ kỹ thuật, tổ chức có thể thiết lập mức độ giám sát phù hợp: tự động hóa thông thường, đồng hành kiểm thử hay kiểm soát phê duyệt nghiêm ngặt.
</div>""", unsafe_allow_html=True)
    
    # Model performance metrics
    st.markdown('<div style="margin-top: 1.5rem; margin-bottom: 0.5rem; font-weight: 700; font-size: 0.85rem; color: #0F172A; text-transform: uppercase;">Chất lượng mô hình</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    
    acc_val = lr_model.score(scaler.transform(df[[c + '_num' for c in LLM_USAGE_COLS]].dropna()), df.loc[df[[c + '_num' for c in LLM_USAGE_COLS]].dropna().index, 'is_paradox']) * 100
    intercept_val = lr_model.intercept_[0]
    n_sig = or_df['Significant'].sum()
    
    with col_a:
        render_metric_card(f"{acc_val:.1f}%", "Độ chính xác (Accuracy)", "trên tập huấn luyện nội bộ", "green", "🎯")
    with col_b:
        render_metric_card(f"{intercept_val:+.3f}", "Hệ số chặn (Intercept β₀)", "xác suất cơ bản khi không dùng LLM", "purple", "⚙️")
    with col_c:
        render_metric_card(f"{n_sig}/9", "Biến có ý nghĩa (Significant Features)", "số đặc trưng có ý nghĩa thống kê", "orange", "📊")

    st.markdown("""<div class="bridge-box">
<strong>⚠️ LƯU Ý DIỄN GIẢI:</strong> Các chỉ số đánh giá chất lượng mô hình ở đây được xây dựng dựa trên tập dữ liệu WORKBank hiện tại nhằm mục đích phân loại nội bộ và định hình khuyến nghị thiết kế tại Chương 3, không mang tính chất kết luận nhân quả tuyệt đối.
</div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────
# TAB 3: AI AGENT BLUEPRINTS
# ──────────────────────────────────────────────────
def render_tab3(df, lr_model, scaler):
    st.markdown('<div class="section-header" style="margin-top: 0;">🎛️ Trình giả lập chân dung kỹ sư</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Trình giả lập này chuyển hóa xác suất rơi vào nhóm Nghịch lý (Paradox) của kỹ sư thành các khuyến nghị thiết kế thực tế: xác định rõ những tác vụ nào có thể giao cho AI tự vận hành, những tác vụ nào cần cơ chế kiểm thử chéo, và điểm nào bắt buộc phải có sự phê duyệt trực tiếp từ con người.</div>', unsafe_allow_html=True)

    # Slider inputs
    slider_cols = st.columns(3)
    slider_values = {}
    llm_display = [
        ('Information Access', 'Truy cập thông tin (Information Access)', '🔍'),
        ('Edit', 'Chỉnh sửa / viết lại (Edit / Rewrite)', '✏️'),
        ('Idea Generation', 'Gợi mở ý tưởng (Idea Generation)', '💡'),
        ('Communication', 'Giao tiếp (Communication)', '💬'),
        ('Analysis', 'Phân tích (Analysis)', '📊'),
        ('Decision', 'Hỗ trợ ra quyết định (Decision Support)', '⚖️'),
        ('Coding', 'Lập trình (Coding)', '💻'),
        ('System Design', 'Thiết kế hệ thống (System Design)', '🏗️'),
        ('Data Processing', 'Xử lý dữ liệu (Data Processing)', '🗄️'),
    ]

    for idx, (name, label, icon) in enumerate(llm_display):
        with slider_cols[idx % 3]:
            val = st.select_slider(
                f"{icon} {label}",
                options=FREQ_LABELS,
                value=FREQ_DISPLAY_MAP['Weekly'],
                key=f"slider_{name}",
            )
            slider_values[name] = FREQ_MAP[FREQ_LABEL_TO_VALUE[val]]

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Compute prediction
    X_input = np.array([[slider_values[name] for name, _, _ in llm_display]])
    X_scaled = scaler.transform(X_input)
    prob = lr_model.predict_proba(X_scaled)[0][1]
    prob_pct = prob * 100

    # Determine persona
    if prob_pct >= 60:
        persona_name = "🏛️ Nhà kiến trúc chiến lược (Strategic Architect)"
        persona_desc = "Kỹ sư cấp cao, sử dụng LLM ở mức chuyên sâu. Nhóm này cần tác tử AI (AI Agent) có cổng phê duyệt để giữ quyền kiểm soát chiến lược."
        border_color = COLORS['paradox']
        value_color = COLORS['paradox']
        arch_type = "supervisory"
    elif prob_pct >= 30:
        persona_name = "⚙️ Lập trình viên thực hành (Code Practitioner)"
        persona_desc = "Lập trình viên thực thi, cân bằng giữa tốc độ và kiểm soát. Phù hợp với mô hình đồng hành (Co-pilot)."
        border_color = COLORS['accent_orange']
        value_color = COLORS['accent_orange']
        arch_type = "copilot"
    else:
        persona_name = "📋 Nhân sự truyền thống (Legacy Worker)"
        persona_desc = "Người lao động truyền thống, ít tương tác với LLM. Chỉ cần tác tử (Agent) tự động hóa các tác vụ lặp đơn giản."
        border_color = COLORS['accent_green']
        value_color = COLORS['accent_green']
        arch_type = "autonomous"

    # Persona card + Architecture
    col_persona, col_arch = st.columns([1, 2])

    with col_persona:
        st.markdown(f"""<div class="persona-card" style="border-color: {border_color};">
<h3 style="color: {value_color};">{persona_name}</h3>
<div class="prob-display" style="color: {value_color};">{prob_pct:.1f}%</div>
<div class="metric-label" style="margin-bottom: 0.8rem; color: #64748B;">XÁC SUẤT NGHỊCH LÝ (PARADOX)</div>
<p>{persona_desc}</p>
</div>""", unsafe_allow_html=True)

    with col_arch:
        st.markdown('<div class="section-header" style="margin-top: 0;">🔧 Kiến trúc AI Agent khuyến nghị</div>', unsafe_allow_html=True)
        
        if arch_type == "supervisory":
            st.markdown("""<div class="arch-box">
<h4 style="color: #EC4899;">🏛️ Tác tử AI giám sát (Supervisory AI Agent) — Mô hình con người trong vòng lặp (Human-in-the-loop)</h4>
<p style="color: #64748B; font-size: 0.88rem; line-height: 1.6;">
Tác tử AI (AI Agent) tự động xử lý các phần việc hạ tầng như tích hợp/triển khai liên tục (CI/CD), triển khai (deployment), và kiểm thử (testing) ở quy mô lớn, 
nhưng <strong style="color: #EC4899;">bắt buộc dừng lại chờ kỹ sư bấm "Phê duyệt" (Approve)</strong> đối với 
các tác vụ cấu trúc hệ thống, quyết định kiến trúc (architectural decisions), và triển khai môi trường sản xuất (production deployment).
</p>
</div>""", unsafe_allow_html=True)
            st.markdown("""
<div class="flow-diagram">
    <div class="flow-step"><strong>1. Đầu vào</strong>Tác vụ kỹ thuật cần xử lý</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step"><strong>2. AI xử lý</strong>Tự động kiểm thử, CI/CD, chuẩn bị triển khai</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step gate"><strong>3. Human Review Gate</strong>Kỹ sư duyệt quyết định rủi ro cao</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step pass"><strong>4. Production</strong>Chỉ triển khai sau khi được phê duyệt</div>
    <div class="flow-step warn"><strong>Nếu bị từ chối</strong>Kỹ sư sửa thủ công rồi chạy lại quy trình</div>
</div>
""", unsafe_allow_html=True)

        elif arch_type == "copilot":
            st.markdown("""<div class="arch-box">
<h4 style="color: #F97316;">⚙️ Hệ thống đồng hành / hai tác tử (Co-pilot / Dual-Agent System)</h4>
<p style="color: #64748B; font-size: 0.88rem; line-height: 1.6;">
Hệ thống hai tác tử (Agent) song hành: <strong style="color: #F97316;">Tác tử lập trình (Coding Agent)</strong> chuyên viết 
mã nguồn (code) và <strong style="color: #F97316;">Tác tử kiểm định/kiểm thử (QA/Tester Agent)</strong> chuyên chạy kiểm thử tự động 
để bổ trợ, giảm tải áp lực dò lỗi cho lập trình viên.
</p>
</div>""", unsafe_allow_html=True)
            st.markdown("""
<div class="flow-diagram">
    <div class="flow-step"><strong>1. Đầu vào</strong>Yêu cầu lập trình hoặc sửa lỗi</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step"><strong>2. Coding Agent</strong>Sinh mã, đề xuất thay đổi</div>
    <div class="flow-arrow">+</div>
    <div class="flow-step"><strong>3. QA Agent</strong>Chạy kiểm thử và kiểm tra lỗi logic</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step gate"><strong>4. Cross-Validation</strong>Đối chiếu mã với kết quả kiểm thử</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step pass"><strong>5. Developer Review</strong>Con người xác nhận rồi merge/deploy</div>
</div>
""", unsafe_allow_html=True)

        else:
            st.markdown("""<div class="arch-box">
<h4 style="color: #22C55E;">📋 Tác tử tự trị theo lịch (Autonomous / Cron-job Agent)</h4>
<p style="color: #64748B; font-size: 0.88rem; line-height: 1.6;">
AI tự chạy hoàn toàn theo lịch trình cố định cho các tác vụ chuẩn hóa 
(sao lưu CSDL, đồng bộ dữ liệu (data sync), xoay vòng nhật ký (log rotation)), vì nhóm này chỉ có nhu cầu 
tự động hóa các tác vụ lặp đi lặp lại đơn giản.
</p>
</div>""", unsafe_allow_html=True)
            st.markdown("""
<div class="flow-diagram">
    <div class="flow-step"><strong>1. Cron Scheduler</strong>Lịch chạy cố định</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step"><strong>2. Autonomous Agent</strong>Tự thực hiện tác vụ chuẩn hóa</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step"><strong>3. Tác vụ lặp</strong>Backup DB, data sync, log rotation</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step pass"><strong>4. Status Dashboard</strong>Ghi nhận trạng thái thành công/thất bại</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step warn"><strong>5. Alert</strong>Chỉ báo kỹ sư khi có lỗi</div>
</div>
""", unsafe_allow_html=True)

    # Detailed explanation
    st.markdown(r"""
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-top: 15px; margin-bottom: 15px; font-size: 0.82rem; line-height: 1.5; color: #334155;">
<span style="font-weight: 700; color: #0F172A; text-transform: uppercase; font-size: 0.78rem; display: block; margin-bottom: 8px;">📖 HƯỚNG DẪN VÀ CƠ SỞ THIẾT KẾ</span>
<ul style="margin: 0; padding-left: 1.2rem;">
<li><strong>Cơ sở tính toán:</strong> Nhận các giá trị đầu vào từ thanh trượt, chuẩn hóa bằng <em>StandardScaler</em> và chạy qua mô hình hồi quy Logistic để tính xác suất phân lớp.
<div class="formula-box" style="margin: 8px 0 10px 0;">
Logit(P) = β₀ + β₁·Info_Access + ... + β₉·Data_Processing &nbsp; | &nbsp; P(Paradox) = 1 / (1 + exp(-Logit(P)))
</div>
Xác suất này đóng vai trò là căn cứ phân cấp các chốt kiểm soát chất lượng cần thiết.</li>
<li><strong>Nguyên lý thiết kế các mô hình AI Agent:</strong>
    <ul style="margin-top: 4px;">
        <li><strong>Tác tử AI giám sát (Supervisory AI Agent, P &ge; 60%):</strong> Thích hợp cho chân dung <em>Nhà kiến trúc chiến lược (Strategic Architect)</em>. Thiết kế tự động hóa các khâu thực thi nền (CI/CD, kiểm thử cơ bản) nhưng bắt buộc dừng để con người bấm "Phê duyệt" (Human Review Gate) tại các điểm quyết định hệ thống (deploy lên production, cấu trúc CSDL).</li>
        <li><strong>Mô hình đồng hành (Co-pilot / Dual-Agent, 30% &le; P &lt; 60%):</strong> Áp dụng cho <em>Lập trình viên thực hành (Code Practitioner)</em>. Sử dụng hai tác tử bổ trợ lẫn nhau: Coding Agent và QA Agent chạy kiểm tra và đối chiếu mã nguồn chéo (Cross-Validation) trước khi trình lập trình viên duyệt merge.</li>
        <li><strong>Tác tử tự trị (Autonomous Agent, P &lt; 30%):</strong> Dành cho <em>Nhân sự truyền thống (Legacy Worker)</em>. AI tự động thực hiện hoàn toàn các tác vụ lặp có tính chuẩn hóa cao theo lịch cố định (Cron-job), chỉ phát cảnh báo (Alert) cho con người khi có lỗi xảy ra.</li>
    </ul>
</li>
</ul>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Recommendation table
    st.markdown('<div class="section-header" style="margin-top: 0;">📋 Bảng quy chuẩn khuyến nghị kiến trúc</div>', unsafe_allow_html=True)

    rec_data = {
        'Phân khúc P': ['P ≥ 60%', '30% ≤ P < 60%', 'P < 30%'],
        'Chân dung (Persona)': [
            '🏛️ Strategic Architect - Kỹ sư cấp cao, dùng LLM rất sâu',
            '⚙️ Code Practitioner - Lập trình viên thực thi, cân bằng tốc độ và kiểm soát',
            '📋 Legacy Worker - Ít dùng LLM, ưu tiên tác vụ lặp ổn định',
        ],
        'Kiến trúc AI Agent': [
            '🚦 Supervisory Agent có Human Review Gate bắt buộc',
            '🤝 Dual-Agent: Coding Agent + QA Agent kiểm thử chéo',
            '🤖 Autonomous / Cron-job Agent tự chạy theo lịch',
        ],
        'Vấn đề cần cải thiện': [
            'Giảm rủi ro triển khai sai ở tác vụ kiến trúc, dữ liệu, bảo mật',
            'Giảm lỗi logic và lỗi kiểm thử khi AI sinh mã ở tốc độ cao',
            'Giảm tải thao tác lặp nhưng không làm phức tạp quy trình',
        ],
        'KPI kiểm chứng': [
            'Tỷ lệ thay đổi bị chặn trước production; số sự cố rollback',
            'Tỷ lệ test fail được phát hiện trước review; thời gian review',
            'Tỷ lệ job chạy thành công; thời gian xử lý thủ công tiết kiệm',
        ],
    }
    current_row = 0 if prob_pct >= 60 else (1 if prob_pct >= 30 else 2)
    rec_rows = list(zip(
        rec_data['Phân khúc P'],
        rec_data['Chân dung (Persona)'],
        rec_data['Kiến trúc AI Agent'],
        rec_data['Vấn đề cần cải thiện'],
        rec_data['KPI kiểm chứng'],
    ))
    table_rows = []
    for idx, row in enumerate(rec_rows):
        row_class = ' class="selected-row"' if idx == current_row else ''
        cells = ''.join(f'<td style="white-space: normal !important; overflow-wrap: break-word !important; word-break: break-word !important; line-height: 1.45;">{escape(str(cell))}</td>' for cell in row)
        table_rows.append(f'<tr{row_class}>{cells}</tr>')

    st.markdown(f"""
<table class="matrix-table" style="width: 100% !important; table-layout: fixed !important;">
    <colgroup>
        <col style="width: 10%;">
        <col style="width: 23%;">
        <col style="width: 25%;">
        <col style="width: 22%;">
        <col style="width: 20%;">
    </colgroup>
    <thead>
        <tr>
            <th style="white-space: normal !important; overflow-wrap: break-word !important; word-break: break-word !important; font-weight: bold;">P</th>
            <th style="white-space: normal !important; overflow-wrap: break-word !important; word-break: break-word !important; font-weight: bold;">Persona</th>
            <th style="white-space: normal !important; overflow-wrap: break-word !important; word-break: break-word !important; font-weight: bold;">Kiến trúc</th>
            <th style="white-space: normal !important; overflow-wrap: break-word !important; word-break: break-word !important; font-weight: bold;">Cải thiện</th>
            <th style="white-space: normal !important; overflow-wrap: break-word !important; word-break: break-word !important; font-weight: bold;">KPI</th>
        </tr>
    </thead>
    <tbody>
        {''.join(table_rows)}
    </tbody>
</table>
""", unsafe_allow_html=True)
    st.markdown("""<div class="bridge-box">
<strong>💡 GIẢI PHÁP THỰC TIỄN:</strong> Trình mô phỏng giúp đội ngũ kỹ sư lựa chọn mức độ kiểm soát phù hợp trước khi đưa AI Agent vào thực tế, qua đó tối ưu hóa quy trình nghiệp vụ: giảm thiểu lỗi lọt ra sản xuất, tối ưu thời gian review và tăng tính minh bạch chịu trách nhiệm.
</div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────
# NEW TAB: STRATEGIC RECOMMENDATIONS
# ──────────────────────────────────────────────────
def render_recommendations(df):
    st.markdown('<div class="section-header" style="margin-top: 0;">🎯 Khuyến nghị & hành động chiến lược</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc" style="text-align: justify; line-height: 1.5;">Phần này tổng hợp các khuyến nghị hành động thực tế được xây dựng trực tiếp từ các kết quả phân tích định lượng, liên kết hành động cụ thể với các chỉ số đo lường hiệu quả (KPIs).</div>', unsafe_allow_html=True)

    strategy_rows = [
        (
            'Nhóm Paradox muốn AI xử lý tác vụ quy mô lớn nhưng vẫn giữ quyền phán quyết',
            'Thiết kế Human Review Gate cho quyết định rủi ro cao',
            'Tech Lead / Platform Engineering',
            'Giảm rollback, incident sau triển khai, lỗi migration',
        ),
        (
            'Trải nghiệm LLM kỹ thuật sâu làm tăng nhu cầu kiểm định và kiểm soát',
            'Tạo quy trình kiểm thử chéo giữa tác tử sinh mã và tác tử QA',
            'AI Tooling Team / QA Engineering',
            'Tăng lỗi phát hiện trước review, giảm thời gian review',
        ),
        (
            'Xác suất Paradox có thể phân tầng mức kiểm soát cần thiết',
            'Chọn kiến trúc Agent theo rủi ro thay vì áp một mô hình AI chung',
            'Engineering Manager / HR Learning',
            'Tăng adoption có kiểm soát, giảm lỗi AI không truy vết được',
        )
    ]
    
    table_rows = []
    for row in strategy_rows:
        cells = ''.join(f'<td style="white-space: normal !important; overflow-wrap: break-word !important; word-break: break-word !important; line-height: 1.45;">{escape(str(cell))}</td>' for cell in row)
        table_rows.append(f'<tr>{cells}</tr>')

    st.markdown('<div class="impact-table-note"><strong>Ma trận đóng góp:</strong> Bảng tổng hợp thể hiện mối liên hệ chặt chẽ giữa các phát hiện phân tích và phương án hành động thực tế nhằm cải thiện quy trình vận hành.</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
<table class="matrix-table" style="width: 100% !important; table-layout: fixed !important;">
    <colgroup>
        <col style="width: 28%;">
        <col style="width: 28%;">
        <col style="width: 22%;">
        <col style="width: 22%;">
    </colgroup>
    <thead>
        <tr>
            <th style="white-space: normal !important; overflow-wrap: break-word !important; word-break: break-word !important; font-weight: bold;">Phát hiện từ phân tích</th>
            <th style="white-space: normal !important; overflow-wrap: break-word !important; word-break: break-word !important; font-weight: bold;">Giải pháp thực tế</th>
            <th style="white-space: normal !important; overflow-wrap: break-word !important; word-break: break-word !important; font-weight: bold;">Chủ thể thực hiện</th>
            <th style="white-space: normal !important; overflow-wrap: break-word !important; word-break: break-word !important; font-weight: bold;">KPI kiểm chứng</th>
        </tr>
    </thead>
    <tbody>
        {''.join(table_rows)}
    </tbody>
</table>
""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
<div style="background: rgba(255, 255, 255, 0.85); border-top: 4px solid #3B82F6; border-left: 1px solid rgba(226,232,240,0.8); border-right: 1px solid rgba(226,232,240,0.8); border-bottom: 1px solid rgba(226,232,240,0.8); border-radius: 16px; padding: 1.5rem; height: 100%; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.02); transition: all 0.25s ease;">
<div style="font-size: 1.8rem; margin-bottom: 0.8rem;">👔</div>
<h3 style="margin: 0 0 0.8rem 0; font-size: 1.15rem; font-weight: 700; color: #3B82F6;">Quản lý & trưởng nhóm kỹ thuật (Tech Leads)</h3>
<p style="color: #475569; font-size: 0.82rem; line-height: 1.6; margin-bottom: 1rem; text-align: justify;">
<strong>Human-in-the-loop Software Engineering:</strong> Dùng phát hiện Paradox để phân loại tác vụ theo rủi ro. Tác vụ lặp có thể tự động hóa; tác vụ ảnh hưởng kiến trúc, dữ liệu, bảo mật và production phải có cổng phê duyệt rõ trách nhiệm.
</p>
<ul style="color: #64748B; font-size: 0.78rem; line-height: 1.6; padding-left: 1.2rem; margin: 0; text-align: justify;">
<li>Đặt Review Gate bắt buộc cho deployment, database migration, thay đổi hạ tầng và quyền truy cập bảo mật.</li>
<li>Tách nhãn pull request có mã do AI sinh ra để áp dụng checklist kiểm thử, bảo mật và khả năng rollback riêng.</li>
<li>Ghi lại người phê duyệt cuối cùng, lý do phê duyệt và bằng chứng kiểm thử để bảo toàn Human accountability.</li>
</ul>
<div style="margin-top: 1rem; padding-top: 0.8rem; border-top: 1px dashed rgba(226,232,240,0.8); font-size: 0.75rem; color: #3B82F6; font-weight: 600;">
📈 KPI đề xuất (KPIs):<br>
<span style="color: #64748B; font-weight: 400;">• Incident sau triển khai giảm &ge; 30%<br>• 100% thay đổi rủi ro cao có log phê duyệt và rollback plan</span>
</div>
</div>
""", unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
<div style="background: rgba(255, 255, 255, 0.85); border-top: 4px solid #8B5CF6; border-left: 1px solid rgba(226,232,240,0.8); border-right: 1px solid rgba(226,232,240,0.8); border-bottom: 1px solid rgba(226,232,240,0.8); border-radius: 16px; padding: 1.5rem; height: 100%; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.02); transition: all 0.25s ease;">
<div style="font-size: 1.8rem; margin-bottom: 0.8rem;">💻</div>
<h3 style="margin: 0 0 0.8rem 0; font-size: 1.15rem; font-weight: 700; color: #8B5CF6;">Nhà Phát Triển Công Cụ AI</h3>
<p style="color: #475569; font-size: 0.82rem; line-height: 1.6; margin-bottom: 1rem; text-align: justify;">
<strong>Explainable AI Interfaces (XAI) cho kỹ sư:</strong> Vì tác vụ kỹ thuật sâu làm tăng nhu cầu kiểm soát, công cụ AI phải giúp kỹ sư kiểm định đầu ra, không chỉ sinh gợi ý nhanh hơn.
</p>
<ul style="color: #64748B; font-size: 0.78rem; line-height: 1.6; padding-left: 1.2rem; margin: 0; text-align: justify;">
<li>Tích hợp Diff Viewer, test suggestion và risk flag ngay trong IDE để kỹ sư nhìn thấy thay đổi nhỏ nhất do AI tạo ra.</li>
<li>Thêm tác tử QA độc lập để kiểm thử đầu ra của tác tử lập trình trước khi chuyển sang code review của con người.</li>
<li>Lưu decision log: prompt, file bị đổi, test đã chạy, cảnh báo rủi ro và lý do kỹ sư chấp nhận hoặc từ chối.</li>
</ul>
<div style="margin-top: 1rem; padding-top: 0.8rem; border-top: 1px dashed rgba(226,232,240,0.8); font-size: 0.75rem; color: #8B5CF6; font-weight: 600;">
📈 KPI đề xuất (KPIs):<br>
<span style="color: #64748B; font-weight: 400;">• Lỗi được phát hiện trước human review tăng &ge; 25%<br>• Thời gian review mã AI giảm &ge; 20% mà không tăng defect rate</span>
</div>
</div>
""", unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
<div style="background: rgba(255, 255, 255, 0.85); border-top: 4px solid #22C55E; border-left: 1px solid rgba(226,232,240,0.8); border-right: 1px solid rgba(226,232,240,0.8); border-bottom: 1px solid rgba(226,232,240,0.8); border-radius: 16px; padding: 1.5rem; height: 100%; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.02); transition: all 0.25s ease;">
<div style="font-size: 1.8rem; margin-bottom: 0.8rem;">🎓</div>
<h3 style="margin: 0 0 0.8rem 0; font-size: 1.15rem; font-weight: 700; color: #22C55E;">Bộ phận nhân sự (HR) & đào tạo</h3>
<p style="color: #475569; font-size: 0.82rem; line-height: 1.6; margin-bottom: 1rem; text-align: justify;">
<strong>Dịch chuyển năng lực số (Digital Competency Shift):</strong> Nghịch lý cho thấy năng lực tương lai không chỉ là dùng AI, mà là biết khi nào phải nghi ngờ, kiểm thử và chịu trách nhiệm với đầu ra của AI.
</p>
<ul style="color: #64748B; font-size: 0.78rem; line-height: 1.6; padding-left: 1.2rem; margin: 0; text-align: justify;">
<li>Đào tạo kỹ sư về AI risk review: hallucination, edge cases, test coverage, dữ liệu nhạy cảm và rollback.</li>
<li>Đưa năng lực thẩm định AI vào khung năng lực: đọc diff, thiết kế test, đánh giá kiến trúc, giải thích quyết định.</li>
<li>Điều chỉnh OKR từ "tạo nhiều mã hơn" sang "tạo thay đổi ổn định hơn": defect rate, maintainability và incident reduction.</li>
</ul>
<div style="margin-top: 1rem; padding-top: 0.8rem; border-top: 1px dashed rgba(226,232,240,0.8); font-size: 0.75rem; color: #22C55E; font-weight: 600;">
📈 KPI đề xuất (KPIs):<br>
<span style="color: #64748B; font-weight: 400;">• 100% kỹ sư qua bài kiểm tra AI risk review<br>• Defect escape rate giảm &ge; 20% trong nhóm dùng AI thường xuyên</span>
</div>
</div>
""", unsafe_allow_html=True)
        
    render_priority_segments(df)

    st.markdown("""<div class="conclusion-box">
<strong>🧪 KẾT LUẬN CHUNG:</strong> Báo cáo đề xuất một khung chuyển hóa từ dữ liệu khảo sát hành vi kỹ sư sang thiết kế hệ thống AI Agent phân tầng: nhận diện nhóm Nghịch lý, phân tích cơ chế thúc đẩy, lựa chọn mô hình kiến trúc AI phù hợp và liên kết trực tiếp với các chỉ số đo lường hiệu quả (KPIs). Phương pháp này giúp tổ chức triển khai AI có trách nhiệm và tối ưu hóa hiệu quả vận hành thực tế.
</div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────
# PRIORITY SEGMENTS FOR CHAPTER 4
# ──────────────────────────────────────────────────
def render_priority_segments(df):
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header" style="margin-top: 0;">👥 Phân khúc ưu tiên triển khai</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Phân tích chéo tỷ lệ Nghịch lý theo nhóm ngành và số năm kinh nghiệm giúp tổ chức định vị chính xác những phân khúc nên ưu tiên thử nghiệm giải pháp trước khi áp dụng trên quy mô lớn.</div>', unsafe_allow_html=True)
    
    col_group1, col_group2 = st.columns(2)
    
    with col_group1:
        # Paradox rate by Occupation
        occ_paradox = df.groupby(OCC_COL)['is_paradox'].agg(['mean', 'count']).reset_index()
        occ_paradox['mean'] = occ_paradox['mean'] * 100
        occ_paradox = occ_paradox.sort_values('mean', ascending=False).head(8).sort_values('mean', ascending=True)
        occ_paradox['Occupation_display'] = occ_paradox[OCC_COL].map(OCCUPATION_MAP).fillna(occ_paradox[OCC_COL])
        
        fig_occ = go.Figure()
        fig_occ.add_trace(go.Bar(
            y=occ_paradox['Occupation_display'],
            x=occ_paradox['mean'],
            orientation='h',
            marker=dict(color=COLORS['accent_purple'], opacity=0.8),
            text=occ_paradox['mean'].apply(lambda x: f'{x:.1f}%'),
            textposition='auto',
        ))
        
        layout_occ = get_plotly_layout("Top nhóm nghề nên ưu tiên triển khai (%)", height=430, showlegend=False)
        layout_occ['xaxis']['title'] = 'Tỷ lệ Nghịch lý (Paradox) (%)'
        layout_occ['margin'] = dict(l=240, r=30, t=50, b=50)
        fig_occ.update_layout(**layout_occ)
        st.plotly_chart(fig_occ, width='stretch')
        
    with col_group2:
        # Paradox rate by Experience
        exp_paradox = df.groupby('Experience')['is_paradox'].agg(['mean', 'count']).reset_index()
        exp_paradox['mean'] = exp_paradox['mean'] * 100
        
        # Order experience logically
        exp_order = ['Less than 1 year', '1-2 year', '3-5 years', '6-10 years', 'More than 10 years']
        exp_paradox['Experience'] = pd.Categorical(exp_paradox['Experience'], categories=exp_order, ordered=True)
        exp_paradox = exp_paradox.dropna().sort_values('Experience')
        exp_paradox['Experience_display'] = exp_paradox['Experience'].astype(str).map(EXPERIENCE_MAP).fillna(exp_paradox['Experience'].astype(str))
        
        fig_exp = go.Figure()
        fig_exp.add_trace(go.Scatter(
            x=exp_paradox['Experience_display'],
            y=exp_paradox['mean'],
            mode='lines+markers',
            line=dict(color=COLORS['accent_orange'], width=3),
            marker=dict(size=8, color=COLORS['accent_orange']),
            text=exp_paradox['mean'].apply(lambda x: f'{x:.1f}%'),
        ))
        
        layout_exp = get_plotly_layout("Ưu tiên theo kinh nghiệm làm việc (%)", height=300, showlegend=False)
        layout_exp['yaxis']['title'] = 'Tỷ lệ Nghịch lý (Paradox) (%)'
        layout_exp['xaxis']['title'] = ''
        fig_exp.update_layout(**layout_exp)
        st.plotly_chart(fig_exp, width='stretch')

    if not occ_paradox.empty:
        top_occ = occ_paradox.sort_values('mean', ascending=False).iloc[0]
        st.markdown(f"""<div class="bridge-box">
<strong>💡 HƯỚNG DẪN THỰC THI:</strong> Nên ưu tiên thử nghiệm giải pháp tại các phân khúc có tỷ lệ Nghịch lý cao nhất như nhóm <strong>{top_occ['Occupation_display']}</strong> ({top_occ['mean']:.1f}%). Đây là nơi có nhu cầu tự động hóa lớn kết hợp cùng ý thức kiểm soát cao, rất phù hợp để đo lường các chỉ số thành công ban đầu (giảm thiểu sự cố, rút ngắn thời gian review) trước khi triển khai rộng rãi.
</div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────
