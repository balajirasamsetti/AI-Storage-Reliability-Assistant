"""src/predictive_model.py
Train a RandomForest classifier to predict At-Risk jobs.
Produces risk_prediction_results.csv in ../data
"""
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

def train_model(input_csv='../data/preprocessed_smf_dataset.csv', out_dir='../data'):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(input_csv)
    label_encoder = LabelEncoder()
    df['RISK_LABEL_ENC'] = label_encoder.fit_transform(df['RISK_LABEL'])
    features = ['IO_USAGE','SPACE_USED','SPACE_ALLOCATED','CPU_TIME','SPACE_UTILIZATION','IO_NORM']
    target = 'RISK_LABEL_ENC'
    X = df[features]
    y = df[target]
    if y.nunique() < 2:
        print('Not enough label variety to train a classifier. Ensure dataset includes At-Risk samples.')
        return None
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:,1]
    results = X_test.copy()
    results['ACTUAL_LABEL'] = y_test.values
    results['PREDICTED_LABEL'] = y_pred
    results['RISK_PROBABILITY'] = y_prob
    results['PREDICTED_STATUS'] = results['PREDICTED_LABEL'].apply(lambda x: 'At-Risk' if x==1 else 'Normal')
    out_path = os.path.join(out_dir, 'risk_prediction_results.csv')
    results.to_csv(out_path, index=False)
    print('Model training complete. Results saved to:', out_path)
    print('\nClassification Report:\n', classification_report(y_test, y_pred))
    print('\nConfusion Matrix:\n', confusion_matrix(y_test, y_pred))
    return out_path

if __name__ == '__main__':
    train_model()
