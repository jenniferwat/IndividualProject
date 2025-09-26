

# ML Project: Using machine learning for predictive health management of patients admitted to hospital



This project is an investigation into the applicability of machine learning techniques on hospital data for provision of clinical predictions and decision support. A range of regression and classification algorithms are applied with particular demonstration of the effectiveness of ensemble techniques for weakly correlated variables. 

Five target areas have been researched to develop models for: length of stay, diagnosis, medication, care unit transfers and medical procedures. 



## Project Structure

\- `notebooks/` – Folder for each target area containing Jupyter notebooks split into preprocessing, algorithm application, training and final models. Feature list csvs have been omitted.

\- `models/` – trained weights, joblib 

\- `data_original/` – information only, raw data not included

\- `requirements.txt` – environment spec

\- `reports/` – Gantt chart and figures, actual report not included

## Setup


### pip/venv

```bash

python -m venv .venv

\# macOS/Linux:

source .venv/bin/activate

\# Windows:

\# .venv\\Scripts\\activate

pip install -r requirements.txt



