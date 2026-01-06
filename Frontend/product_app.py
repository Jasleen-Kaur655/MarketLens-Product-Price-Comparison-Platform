import requests
import streamlit as st

st.title("Product Price Comparison")

query = st.text_input("Enter product name:")

if query:
    try:
        # make request
        response = requests.get("http://127.0.0.1:8000/api/products/")
        response.raise_for_status()  # raise error if status != 200
        products = response.json()
        
        # filter by name
        filtered = [p for p in products if query.lower() in p['name'].lower()]
        
        if filtered:
            for p in filtered:
                st.write(f"**{p['name']}**")
                st.write(f"Description: {p['description']}")
                st.write(f"Amazon: ₹{p['amazon_price']},   Flipkart: ₹{p['flipkart_price']},   Myntra: ₹{p['myntra_price']}")
                st.write("---")
        else:
            st.write("No products found.")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")




