import pandas as pd

# 🔹 Load datasets (CSV files)
amazon = pd.read_csv(r"C:/Users/HP/OneDrive/Desktop/Product comparison/amazon price.csv")
flipkart = pd.read_csv(r"C:/Users/HP/OneDrive/Desktop/Product comparison/flipkart price.csv")
myntra = pd.read_csv(r"C:/Users/HP/OneDrive/Desktop/Product comparison/myntra price.csv")

# 🔹 Clean column names (remove spaces, lowercase)
amazon.columns = amazon.columns.str.strip().str.lower()
flipkart.columns = flipkart.columns.str.strip().str.lower()
myntra.columns = myntra.columns.str.strip().str.lower()

# 🔹 Rename price and description columns to match Django model
amazon = amazon.rename(columns={"price": "amazon_price", "description": "amazon_description"})
flipkart = flipkart.rename(columns={"price": "flipkart_price", "description": "flipkart_description"})
myntra = myntra.rename(columns={"price": "myntra_price", "description": "myntra_description"})

# 🔹 Merge datasets on 'name'
df = amazon.merge(flipkart[['name', 'flipkart_price', 'flipkart_description']], on='name', how='outer')
df = df.merge(myntra[['name', 'myntra_price', 'myntra_description']], on='name', how='outer')

# 🔹 Combine descriptions (priority: Amazon → Flipkart → Myntra → 'No description')
df['description'] = df['amazon_description'].combine_first(df['flipkart_description'])
df['description'] = df['description'].combine_first(df['myntra_description'])
df['description'] = df['description'].fillna('No description')

# 🔹 Set combined price (priority: Amazon → Flipkart → Myntra → 0)
df['price'] = df['amazon_price'].fillna(df['flipkart_price']).fillna(df['myntra_price']).fillna(0)

# 🔹 Reorder columns for Django model
df = df[['name', 'description', 'price', 'amazon_price', 'flipkart_price', 'myntra_price']]

# 🔹 Save combined CSV
df.to_csv(r"C:/Users/HP/OneDrive/Desktop/Product comparison/products_combined.csv", index=False)

print("✅ Combined CSV created successfully!")


