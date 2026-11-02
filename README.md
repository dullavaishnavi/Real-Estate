# 🏡 Real Estate Investment Advisor: Predicting Property Profitability & Future Value

An end-to-end Machine Learning and Financial Analytics project that assists investors in identifying high-return residential properties, forecasting 5-year future valuations, and exploring regional market dynamics via an interactive Streamlit dashboard.

---

## 🚀 Key Features
1. **Investment Classification:** Predicts whether a property is a **"Good Investment"** based on pricing relative to median benchmarks, size, and school/infrastructure density.
2. **Future Price Regression:** Forecasts property value after 5 years using compound growth rates and structural features.
3. **MLflow Experiment Tracking:** Logs metrics (RMSE, MAE, R², Accuracy, F1-Score) and version-controls trained models.
4. **Interactive Streamlit Web App:** Allows users to input customized property parameters and view real-time predictions, visual comparisons, and feature importance breakdowns.

---

## 🛠️ Tech Stack & Libraries
* **Language:** Python
* **Data Processing & ML:** Pandas, NumPy, Scikit-Learn, XGBoost
* **Experiment Tracking:** MLflow
* **Deployment & UI:** Streamlit, Matplotlib, Seaborn

---

## ⚙️ Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/real-estate-investment-advisor.git
   cd real-estate-investment-advisor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run src/app.py
   ```
