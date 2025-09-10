# ML Project: Using machine learning for predictive health management of patients admitted to hospital

This project is an investigation into the applicability of machine learning techniques on hospital data for provision of clinical predictions and decision support. A range of regression and classification algorithms are applied with particular demonstration of the effectiveness of ensemble techniques for weakly correlated variables. 
Five target areas have been researched to develop models for: length of stay, diagnosis, medication, care unit transfers and medical procedures. 

## Project Structure
- `notebooks/` – Jupyter notebooks split into preprocessing, algorithm application, training and final models
- `src/` – helper modules (data loading, features, models)
- `models/` – (ignored or LFS) trained weights
- `data/` – (ignored) raw data
- `requirements.txt` or `environment.yml` – environment spec

## Setup

### Option A: pip/venv
```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
pip install -r requirements.txt
