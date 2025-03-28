import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Load data
    data = pd.read_csv('./data/Chocolate Sales.csv')

    # Drop rows with any NaN values
    data.dropna(inplace=True)

    # Remove spaces from column names
    data.columns = data.columns.str.replace(' ', '', regex=False)

    # Convert the Date column to datetime format
    data['Date'] = pd.to_datetime(data['Date'], format='%d-%b-%y')

    # Handle duplicates
    if data.duplicated().sum():
        data.drop_duplicates(inplace=True)

    # Ensure 'Amount' column is numeric (in case of any non-numeric values)
    data['Amount'] = data['Amount'].replace({'\$': ''}, regex=True)  # Remove the dollar sign
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

    # Extract the month and year to a new column
    data['Month'] = data['Date'].dt.to_period('M')

    # Group by Month and calculate the total profit (Amount) per month
    monthly_profit = data.groupby('Month')['Amount'].sum()

    # Find the most profitable month
    most_profitable_month = monthly_profit.idxmax().strftime('%B %Y')

    # Get the total profit for the best month
    total_best_month_profit = monthly_profit.loc[most_profitable_month]

    top_5_products = data['Product'].value_counts().head(5).to_string(index=True, header=False)

    # Print the results
    print(f"Total boxes shipped: {data['BoxesShipped'].sum()}")
    print(f"Top sales person: {data['SalesPerson'].mode()[0]}")
    print(f"Top 5 chocolate brands: \n{top_5_products}")
    print(f"Most profitable month: {most_profitable_month} - Total profit: {total_best_month_profit}")
    #print(data['Date'].head)

    # Plot histogram of sales (Amount distribution)
    plt.figure(figsize=(10, 6))
    plt.hist(data['Amount'].dropna(), bins=20, edgecolor='black', alpha=0.7)
    plt.xlabel('Sales Amount')
    plt.ylabel('Frequency')
    plt.title('Sales Distribution')
    plt.grid(axis='y', linestyle='dashed', alpha=0.7)
    plt.show()

    # Get the top 5 chocolate brands and their sales counts
    top_5_products = data['Product'].value_counts().head(5)

    # Bar graph of top 5 products
    plt.figure(figsize=(10, 6))
    plt.bar(top_5_products.index, top_5_products.values, color='chocolate', edgecolor='black', alpha=0.9)

    plt.xlabel('Product')
    plt.ylabel('Number of Sales')
    plt.title('Top 5 Best-Selling Chocolate Brands')
    plt.xticks(rotation=45)  # Rotate labels for better visibility
    plt.grid(axis='y', linestyle='dashed', alpha=0.7)

    plt.show()

    # Line graph of monthly sales trends
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_profit.index.astype(str), monthly_profit.values, marker='o', linestyle='-', color='b',
             label="Total Sales")

    plt.xlabel('Month')
    plt.ylabel('Total Sales Amount')
    plt.title('Monthly Sales Trends')
    plt.xticks(rotation=45)  # Rotate labels for better readability
    plt.legend()
    plt.grid(axis='y', linestyle='dashed', alpha=0.7)

    plt.show()


if __name__ == '__main__':
    main()
