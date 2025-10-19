"""src/data_generator.py
Generate a mock SMF-like dataset (CSV + JSON).
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_mock_smf(num_records=200, out_dir='../data'):
    os.makedirs(out_dir, exist_ok=True)
    start_time = datetime.now() - timedelta(hours=5)
    data = []
    for i in range(num_records):
        job_id = f"JOB{1000 + i}"
        volume_id = f"VOL{random.randint(100, 199)}"
        dataset_name = f"DATASET.{random.choice(['FIN','HR','LOG','PAY','BKP'])}.{random.randint(100,999)}"
        io_usage = np.random.normal(50, 15)
        space_alloc = random.randint(1000, 2000)  # in MB
        space_used = np.random.normal(space_alloc * 0.6, space_alloc * 0.1)
        cpu_time = np.random.normal(2.5, 0.5)
        return_code = 0
        timestamp = start_time + timedelta(minutes=i * 2)

        # Inject anomalies (~10%)
        if random.random() < 0.1:
            anomaly_type = random.choice(['SPACE_FULL','IO_SPIKE','ABEND'])
            if anomaly_type == 'SPACE_FULL':
                space_used = space_alloc * np.random.uniform(0.95, 1.05)
            elif anomaly_type == 'IO_SPIKE':
                io_usage = np.random.normal(150, 20)
            elif anomaly_type == 'ABEND':
                return_code = random.choice([4,8,12,16])

        io_usage = max(0, min(io_usage, 200))
        space_used = max(0, min(space_used, space_alloc * 1.1))
        cpu_time = max(0.1, cpu_time)

        data.append([job_id, volume_id, dataset_name, round(io_usage,2),
                     round(space_used,2), space_alloc, round(cpu_time,2),
                     return_code, timestamp.strftime('%Y-%m-%d %H:%M:%S')])

    columns = ["JOB_ID","VOLUME_ID","DATASET_NAME","IO_USAGE","SPACE_USED",
               "SPACE_ALLOCATED","CPU_TIME","RETURN_CODE","DATE_TIME"]

    df = pd.DataFrame(data, columns=columns)
    csv_path = os.path.join(out_dir, 'mock_smf_dataset.csv')
    json_path = os.path.join(out_dir, 'mock_smf_dataset.json')
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient='records', indent=2)
    print(f"Generated mock SMF dataset: {csv_path} and {json_path}")
    return csv_path, json_path

if __name__ == '__main__':
    generate_mock_smf()
