import streamlit as st
import pandas as pd

st.title("Sustainable Construction Practices")

# File uploader
uploaded_file = st.file_uploader("Upload your construction data file", type="csv")

if uploaded_file:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)

    # Show the data
    st.write("Uploaded Data:")
    st.dataframe(data)

    # Basic Analysis
    if 'Material_Type' in data.columns:
        st.subheader("Eco-Friendly Material Usage")
        material_count = data['Material_Type'].value_counts()
        st.bar_chart(material_count)
