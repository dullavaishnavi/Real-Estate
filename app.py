import streamlit as st
import pandas as pd

st.set_page_config(page_title="Real Estate Investment Advisor", page_icon="🏡", layout="wide")

st.markdown('<p style="font-size: 2.5rem; color: #1E3A8A; font-weight: 700;">🏡 Real Estate Investment Advisor</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.2rem; color: #4B5563;">Predict property profitability, forecast future prices after 5 years, and explore data-driven market insights.</p>', unsafe_allow_html=True)
st.write("---")

st.sidebar.header("🔍 Property Details Input")
with st.sidebar.form("property_form"):
    property_type = st.selectbox("Property Type", ["Apartment", "Villa", "House"])
    city = st.selectbox("City", ["Mumbai", "Bangalore", "Hyderabad", "Chennai", "Pune", "Gurgaon", "Noida"])
    bhk = st.slider("BHK (Bedrooms)", 1, 5, 2)
    size_sqft = st.number_input("Size (in SqFt)", min_value=300, max_value=10000, value=1200)
    current_price = st.number_input("Current Price (in Lakhs ₹)", min_value=10.0, max_value=1000.0, value=75.0)
    age_property = st.slider("Age of Property (Years)", 0, 30, 5)
    nearby_schools = st.slider("Nearby Schools (Count/Rating)", 1, 10, 5)
    submit_button = st.form_submit_button(label="Analyze Investment 🚀")

if submit_button:
    price_per_sqft = (current_price * 100000) / size_sqft
    city_multiplier = {'Mumbai': 1.09, 'Bangalore': 1.08, 'Hyderabad': 1.085, 'Chennai': 1.075, 'Pune': 1.075, 'Gurgaon': 1.085, 'Noida': 1.07}
    future_price_5yrs = current_price * (city_multiplier.get(city, 1.08) ** 5)
    is_good_investment = (price_per_sqft < 9500) and (bhk >= 2) and (nearby_schools >= 4)
    
    st.subheader("📊 Investment Assessment Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Investment Status")
        if is_good_investment:
            st.success("✅ **Good Investment**\n\nHigh appreciation potential detected.")
        else:
            st.warning("⚠️ **Moderate / High Risk**\n\nPrice per sqft exceeds median benchmark.")
            
    with col2:
        st.markdown("### Price Forecast (5 Yrs)")
        st.metric(label="Estimated Future Price", value=f"₹ {future_price_5yrs:.2f} Lakhs", delta=f"+{(future_price_5yrs - current_price):.2f} Lakhs")
        
    with col3:
        st.markdown("### Valuation Metric")
        st.metric(label="Calculated Price per SqFt", value=f"₹ {price_per_sqft:,.0f} / sqft")

else:
    st.info("👈 Enter property characteristics in the sidebar and click **'Analyze Investment'**.")
