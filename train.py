import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor, XGBClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, f1_score
import mlflow
import mlflow.sklearn
from preprocess import load_and_preprocess_data

def train_models():
    df = load_and_preprocess_data()
    features = df.drop(columns=['ID', 'Year_Built', 'Price_in_Lakhs', 'Future_Price_5Yrs', 'Good_Investment'])
    cat_cols = features.select_dtypes(include=['object']).columns.tolist()
    num_cols = features.select_dtypes(include=[np.number]).columns.tolist()
    
    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ])
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(features, df['Future_Price_5Yrs'], test_size=0.2, random_state=42)
    reg_pipeline = Pipeline([('preprocessor', preprocessor), ('regressor', XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42))])
    reg_pipeline.fit(X_train_r, y_train_r)
    y_pred_r = reg_pipeline.predict(X_test_r)
    
    rmse = np.sqrt(mean_squared_error(y_test_r, y_pred_r))
    mae = mean_absolute_error(y_test_r, y_pred_r)
    r2 = r2_score(y_test_r, y_pred_r)
    
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(features, df['Good_Investment'], test_size=0.2, random_state=42, stratify=df['Good_Investment'])
    class_pipeline = Pipeline([('preprocessor', preprocessor), ('classifier', XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42))])
    class_pipeline.fit(X_train_c, y_train_c)
    y_pred_c = class_pipeline.predict(X_test_c)
    
    acc = accuracy_score(y_test_c, y_pred_c)
    f1 = f1_score(y_test_c, y_pred_c)
    
    mlflow.set_experiment("Real_Estate_Investment_Advisor")
    with mlflow.start_run(run_name="XGBoost_Pipeline_Run"):
        mlflow.log_metric("reg_rmse", rmse)
        mlflow.log_metric("reg_mae", mae)
        mlflow.log_metric("reg_r2", r2)
        mlflow.log_metric("class_accuracy", acc)
        mlflow.log_metric("class_f1", f1)
        mlflow.sklearn.log_model(reg_pipeline, "regression_model")
        mlflow.sklearn.log_model(class_pipeline, "classification_model")

if __name__ == "__main__":
    train_models()
