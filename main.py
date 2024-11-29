import streamlit as st
import pandas as pd
import os
import json

# Load or initialize the storage
DATA_FILE = "price_data.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as file:
        price_data = json.load(file)
else:
    price_data = {}

# Save data function
def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(price_data, file)

# App title
st.title("Price Comparison App")

# Dropdown to select or add a new product
product = st.text_input("Enter a product name to add or search:", value="")
if product:
    if product not in price_data:
        price_data[product] = {}
        save_data()

    st.subheader(f"Price Comparison for: {product}")

    # Display current prices for the product
    data = price_data[product]
    stores = list(data.keys()) + ["Walmart", "Costco", "Longos"]
    unique_stores = sorted(set(stores))  # Avoid duplicates
    store_prices = {store: data.get(store, "") for store in unique_stores}

    # Editable quadrant display
    cols = st.columns(4)
    updated_data = {}
    for i, store in enumerate(store_prices.keys()):
        with cols[i % 4]:  # Distribute stores across 4 columns
            price = st.text_input(f"Price for {store}:", value=store_prices[store])
            if price:
                updated_data[store] = price

    # Update button
    if st.button("Save Changes"):
        price_data[product] = updated_data
        save_data()
        st.success("Prices updated successfully!")

    # Deletion of store entry
    selected_store = st.selectbox("Select a store to delete its entry:", options=[""] + list(updated_data.keys()))
    if st.button("Delete Store Entry"):
        if selected_store in price_data[product]:
            del price_data[product][selected_store]
            save_data()
            st.success(f"Store entry for '{selected_store}' deleted.")

# Show all product entries
st.subheader("All Product Entries")
if price_data:
    for prod, prices in price_data.items():
        st.write(f"**{prod}**")
        for store, price in prices.items():
            st.write(f"- {store}: {price}")
else:
    st.write("No entries yet.")

# Footer
st.write("---")
st.write("Created with ❤️ using Streamlit")
