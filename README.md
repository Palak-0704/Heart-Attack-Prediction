# Heart Attack Prediction - end-to-end app

`heart.csv` + `analysis_heart.ipynb` -> `final_model_catboost.pkl` (actually an ExtraTrees model) -> FastAPI -> web form.

## Run
```
pip install -r requirements.txt
cd backend && uvicorn main:app --port 8000
```
Open http://localhost:8000. API: `GET /api/health`, `POST /api/predict` (the 13 heart.csv features).
Tests: `cd backend && pytest`.

## Notes
- The notebook did not save its scaler or outlier bounds, so `backend/preprocess.py` rebuilds them from `heart.csv` (IQR clipping + StandardScaler on columns with more than 10 unique values). With this the model scores 100% on the CSV, which suggests it was trained on all of it, so that figure says nothing about generalisation.
- The pickle was made with scikit-learn 1.7.0. Newer versions load it with a warning, so requirements pin 1.7.0.
- For educational use only, not medical advice.
