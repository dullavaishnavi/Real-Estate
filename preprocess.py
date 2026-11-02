import pandas as pd
import numpy as np
import os

def load_and_preprocess_data(file_path="data/india_housing_prices.csv"):
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        np.random.seed(42)
        n_samples = 2500
        states = ['Maharashtra', 'Karnataka', 'Telangana', 'Tamil Nadu', 'Delhi NCR']
        cities = {'Maharashtra': ['Mumbai', 'Pune'], 'Karnataka': ['Bangalore'], 
                  'Telangana': ['Hyderabad'], 'Tamil Nadu': ['Chennai'], 'Delhi NCR': ['Gurgaon', 'Noida']}
        localities = ['Andheri', 'Koramangala', 'Gachibowli', 'T. Nagar', 'Whitefield', 'Bandra', 'Hitec City']
        
        data = {
            'ID': [f"PROP_{1000+i}" for i in range(n_samples)],
            'State': np.random.choice(states, n_samples),
            'Property_Type': np.random.choice(['Apartment', 'Villa', 'House'], n_samples, p=[0.6, 0.2, 0.2]),
            'BHK': np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.1, 0.4, 0.3, 0.15, 0.05]),
            'Size_in_SqFt': np.random.randint(500, 4500, n_samples),
            'Year_Built': np.random.randint(2005, 2025, n_samples),
            'Furnished_Status': np.random.choice(['Unfurnished', 'Semi', 'Fully'], n_samples),
            'Floor_No': np.random.randint(0, 30, n_samples),
            'Total_Floors': np.random.randint(1, 35, n_samples),
            'Nearby_Schools': np.random.randint(1, 10, n_samples),
            'Nearby_Hospitals': np.random.randint(1, 6, n_samples),
            'Public_Transport_Accessibility': np.random.choice(['Low', 'Medium', 'High'], n_samples, p=[0.2, 0.5, 0.3]),
            'Parking_Space': np.random.randint(0, 3, n_samples),
            'Facing': np.random.choice(['North', 'South', 'East', 'West'], n_samples),
            'Owner_Type': np.random.choice(['Individual', 'Builder', 'Agent'], n_samples),
            'Availability_Status': np.random.choice(['Available', 'Under Construction', 'Sold'], n_samples, p=[0.7, 0.2, 0.1])
        }
        df = pd.DataFrame(data)
        df['City'] = df['State'].apply(lambda s: np.random.choice(cities[s]))
        df['Locality'] = np.random.choice(localities, n_samples)
        
        base_price_per_sqft = df['City'].map({'Mumbai': 18000, 'Bangalore': 9000, 'Hyderabad': 8500, 'Chennai': 7500, 'Pune': 7000, 'Gurgaon': 12000, 'Noida': 8000})
        df['Price_in_Lakhs'] = (df['Size_in_SqFt'] * base_price_per_sqft * np.random.normal(1.0, 0.15, n_samples)) / 100000
        df.loc[df['Price_in_Lakhs'] < 20, 'Price_in_Lakhs'] = 25
        df.to_csv(file_path, index=False)

    df = pd.read_csv(file_path)
    df.drop_duplicates(inplace=True)
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col].fillna(df[col].median(), inplace=True)
    for col in df.select_dtypes(include=[object]).columns:
        df[col].fillna(df[col].mode()[0], inplace=True)
        
    current_year = 2026
    df['Age_of_Property'] = current_year - df['Year_Built']
    df['Price_per_SqFt'] = (df['Price_in_Lakhs'] * 100000) / df['Size_in_SqFt']
    df['Future_Price_5Yrs'] = df['Price_in_Lakhs'] * ((1 + 0.08) ** 5)
    median_price_sqft = df['Price_per_SqFt'].median()
    df['Good_Investment'] = ((df['Price_per_SqFt'] <= median_price_sqft) & (df['BHK'] >= 2)).astype(int)
    return df
