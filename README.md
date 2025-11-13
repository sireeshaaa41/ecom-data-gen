# E-commerce Synthetic Data Generator

A Python tool to generate realistic synthetic e-commerce data using the Faker library.

## Features

- **Customers**: Generate customer profiles with names, emails, addresses, and contact information
- **Products**: Create products across 10 different categories with prices, SKUs, and descriptions
- **Orders**: Generate orders with various statuses and payment methods
- **Order Items**: Create order line items with quantities and prices
- **Reviews**: Generate product reviews with ratings and text

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script to generate default amounts of data:

```bash
python generate_ecommerce_data.py
```

This will generate:
- 100 customers
- 50 products
- 200 orders
- Order items for each order
- 150 reviews

### Custom Usage

You can modify the script to generate custom amounts of data:

```python
from generate_ecommerce_data import EcommerceDataGenerator

# Initialize generator
generator = EcommerceDataGenerator(seed=42)

# Generate custom amounts
generator.generate_customers(count=500)
generator.generate_products(count=200)
generator.generate_orders(count=1000)
generator.generate_order_items()
generator.generate_reviews(count=500)

# Save to files
generator.save_to_csv(output_dir="my_data")
generator.save_to_json(output_dir="my_data")

# Get summary
summary = generator.get_summary()
print(summary)
```

## Output

The script generates data in two formats:

1. **CSV files** (in `output/` directory):
   - `customers.csv`
   - `products.csv`
   - `orders.csv`
   - `order_items.csv`
   - `reviews.csv`

2. **JSON files** (in `output/` directory):
   - `customers.json`
   - `products.json`
   - `orders.json`
   - `order_items.json`
   - `reviews.json`

## Data Schema

### Customers
- customer_id, first_name, last_name, email, phone, address, city, state, zip_code, country, date_joined

### Products
- product_id, product_name, description, category, price, cost, sku, stock_quantity, rating, created_date

### Orders
- order_id, customer_id, order_date, status, payment_method, shipping_address, shipping_city, shipping_state, shipping_zip, shipping_cost

### Order Items
- item_id, order_id, product_id, quantity, unit_price, total_price

### Reviews
- review_id, product_id, customer_id, rating, review_text, review_date, verified_purchase

## Customization

You can customize the generator by modifying:
- `CATEGORIES`: Product categories
- `ORDER_STATUSES`: Order status options
- `PAYMENT_METHODS`: Payment method options
- Product names dictionary in `generate_products()` method

## License

This project is open source and available for use.

