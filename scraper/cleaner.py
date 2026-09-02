import re
import pandas as pd

def clean_price(price_str):
    """Extract float values from multiple currency formats ($19.99, £15.00, US $24.50)."""
    if not price_str or not isinstance(price_str, str):
        return 0.0
    
    # Handle ranges like '$10.00 to $20.00' by taking lower bound
    if "to" in price_str.lower():
        price_str = price_str.lower().split("to")[0]
    elif "-" in price_str:
        price_str = price_str.split("-")[0]

    cleaned = re.sub(r"[^\d.]", "", price_str)
    try:
        val = float(cleaned)
        return round(val, 2)
    except ValueError:
        return 0.0

def clean_rating(rating_str):
    """Extract numerical score out of formats like '4.5 out of 5' or raw numbers."""
    if not rating_str:
        return 4.0
    match = re.search(r"(\d+(\.\d+)?)", str(rating_str))
    if match:
        try:
            val = float(match.group(1))
            return min(max(val, 1.0), 5.0)
        except ValueError:
            return 4.0
    return 4.0

def clean_dataset(raw_records):
    """Normalize multi-vendor records into structured Pandas DataFrame."""
    if not raw_records:
        return pd.DataFrame()

    df = pd.DataFrame(raw_records)

    # Process prices & ratings
    df["price"] = df["price"].apply(clean_price)
    df["rating"] = df["rating"].apply(clean_rating)

    # Clean text values
    df["title"] = df["title"].fillna("Unknown Title").astype(str).str.strip()
    df["source"] = df["source"].fillna("Marketplace").astype(str).str.strip()
    df["description"] = df["description"].fillna("N/A").astype(str).str.strip()
    df["product_url"] = df["product_url"].fillna("").astype(str).str.strip()
    df["image_url"] = df["image_url"].fillna("").astype(str).str.strip()

    # Drop items with missing links or blank titles
    df = df[df["title"] != ""]
    df = df[df["product_url"] != ""]

    # Deduplicate based on link or title
    df.drop_duplicates(subset=["product_url"], inplace=True)
    df.drop_duplicates(subset=["title", "source"], inplace=True)

    columns_order = ["source", "title", "price", "rating", "image_url", "product_url", "description"]
    df = df.reindex(columns=columns_order)

    return df