"""src/data_preprocessing.py
Read mock SMF CSV, clean, normalize and label records as 'Normal' or 'At-Risk'.
Outputs preprocessed_smf_dataset.csv in ../data
"""
import pandas as pd
import numpy as np
import os

def preprocess(input_csv='../data/mock_smf_dataset.csv', out_dir='../data'):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(input_csv)
    df.fillna(0, inplace=True)
    numeric_cols = ["IO_USAGE","SPACE_USED","SPACE_ALLOCATED","CPU_TIME","RETURN_CODE"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
    # Features
    df['SPACE_UTILIZATION'] = df['SPACE_USED'] / df['SPACE_ALLOCATED']
    df['IO_NORM'] = df['IO_USAGE'] / (df['IO_USAGE'].max() if df['IO_USAGE'].max() > 0 else 1)
    # Labeling rules
    conditions = (
        (df['SPACE_UTILIZATION'] > 0.9) |
        (df['IO_NORM'] > 0.85) |
        (df['RETURN_CODE'] > 0)
    )
    df['RISK_LABEL'] = np.where(conditions, 'At-Risk', 'Normal')
    out_path = os.path.join(out_dir, 'preprocessed_smf_dataset.csv')
    df.to_csv(out_path, index=False)
    print(f"Preprocessed data saved to: {out_path}")
    return out_path

if __name__ == '__main__':
    preprocess()
