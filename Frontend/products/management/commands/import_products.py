import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Product
from tqdm import tqdm  # progress bar library

def clean_price(value):
    """Convert price strings like '₹1,099' into float 1099.0"""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return value
    return float(str(value).replace("₹", "").replace(",", "").strip())

class Command(BaseCommand):
    help = "Import products from CSV efficiently"

    def handle(self, *args, **kwargs):
        # Read CSV
        df = pd.read_csv(
            r"C:\Users\HP\OneDrive\Desktop\Product comparison\products_combined.csv",
            low_memory=False
        )

        # Optional: clear old data (be careful in production!)
        Product.objects.all().delete()

        BATCH_SIZE = 1000  # Insert in batches of 1000
        batch = []

        # ✅ Use correct column names from CSV
        for row in tqdm(df.itertuples(index=False), total=len(df), desc="📦 Importing products"):
            batch.append(Product(
                name=row.product,          # <-- use 'product' if your CSV header is 'product'
                description=row.description,
                amazon_price=clean_price(row.amazon_price),
                flipkart_price=clean_price(row.flipkart_price),
                myntra_price=clean_price(row.myntra_price),
            ))

            # Insert batch
            if len(batch) >= BATCH_SIZE:
                Product.objects.bulk_create(batch)
                batch = []

        # Insert remaining products
        if batch:
            Product.objects.bulk_create(batch)

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {len(df)} products successfully!"))



