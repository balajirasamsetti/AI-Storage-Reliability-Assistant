"""src/alert_dashboard.py
Simple console-based alert dashboard that reads risk_prediction_results.csv
and prints top risky jobs with suggested actions.
"""
import pandas as pd
import os

def suggest_action(row):
    p = row.get('RISK_PROBABILITY', 0)
    if p > 0.9:
        return '⚠️ Immediate Action: Expand dataset space or reroute job.'
    elif p > 0.75:
        return '🟠 High Risk: Review I/O usage and dataset allocation.'
    elif p > 0.5:
        return '🟡 Moderate Risk: Monitor space utilization.'
    else:
        return '🟢 Normal Operation.'

def run_dashboard(input_csv='../data/risk_prediction_results.csv'):
    if not os.path.exists(input_csv):
        print('Prediction results not found. Please run predictive_model.py first.')
        return
    df = pd.read_csv(input_csv)
    df_sorted = df.sort_values(by='RISK_PROBABILITY', ascending=False)
    df_sorted['SUGGESTED_ACTION'] = df_sorted.apply(suggest_action, axis=1)
    print('='*70)
    print('🧠 AI-Powered Storage Reliability Assistant — Alert Dashboard')
    print('='*70)
    top = df_sorted.head(10)
    for idx, row in top.iterrows():
        print(f"\nJOB: {idx}")
        print(f"➡️ Status: {row['PREDICTED_STATUS']} | Risk Probability: {row['RISK_PROBABILITY']:.2f}")
        print(f"📊 Space: {row['SPACE_USED']}/{row['SPACE_ALLOCATED']} MB | IO: {row['IO_USAGE']}")
        print(f"💡 Action: {row['SUGGESTED_ACTION']}")
    print('\nTotal At-Risk Jobs:', (df_sorted['PREDICTED_STATUS'] == 'At-Risk').sum())
    print('='*70)

if __name__ == '__main__':
    run_dashboard()
