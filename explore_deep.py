import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import numpy as np

desires = pd.read_csv('domain_worker_desires.csv')
metadata = pd.read_csv('domain_worker_metadata.csv')
expert = pd.read_csv('expert_rated_technological_capability.csv')
tasks = pd.read_csv('task_statement_with_metadata.csv')
occ_col = 'Occupation (O*NET-SOC Title)'

merged = desires.merge(metadata, on=['User ID', occ_col], how='left')

# 1. LLM Usage Patterns vs Automation Desire - granular analysis
print("=" * 80)
print("1. LLM USAGE PROFILE ANALYSIS")
print("=" * 80)
llm_cols = [c for c in metadata.columns if 'LLM Usage by Type' in c]
freq_map = {'Never': 0, 'Monthly': 1, 'Weekly': 2, 'Daily': 3}
for col in llm_cols:
    merged[col + '_num'] = merged[col].map(freq_map)

print("\nCorrelation between LLM usage types and automation desire:")
for col in llm_cols:
    corr = merged[col + '_num'].corr(merged['Automation Desire Rating'])
    corr_has = merged[col + '_num'].corr(merged['Human Agency Scale Rating'])
    print(f"  {col.replace('LLM Usage by Type - ', '')}: AutoDesire r={corr:.3f}, HAS r={corr_has:.3f}")

# 2. Inconsistency / Paradox Analysis
print("\n" + "=" * 80)
print("2. PARADOX ANALYSIS - Workers who want automation but high human agency")
print("=" * 80)
high_auto = merged['Automation Desire Rating'] >= 4
high_has = merged['Human Agency Scale Rating'] >= 4
paradox = merged[high_auto & high_has]
print(f"Paradoxical responses (high automation desire + high human agency): {len(paradox)} / {len(merged)} ({len(paradox)/len(merged)*100:.1f}%)")
print(f"Most common occupations in paradox group:")
print(paradox[occ_col].value_counts().head(10))

# 3. Enjoyment-Automation Tension
print("\n" + "=" * 80)
print("3. ENJOYMENT vs AUTOMATION DESIRE")
print("=" * 80)
print("\nMean Automation Desire by Enjoyment Rating:")
print(merged.groupby('Enjoyment Rating')['Automation Desire Rating'].agg(['mean', 'count']))
high_enjoy_high_auto = merged[(merged['Enjoyment Rating'] >= 4) & (merged['Automation Desire Rating'] >= 4)]
print(f"\nHigh enjoyment (>=4) but still want automation (>=4): {len(high_enjoy_high_auto)} ({len(high_enjoy_high_auto)/len(merged)*100:.1f}%)")

# 4. Job Security Anxiety vs Automation Desire
print("\n" + "=" * 80)
print("4. JOB SECURITY vs AUTOMATION DESIRE")
print("=" * 80)
print(merged.groupby('Job Security Rating')['Automation Desire Rating'].agg(['mean', 'count']))

# 5. Demographic Intersectionality  
print("\n" + "=" * 80)
print("5. INTERSECTIONAL ANALYSIS - Gender x Education x Automation Desire")
print("=" * 80)
intersect = merged.groupby(['Gender', 'Education'])['Automation Desire Rating'].agg(['mean', 'count'])
intersect = intersect[intersect['count'] >= 20].sort_values('mean')
print(intersect)

# 6. Income x AI Attitude Interaction
print("\n" + "=" * 80)
print("6. INCOME x AI SUFFERING ATTITUDE -> Automation Desire")
print("=" * 80)
pivot = merged.groupby(['Income', 'AI Suffering Attitude'])['Automation Desire Rating'].mean().unstack()
print(pivot.to_string())

# 7. Core Skill Rating as Moderator
print("\n" + "=" * 80)
print("7. CORE SKILL RATING AS MODERATOR")
print("=" * 80)
merged['Core_Skill_Group'] = pd.cut(merged['Core Skill Rating'], bins=[0, 2, 3, 5], labels=['Low (1-2)', 'Medium (3)', 'High (4-5)'])
print(merged.groupby('Core_Skill_Group')[['Automation Desire Rating', 'Human Agency Scale Rating', 'Enjoyment Rating']].mean())

