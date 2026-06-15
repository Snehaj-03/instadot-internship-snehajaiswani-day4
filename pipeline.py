import pandas as pd

# -----------------------------
# Load the dataset
# -----------------------------
df = pd.read_csv("raw_customer_sales.csv")

# -----------------------------
# Clean Order_ID
# -----------------------------
df["Order_ID"] = (
    df["Order_ID"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# -----------------------------
# Clean Order_Date
# -----------------------------
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce",
    dayfirst=True,
    format="mixed"
)

# Fill missing dates with the most frequent date
if df["Order_Date"].notna().any():
    most_common_date = df["Order_Date"].mode()[0]
    df["Order_Date"] = df["Order_Date"].fillna(most_common_date)

# Convert to DD-MM-YYYY format
df["Order_Date"] = df["Order_Date"].dt.strftime("%d-%m-%Y")

# -----------------------------
# Clean Customer_ID
# -----------------------------
df["Customer_ID"] = (
    df["Customer_ID"]
    .fillna("")
    .astype(str)
    .str.strip()
    .replace("", "Unknown")
    .str.upper()
)

# -----------------------------
# Clean Product_Category
# -----------------------------
df["Product_Category"] = (
    df["Product_Category"]
    .fillna("")
    .astype(str)
    .str.strip()
    .replace("", "Unknown")
    .str.replace("_", " ", regex=False)
    .str.title()
)

# Standardize common category names
df["Product_Category"] = df["Product_Category"].replace({
    "Home Kitchen": "Home & Kitchen"
})

# -----------------------------
# Clean Region
# -----------------------------
df["Region"] = (
    df["Region"]
    .fillna("")
    .astype(str)
    .str.strip()
    .replace("", "Unknown")
    .str.title()
)

# -----------------------------
# Clean Quantity
# -----------------------------
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

median_quantity = int(df["Quantity"].median())
df["Quantity"] = df["Quantity"].fillna(median_quantity)

# Replace invalid quantities
df.loc[df["Quantity"] <= 0, "Quantity"] = 1

df["Quantity"] = df["Quantity"].astype(int)

# -----------------------------
# Clean Sales_Amount
# -----------------------------
df["Sales_Amount"] = (
    df["Sales_Amount"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.strip()
)

df["Sales_Amount"] = pd.to_numeric(
    df["Sales_Amount"],
    errors="coerce"
)

median_sales = df["Sales_Amount"].median()
df["Sales_Amount"] = df["Sales_Amount"].fillna(median_sales)

# Convert negative sales to positive
df["Sales_Amount"] = df["Sales_Amount"].abs()

# -----------------------------
# Remove duplicate rows
# -----------------------------
df = df.drop_duplicates()

# -----------------------------
# Save cleaned dataset
# -----------------------------
df.to_csv("cleaned_customer_sales.csv", index=False)

print(" Data cleaning completed successfully!")
print(" Cleaned file saved as: cleaned_customer_sales.csv")