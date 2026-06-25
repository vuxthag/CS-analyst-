import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import numpy as np

desires = pd.read_csv('domain_worker_desires.csv')
metadata = pd.read_csv('domain_worker_metadata.csv')
expert = pd.read_csv('expert_rated_technological_capability.csv')
tasks = pd.read_csv('task_statement_with_metadata.csv')
occ_col = 'Occupation (O*NET-SOC Title)'

cs_it = [
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
print(f'CS/IT occupations count: {len(cs_it)}')

d = desires[desires[occ_col].isin(cs_it)]
m = metadata[metadata[occ_col].isin(cs_it)]
merged = d.merge(m, on=['User ID', occ_col], how='left')

uid_count = merged['User ID'].nunique()
print(f'Desires rows (CS/IT): {len(d)}')
print(f'Metadata rows (CS/IT): {len(m)}')
print(f'Merged rows: {len(merged)}')
print(f'Unique users: {uid_count}')
print()

high_auto = merged['Automation Desire Rating'] >= 4
high_has = merged['Human Agency Scale Rating'] >= 4
paradox = merged[high_auto & high_has]
pct = len(paradox)/len(merged)*100
print(f'Paradox count: {len(paradox)} / {len(merged)} ({pct:.2f}%)')
print()

freq_map = {'Never': 0, 'Monthly': 1, 'Weekly': 2, 'Daily': 3}
llm_cols = [c for c in m.columns if 'LLM Usage by Type' in c]
for col in llm_cols:
    merged[col + '_num'] = merged[col].map(freq_map)
    
print('LLM Usage correlations (CS/IT only):')
for col in llm_cols:
    corr_auto = merged[col + '_num'].corr(merged['Automation Desire Rating'])
    corr_has = merged[col + '_num'].corr(merged['Human Agency Scale Rating'])
    short = col.replace('LLM Usage by Type - ', '')
    print(f'  {short}: Auto r={corr_auto:.3f}, HAS r={corr_has:.3f}')
print()

task_wage = tasks[['Task ID', 'Occupation Mean Annual Wage']].drop_duplicates('Task ID')
d_wage = d.merge(task_wage, on='Task ID', how='left')
wage_notna = d_wage['Occupation Mean Annual Wage'].notna().sum()
wage_min = d_wage['Occupation Mean Annual Wage'].min()
wage_max = d_wage['Occupation Mean Annual Wage'].max()
print(f'Rows with wage info: {wage_notna} / {len(d_wage)}')
print(f'Wage range: {wage_min} - {wage_max}')
print()

print('Gender dist (CS/IT):')
print(merged['Gender'].value_counts())
print()
print('Experience dist (CS/IT):')
print(merged['Experience'].value_counts())
print()

# Paradox reasons analysis
auto_reason_cols = [c for c in desires.columns if c.startswith('Reasons for Automation Desire -') and 'Other' not in c]
human_reason_cols = [c for c in desires.columns if c.startswith('Reasons for Human Agency -')]

paradox_mask = (d['Automation Desire Rating'] >= 4) & (d['Human Agency Scale Rating'] >= 4)
consistent_mask = ~paradox_mask

print('Automation Reasons (CS/IT) - Paradox vs Consistent:')
for col in auto_reason_cols:
    p_pct = d.loc[paradox_mask, col].mean() * 100
    c_pct = d.loc[consistent_mask, col].mean() * 100
    short = col.replace('Reasons for Automation Desire - ', '')
    print(f'  {short}: Paradox={p_pct:.1f}%, Consistent={c_pct:.1f}%')

print()
print('Human Agency Reasons (CS/IT) - Paradox vs Consistent:')
for col in human_reason_cols:
    p_pct = d.loc[paradox_mask, col].mean() * 100
    c_pct = d.loc[consistent_mask, col].mean() * 100
    short = col.replace('Reasons for Human Agency - ', '')
    print(f'  {short}: Paradox={p_pct:.1f}%, Consistent={c_pct:.1f}%')

print()
# Logistic regression preview
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

merged['is_paradox'] = ((merged['Automation Desire Rating'] >= 4) & (merged['Human Agency Scale Rating'] >= 4)).astype(int)
llm_num_cols = [col + '_num' for col in llm_cols]
X = merged[llm_num_cols].dropna()
y = merged.loc[X.index, 'is_paradox']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(X_scaled, y)

print('Logistic Regression Coefficients (CS/IT):')
for name, coef in zip(llm_num_cols, lr.coef_[0]):
    odds = np.exp(coef)
    short = name.replace('LLM Usage by Type - ', '').replace('_num', '')
    print(f'  {short}: beta={coef:.3f}, OR={odds:.3f}')
print(f'  Intercept: {lr.intercept_[0]:.3f}')
print(f'  Accuracy: {lr.score(X_scaled, y):.3f}')