# 8. Occupation-level wage and automation desire
print("\n" + "=" * 80)
print("8. WAGE vs AUTOMATION DESIRE (Occupation level)")
print("=" * 80)
task_wage = tasks.groupby('Task ID')['Occupation Mean Annual Wage'].first().reset_index()
desire_by_task = desires.groupby('Task ID')['Automation Desire Rating'].mean().reset_index()
desire_by_task.columns = ['Task ID', 'Mean_Auto_Desire']
wage_desire = desire_by_task.merge(task_wage, on='Task ID')
print(f"Correlation between wage and mean automation desire: {wage_desire['Mean_Auto_Desire'].corr(wage_desire['Occupation Mean Annual Wage']):.3f}")

# 9. Reason Combinations Analysis
print("\n" + "=" * 80)
print("9. REASON COMBINATION PATTERNS")
print("=" * 80)
auto_reason_cols = [c for c in desires.columns if c.startswith('Reasons for Automation Desire -') and 'Other' not in c]
desires['n_auto_reasons'] = desires[auto_reason_cols].sum(axis=1)
print(f"Distribution of number of automation reasons selected:")
print(desires['n_auto_reasons'].value_counts().sort_index())
print(f"\nMean auto desire by number of reasons:")
print(desires.groupby('n_auto_reasons')['Automation Desire Rating'].mean())

human_reason_cols = [c for c in desires.columns if c.startswith('Reasons for Human Agency -')]
desires['n_human_reasons'] = desires[human_reason_cols].sum(axis=1)
print(f"\nDistribution of number of human agency reasons selected:")
print(desires['n_human_reasons'].value_counts().sort_index())

# 10. Worker-Expert Gap by Occupation
print("\n" + "=" * 80)
print("10. WORKER-EXPERT HAS GAP BY OCCUPATION")
print("=" * 80)
worker_occ_has = desires.groupby(occ_col)['Human Agency Scale Rating'].mean().reset_index()
worker_occ_has.columns = [occ_col, 'Worker_HAS']
expert_occ_has = expert.groupby(occ_col)['Human Agency Scale Rating'].mean().reset_index()
expert_occ_has.columns = [occ_col, 'Expert_HAS']
occ_gap = worker_occ_has.merge(expert_occ_has, on=occ_col)
occ_gap['Gap'] = occ_gap['Worker_HAS'] - occ_gap['Expert_HAS']
print("Top 10 occupations where workers want MORE human agency than experts think needed:")
print(occ_gap.nlargest(10, 'Gap')[[occ_col, 'Worker_HAS', 'Expert_HAS', 'Gap']].to_string())
print()
print("Top 10 occupations where workers want LESS human agency than experts think needed:")
print(occ_gap.nsmallest(10, 'Gap')[[occ_col, 'Worker_HAS', 'Expert_HAS', 'Gap']].to_string())

# 11. LLM Experience as moderator on Worker-Expert Gap
print("\n" + "=" * 80)
print("11. LLM EXPERIENCE AS MODERATOR")
print("=" * 80)
print("HAS by LLM Familiarity:")
print(merged.groupby('LLM Familiarity')['Human Agency Scale Rating'].mean().sort_values())
print()
print("Automation Desire by LLM Use in Work:")
print(merged.groupby('LLM Use in Work')['Automation Desire Rating'].mean().sort_values())
print()
print("HAS by LLM Use in Work:")
print(merged.groupby('LLM Use in Work')['Human Agency Scale Rating'].mean().sort_values())

# 12. Time-based analysis
print("\n" + "=" * 80)
print("12. TEMPORAL ANALYSIS")
print("=" * 80)
desires['Date_parsed'] = pd.to_datetime(desires['Date'], format='%Y/%m/%d')
desires['Month'] = desires['Date_parsed'].dt.to_period('M')
print("Automation Desire by Month:")
print(desires.groupby('Month')['Automation Desire Rating'].agg(['mean', 'count']))
print()
print("HAS by Month:")
print(desires.groupby('Month')['Human Agency Scale Rating'].agg(['mean', 'count']))

# 13. Task Frequency/Importance vs Automation Desire
print("\n" + "=" * 80)
print("13. TASK IMPORTANCE/FREQUENCY vs AUTOMATION DESIRE")
print("=" * 80)
task_meta = tasks[['Task ID', 'Frequency', 'Importance', 'Relevance', 'Category']].drop_duplicates()
desire_task_meta = desire_by_task.merge(task_meta, on='Task ID')
for col in ['Frequency', 'Importance', 'Relevance', 'Category']:
    corr = desire_task_meta['Mean_Auto_Desire'].corr(desire_task_meta[col])
    print(f"Correlation between {col} and Mean Auto Desire: {corr:.3f}")
