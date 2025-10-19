# AI-Storage-Reliability-Assistant

Prototype to simulate an AI-powered mainframe storage reliability assistant.

## Repository contents
- `data/` : generated mock SMF datasets and processed outputs
- `src/`  : Python scripts
  - `data_generator.py` : generate mock SMF CSV/JSON
  - `data_preprocessing.py` : preprocess and label data
  - `predictive_model.py` : train RandomForest & output predictions
  - `alert_dashboard.py` : console dashboard for alerts
- `notebooks/` : Colab-friendly demo notebook (prototype_demo.ipynb)
- `requirements.txt` : Python dependencies

## Quickstart (Local / Colab)
1. Generate mock data:
   ```bash
   python src/data_generator.py
   ```
2. Preprocess:
   ```bash
   python src/data_preprocessing.py
   ```
3. Train model:
   ```bash
   python src/predictive_model.py
   ```
4. Run dashboard:
   ```bash
   python src/alert_dashboard.py
   ```

## Notes
- This prototype uses **mocked SMF data** for demonstration. For production, replace ingestion with real SMF streams via Zowe or other mainframe integration.
- Streamlit dashboard can be added by adapting `alert_dashboard.py` or using the notebook.

## Author
Balaji Rasamsetti
