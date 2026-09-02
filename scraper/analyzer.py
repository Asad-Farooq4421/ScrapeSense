import os
import logging
import matplotlib.pyplot as plt

logger = logging.getLogger("ScraperLogger")

def generate_summary_statistics(df):
    """Compute and print key descriptive statistical metrics."""
    total_products = len(df)
    avg_price = df["price"].mean()
    min_price = df["price"].min()
    max_price = df["price"].max()
    most_common_rating = df["rating"].mode()[0] if not df["rating"].empty else None
    available_count = df["in_stock"].sum()

    print("\n" + "=" * 48)
    print("           EXPLORATORY DATA ANALYSIS")
    print("=" * 48)
    print(f"Total Products Scraped : {total_products}")
    print(f"Average Product Price  : £{avg_price:.2f}")
    print(f"Minimum Product Price  : £{min_price:.2f}")
    print(f"Maximum Product Price  : £{max_price:.2f}")
    print(f"Most Common Rating     : {most_common_rating} Stars")
    print(f"Products in Stock      : {available_count} / {total_products}")
    print("=" * 48)

    print("\nTop 3 Lowest Price Products:")
    lowest_3 = df.nsmallest(3, "price")[["title", "price", "rating"]]
    print(lowest_3.to_string(index=False))

    print("\nTop 3 Highest Rated Products:")
    highest_3 = df[df["rating"] == 5].head(3)[["title", "price", "rating"]]
    print(highest_3.to_string(index=False))
    print("=" * 48 + "\n")

def generate_visualizations(df, output_dir="output"):
    """Generate and export high-resolution EDA visual plots."""
    os.makedirs(output_dir, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # 1. Price Distribution Histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["price"], bins=15, color="#0f172a", edgecolor="#334155", alpha=0.9)
    ax.set_title("Product Price Distribution", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Price (£)", fontsize=10)
    ax.set_ylabel("Frequency", fontsize=10)
    price_path = os.path.join(output_dir, "price_distribution.png")
    fig.tight_layout()
    fig.savefig(price_path, dpi=300)
    plt.close(fig)

    # 2. Rating Distribution Bar Chart
    fig, ax = plt.subplots(figsize=(7, 5))
    rating_counts = df["rating"].value_counts().sort_index()
    ax.bar(rating_counts.index, rating_counts.values, color="#2563eb", edgecolor="#1d4ed8", alpha=0.85)
    ax.set_title("Rating Distribution", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Star Rating", fontsize=10)
    ax.set_ylabel("Number of Books", fontsize=10)
    ax.set_xticks(range(1, 6))
    rating_path = os.path.join(output_dir, "rating_distribution.png")
    fig.tight_layout()
    fig.savefig(rating_path, dpi=300)
    plt.close(fig)

    # 3. Price vs Rating Scatter Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["rating"], df["price"], color="#059669", alpha=0.6, edgecolors="none", s=50)
    ax.set_title("Product Price vs. Star Rating", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Star Rating", fontsize=10)
    ax.set_ylabel("Price (£)", fontsize=10)
    ax.set_xticks(range(1, 6))
    scatter_path = os.path.join(output_dir, "price_vs_rating.png")
    fig.tight_layout()
    fig.savefig(scatter_path, dpi=300)
    plt.close(fig)

    logger.info(f"Visualizations saved to '{output_dir}/'")