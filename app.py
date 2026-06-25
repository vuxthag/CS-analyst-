"""
Báo cáo WORKBank CS/IT - Nghịch lý tự động hóa (Automation Paradox) x
xúc tác mô hình ngôn ngữ lớn (LLM Catalyst).
"""

import sys
import streamlit as st

# Force reload workbank_app submodules to reflect views.py updates immediately
for mod in list(sys.modules.keys()):
    if mod.startswith("workbank_app"):
        del sys.modules[mod]

st.set_page_config(
    page_title="WORKBank CS/IT · Báo cáo Nghịch lý tự động hóa",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

from workbank_app.main import main


if __name__ == '__main__':
    # Reload trigger: 2
    main()
