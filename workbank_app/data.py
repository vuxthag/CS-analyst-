"""Data loading and modeling helpers for the WORKBank Streamlit report."""

import numpy as np
import pandas as pd
import streamlit as st
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from .constants import CS_IT_OCCUPATIONS, FREQ_MAP, LLM_USAGE_COLS, OCC_COL

@st.cache_data
def load_data():
    desires = pd.read_csv('domain_worker_desires.csv')
    metadata = pd.read_csv('domain_worker_metadata.csv')
    expert = pd.read_csv('expert_rated_technological_capability.csv')
    tasks = pd.read_csv('task_statement_with_metadata.csv')
    return desires, metadata, expert, tasks


@st.cache_data
def prepare_csit_data(desires, metadata, tasks):
    d = desires[desires[OCC_COL].isin(CS_IT_OCCUPATIONS)].copy()
    m = metadata[metadata[OCC_COL].isin(CS_IT_OCCUPATIONS)].copy()
    merged = d.merge(m, on=['User ID', OCC_COL], how='left')

    # Wage info
    task_wage = tasks[['Task ID', 'Occupation Mean Annual Wage']].drop_duplicates('Task ID')
    merged = merged.merge(task_wage, on='Task ID', how='left')

    # Paradox flag
    merged['is_paradox'] = (
        (merged['Automation Desire Rating'] >= 4) &
        (merged['Human Agency Scale Rating'] >= 4)
    ).astype(int)
    merged['Group'] = merged['is_paradox'].map({1: 'Paradox', 0: 'Consistent'})

    # LLM numeric encoding
    for col in LLM_USAGE_COLS:
        merged[col + '_num'] = merged[col].map(FREQ_MAP)

    return merged


@st.cache_resource
def train_logistic_model(merged):
    llm_num_cols = [c + '_num' for c in LLM_USAGE_COLS]
    df = merged[llm_num_cols + ['is_paradox']].dropna()
    X = df[llm_num_cols].values
    y = df['is_paradox'].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    lr = LogisticRegression(random_state=42, max_iter=1000)
    lr.fit(X_scaled, y)

    # p-values via Wald test
    n = X_scaled.shape[0]
    p = X_scaled.shape[1]
    y_pred_proba = lr.predict_proba(X_scaled)[:, 1]
    W = np.diag(y_pred_proba * (1 - y_pred_proba))
    try:
        cov = np.linalg.inv(X_scaled.T @ W @ X_scaled)
        se = np.sqrt(np.diag(cov))
        z_scores = lr.coef_[0] / se
        p_values = 2 * (1 - stats.norm.cdf(np.abs(z_scores)))
    except np.linalg.LinAlgError:
        p_values = np.ones(p) * np.nan

    return lr, scaler, p_values


# ──────────────────────────────────────────────────
