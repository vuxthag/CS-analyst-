"""CSS injection for the WORKBank Streamlit report."""

import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global styling overrides */
    .stApp {
        font-family: 'Inter', 'IBM Plex Sans', sans-serif;
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 50%, #EEF2F6 100%);
        background-image: 
            radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.08) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(236, 72, 153, 0.05) 0px, transparent 50%);
        color: #0F172A;
    }

    /* Hide Streamlit chrome so the report reads as a polished dashboard */
    #MainMenu, header [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"], [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Header main */
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: left;
        margin-bottom: 0.1rem;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #64748B;
        text-align: left;
        font-weight: 400;
        margin-top: 0.2rem;
        margin-bottom: 1.5rem;
    }
    
    /* Ambient lights & glow effects */
    .ambient-light {
        position: fixed;
        width: 400px;
        height: 400px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.07) 0%, rgba(59, 130, 246, 0) 70%);
        filter: blur(80px);
        pointer-events: none;
        z-index: -1;
    }
    .ambient-light-1 {
        top: -100px;
        left: -100px;
        animation: float-light-1 20s infinite alternate ease-in-out;
    }
    .ambient-light-2 {
        bottom: -100px;
        right: -100px;
        animation: float-light-2 25s infinite alternate ease-in-out;
    }
    @keyframes float-light-1 {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 30px); }
    }
    @keyframes float-light-2 {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-60px, -40px); }
    }

    /* Metric cards styling */
    .metric-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.02);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        height: 105px;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 25px rgba(139, 92, 246, 0.08);
        border-color: rgba(139, 92, 246, 0.3);
    }
    .metric-content {
        display: flex;
        flex-direction: column;
        text-align: left;
    }
    .metric-label {
        font-size: 0.7rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }
    .metric-subtext {
        font-size: 0.72rem;
        color: #94A3B8;
        margin-top: 4px;
    }
    
    .metric-icon-container {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    .circle-blue { background-color: rgba(59, 130, 246, 0.1); color: #3B82F6; }
    .circle-purple { background-color: rgba(139, 92, 246, 0.1); color: #8B5CF6; }
    .circle-green { background-color: rgba(34, 197, 94, 0.1); color: #22C55E; }
    .circle-orange { background-color: rgba(249, 115, 22, 0.1); color: #F97316; }
    .circle-pink { background-color: rgba(236, 72, 153, 0.1); color: #EC4899; }

    /* Custom cards / panels */
    .chart-card {
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.02);
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
    }
    
    /* Research goal card */
    .research-goal-card {
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 14px;
        padding: 12px 14px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.02);
        backdrop-filter: blur(10px);
        margin-top: 5px;
    }
    
    /* Insight boxes light theme */
    .insight-box {
        background: rgba(241, 245, 249, 0.7);
        border-left: 4px solid #8B5CF6;
        border-radius: 0 12px 12px 0;
        padding: 1.2rem 1.4rem;
        margin: 1.2rem 0;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #334155;
        border-top: 1px solid rgba(226, 232, 240, 0.5);
        border-bottom: 1px solid rgba(226, 232, 240, 0.5);
        border-right: 1px solid rgba(226, 232, 240, 0.5);
    }
    .insight-box strong { color: #8B5CF6; }
    .insight-box .highlight-red, .insight-box .highlight-pink { color: #EC4899; font-weight: 700; }
    .insight-box .highlight-green { color: #22C55E; font-weight: 700; }
    .insight-box .highlight-cyan { color: #3B82F6; font-weight: 700; }
    
    .conclusion-box {
        background: rgba(255, 247, 237, 0.7);
        border-left: 4px solid #F97316;
        border-radius: 0 12px 12px 0;
        padding: 1.2rem 1.4rem;
        margin: 1.2rem 0;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #431407;
        border-top: 1px solid rgba(254, 215, 170, 0.5);
        border-bottom: 1px solid rgba(254, 215, 170, 0.5);
        border-right: 1px solid rgba(254, 215, 170, 0.5);
    }
    .conclusion-box strong { color: #EA580C; }

    .bridge-box {
        background: rgba(239, 246, 255, 0.75);
        border-left: 4px solid #3B82F6;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        font-size: 0.86rem;
        line-height: 1.55;
        color: #1E3A8A;
        border-top: 1px solid rgba(191, 219, 254, 0.7);
        border-bottom: 1px solid rgba(191, 219, 254, 0.7);
        border-right: 1px solid rgba(191, 219, 254, 0.7);
    }

    .bridge-box strong { color: #2563EB; }

    .argument-rail {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin-top: 14px;
    }

    .argument-step {
        background: rgba(248, 250, 252, 0.86);
        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 12px;
        padding: 14px;
        min-height: 132px;
    }

    .argument-step .step-label {
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .argument-step .step-title {
        font-size: 0.88rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 6px;
    }

    .argument-step .step-body {
        font-size: 0.78rem;
        line-height: 1.5;
        color: #475569;
    }

    .evidence-chain {
        background: rgba(255, 255, 255, 0.68);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 12px;
        padding: 16px;
        margin-top: 12px;
        font-size: 0.84rem;
        line-height: 1.55;
        color: #334155;
    }

    .impact-table-note {
        background: rgba(240, 253, 244, 0.72);
        border: 1px solid #BBF7D0;
        border-radius: 12px;
        padding: 14px 16px;
        margin: 14px 0 18px 0;
        font-size: 0.84rem;
        line-height: 1.55;
        color: #166534;
    }

    .matrix-table {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
        margin: 10px 0 16px 0;
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        overflow: hidden;
        font-size: 0.82rem;
    }

    .matrix-table th,
    .matrix-table td {
        border-bottom: 1px solid #E2E8F0;
        padding: 12px 12px;
        text-align: left;
        vertical-align: top;
        white-space: normal;
        overflow-wrap: anywhere;
        line-height: 1.45;
    }

    .matrix-table th {
        background: #F8FAFC;
        color: #64748B;
        font-weight: 800;
        font-size: 0.75rem;
        letter-spacing: 0.02em;
    }

    .matrix-table tr:last-child td {
        border-bottom: none;
    }

    .matrix-table .selected-row td {
        background: rgba(139, 92, 246, 0.10);
        color: #6D28D9;
        font-weight: 650;
    }

    .flow-diagram {
        display: flex;
        flex-wrap: wrap;
        align-items: stretch;
        gap: 10px;
        margin: 12px 0 16px 0;
    }

    .flow-step {
        flex: 1 1 130px;
        min-width: 130px;
        background: rgba(255, 255, 255, 0.86);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 12px;
        color: #334155;
        line-height: 1.35;
        font-size: 0.8rem;
    }

    .flow-step strong {
        display: block;
        color: #0F172A;
        font-size: 0.78rem;
        margin-bottom: 4px;
    }

    .flow-arrow {
        display: flex;
        align-items: center;
        color: #94A3B8;
        font-weight: 800;
        font-size: 1.05rem;
    }

    .flow-step.gate {
        border-color: rgba(236, 72, 153, 0.36);
        background: rgba(253, 242, 248, 0.75);
    }

    .flow-step.pass {
        border-color: rgba(34, 197, 94, 0.36);
        background: rgba(240, 253, 244, 0.72);
    }

    .flow-step.warn {
        border-color: rgba(249, 115, 22, 0.36);
        background: rgba(255, 247, 237, 0.74);
    }

    @media (max-width: 900px) {
        .argument-rail {
            grid-template-columns: 1fr;
        }

        .flow-diagram {
            flex-direction: column;
        }

        .flow-arrow {
            justify-content: center;
            transform: rotate(90deg);
        }
    }

    /* Mint green insight card */
    .insight-mint {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 12px;
        padding: 16px;
        margin-top: 16px;
    }

    /* Section headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 1.5rem;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-desc {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 1.2rem;
    }
    
    /* Divider */
    .section-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(226, 232, 240, 0.8), transparent);
        margin: 2rem 0;
    }
    
    /* Persona card */
    .persona-card {
        background: rgba(255, 255, 255, 0.85);
        border: 2px solid;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.01);
    }
    .persona-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 700;
    }
    .persona-card .prob-display {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1;
        margin: 0.5rem 0;
    }
    .persona-card p {
        color: #64748B;
        font-size: 0.85rem;
        line-height: 1.5;
        margin: 0;
    }
    
    /* Formula display */
    .formula-box {
        background: rgba(248, 250, 252, 0.8);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #3B82F6;
        margin: 0.8rem 0;
        white-space: nowrap;
        overflow-x: auto;
    }

    /* Architecture box */
    .arch-box {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 16px;
        padding: 1.4rem;
        margin-top: 1rem;
    }
    .arch-box h4 {
        margin: 0 0 0.6rem 0;
        font-size: 1.05rem;
    }

    /* Sidebar visual redesign */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(226, 232, 240, 0.8) !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {
        color: #475569;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.72rem;
        letter-spacing: 0.05em;
    }

    /* Compact sidebar checkboxes */
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] {
        padding: 2px 0px !important;
        margin: 0 !important;
        min-height: auto !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label p {
        font-size: 0.78rem !important;
        color: #475569 !important;
        line-height: 1.35 !important;
    }

    /* Scrollable filter container border styling */
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid rgba(226, 232, 240, 0.9) !important;
        border-radius: 12px !important;
        background-color: rgba(248, 250, 252, 0.45) !important;
        padding: 8px 12px !important;
    }
    
    /* Styled navigation radio button list in sidebar */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 6px;
        padding: 8px 0;
    }
    div[role="radiogroup"] label {
        padding: 10px 14px !important;
        margin: 0 !important;
        width: 100%;
        cursor: pointer;
        border-radius: 12px;
        background: transparent;
        transition: all 0.2s ease;
        border: 1px solid transparent !important;
    }
    div[role="radiogroup"] label:hover {
        background-color: rgba(139, 92, 246, 0.05) !important;
        color: #8B5CF6 !important;
    }
    div[role="radiogroup"] label > div:first-child {
        display: none !important; /* Hide circular radio dots */
    }
    div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%) !important;
        color: #8B5CF6 !important;
        border: 1px solid rgba(139, 92, 246, 0.15) !important;
    }
    div[role="radiogroup"] label:has(input:checked) p {
        color: #8B5CF6 !important;
        font-weight: 700;
    }

    /* Customized multiselect tag chips styling */
    span[data-baseweb="tag"] {
        background-color: rgba(139, 92, 246, 0.08) !important;
        color: #8B5CF6 !important;
        border-radius: 20px !important;
        padding: 4px 12px !important;
        border: 1px solid rgba(139, 92, 246, 0.15) !important;
        font-size: 0.78rem !important;
    }
    span[data-baseweb="tag"] svg {
        fill: #8B5CF6 !important;
    }

    /* Custom tabs component styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(10px);
        border-radius: 16px !important;
        padding: 6px !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.02) !important;
        gap: 8px !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        color: #64748B !important;
        border: none !important;
        background-color: transparent !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #8B5CF6 !important;
        background-color: rgba(139, 92, 246, 0.04) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(59, 130, 246, 0.04) 100%) !important;
        color: #8B5CF6 !important;
        border-bottom: 2px solid #8B5CF6 !important;
    }
    
    /* Clean dataframes */
    .stDataFrame {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    /* Hide streamlit default branding/margins */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar static box styling */
    .sidebar-info-box {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 14px;
        padding: 14px;
        margin-top: 15px;
    }
    .sidebar-info-box h4 {
        margin: 0 0 8px 0;
        font-size: 0.75rem;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 700;
    }
    .sidebar-info-box ul {
        margin: 0;
        padding-left: 18px;
        font-size: 0.78rem;
        color: #64748B;
        line-height: 1.6;
    }
    
    /* Custom deploy button link */
    .deploy-button {
        display: inline-block;
        background: #FFFFFF;
        color: #8B5CF6;
        border: 1px solid rgba(139, 92, 246, 0.25);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.05);
    }
    .deploy-button:hover {
        background: rgba(139, 92, 246, 0.04);
        border-color: #8B5CF6;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(139, 92, 246, 0.1);
    }
    </style>
    
    <!-- Inject ambient light blobs and sparkles into the background -->
    <div class="ambient-light ambient-light-1"></div>
    <div class="ambient-light ambient-light-2"></div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────
# CHART HELPERS
# ──────────────────────────────────────────────────
