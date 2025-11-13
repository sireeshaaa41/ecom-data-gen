"""
Synthetic E-commerce Data Generator using Faker
Generates realistic e-commerce data including customers, products, orders, and reviews.
"""

from faker import Faker
import random
import csv
import json
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd

# Initialize Faker
fake = Faker()

# E-commerce categories
CATEGORIES = [
    "Electronics", "Clothing", "Home & Garden", "Books", "Sports & Outdoors",
    "Toys & Games", "Health & Beauty", "Automotive", "Food & Beverages", "Pet Supplies"
]

# Order statuses
ORDER_STATUSES = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]

# Payment methods
PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash on Delivery"]


class EcommerceDataGenerator:
    """Generate synthetic e-commerce data"""
    
    def __init__(self, seed: int = None):
        """Initialize the generator with optional seed for reproducibility"""
        if seed:
            Faker.seed(seed)
            random.seed(seed)
        self.customers = []
        self.products = []
        self.orders = []
        self.order_items = []
        self.reviews = []
    
    def generate_customers(self, count: int = 100) -> List[Dict]:
        """Generate customer data"""
        print(f"Generating {count} customers...")
        customers = []
        
        for i in range(1, count + 1):
            customer = {
                "customer_id": i,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "address": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "zip_code": fake.zipcode(),
                "country": fake.country(),
                "date_joined": fake.date_between(start_date="-2y", end_date="today").isoformat(),
            }
            customers.append(customer)
        
        self.customers = customers
        return customers
    
    def generate_products(self, count: int = 50) -> List[Dict]:
        """Generate product data"""
        print(f"Generating {count} products...")
        products = []
        
        product_names = {
            "Electronics": ["Smartphone", "Laptop", "Tablet", "Headphones", "Smartwatch", "Camera", "Speaker"],
            "Clothing": ["T-Shirt", "Jeans", "Dress", "Jacket", "Shoes", "Hat", "Sunglasses"],
            "Home & Garden": ["Lamp", "Chair", "Table", "Plant Pot", "Garden Tool", "Cushion", "Curtain"],
            "Books": ["Novel", "Textbook", "Cookbook", "Biography", "Mystery", "Science Fiction", "Fantasy"],
            "Sports & Outdoors": ["Bicycle", "Tent", "Running Shoes", "Yoga Mat", "Dumbbells", "Basketball", "Tennis Racket"],
            "Toys & Games": ["Board Game", "Action Figure", "Puzzle", "Doll", "RC Car", "LEGO Set", "Card Game"],
            "Health & Beauty": ["Shampoo", "Perfume", "Skincare Set", "Makeup Kit", "Vitamins", "Hair Dryer", "Face Mask"],
            "Automotive": ["Car Battery", "Tire", "Oil Filter", "Car Cover", "Floor Mat", "Phone Mount", "Dash Cam"],
            "Food & Beverages": ["Coffee", "Tea", "Chocolate", "Snacks", "Wine", "Juice", "Cereal"],
            "Pet Supplies": ["Dog Food", "Cat Litter", "Pet Toy", "Leash", "Pet Bed", "Pet Bowl", "Pet Grooming Kit"]
        }
        
        for i in range(1, count + 1):
            category = random.choice(CATEGORIES)
            product_type = random.choice(product_names.get(category, ["Product"]))
            
            product = {
                "product_id": i,
                "product_name": f"{fake.company()} {product_type}",
                "description": fake.text(max_nb_chars=200),
                "category": category,
                "price": round(random.uniform(10.0, 500.0), 2),
                "cost": round(random.uniform(5.0, 250.0), 2),
                "sku": fake.bothify(text="SKU-####-????", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                "stock_quantity": random.randint(0, 1000),
                "rating": round(random.uniform(3.0, 5.0), 1),
                "created_date": fake.date_between(start_date="-1y", end_date="today").isoformat(),
            }
            products.append(product)
        
        self.products = products
        return products
    
    def generate_orders(self, count: int = 200) -> List[Dict]:
        """Generate order data"""
        if not self.customers:
            raise ValueError("Customers must be generated first")
        
        print(f"Generating {count} orders...")
        orders = []
        
        for i in range(1, count + 1):
            customer = random.choice(self.customers)
            order_date = fake.date_between(
                start_date=customer["date_joined"],
                end_date="today"
            )
            
            order = {
                "order_id": i,
                "customer_id": customer["customer_id"],
                "order_date": order_date.isoformat(),
                "status": random.choice(ORDER_STATUSES),
                "payment_method": random.choice(PAYMENT_METHODS),
                "shipping_address": customer["address"],
                "shipping_city": customer["city"],
                "shipping_state": customer["state"],
                "shipping_zip": customer["zip_code"],
                "shipping_cost": round(random.uniform(5.0, 25.0), 2),
            }
            orders.append(order)
        
        self.orders = orders
        return orders
    
    def generate_order_items(self) -> List[Dict]:
        """Generate order items for each order"""
        if not self.orders or not self.products:
            raise ValueError("Orders and products must be generated first")
        
        print("Generating order items...")
        order_items = []
        item_id = 1
        
        for order in self.orders:
            # Each order has 1-5 items
            num_items = random.randint(1, 5)
            selected_products = random.sample(self.products, min(num_items, len(self.products)))
            
            for product in selected_products:
                quantity = random.randint(1, 5)
                # Price might be different from current product price (sales, discounts)
                item_price = round(product["price"] * random.uniform(0.8, 1.2), 2)
                
                order_item = {
                    "item_id": item_id,
                    "order_id": order["order_id"],
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "unit_price": item_price,
                    "total_price": round(quantity * item_price, 2),
                }
                order_items.append(order_item)
                item_id += 1
        
        self.order_items = order_items
        return order_items
    
    def generate_reviews(self, count: int = 150) -> List[Dict]:
        """Generate product reviews"""
        if not self.customers or not self.products:
            raise ValueError("Customers and products must be generated first")
        
        print(f"Generating {count} reviews...")
        reviews = []
        
        # Get products that have been ordered
        ordered_products = set(item["product_id"] for item in self.order_items)
        
        for i in range(1, count + 1):
            product = random.choice(self.products)
            customer = random.choice(self.customers)
            
            # Review date should be after product creation and customer join date
            start_date = max(
                datetime.fromisoformat(product["created_date"]),
                datetime.fromisoformat(customer["date_joined"])
            )
            review_date = fake.date_between(
                start_date=start_date,
                end_date="today"
            )
            
            review = {
                "review_id": i,
                "product_id": product["product_id"],
                "customer_id": customer["customer_id"],
                "rating": random.randint(1, 5),
                "review_text": fake.text(max_nb_chars=300),
                "review_date": review_date.isoformat(),
                "verified_purchase": product["product_id"] in ordered_products,
            }
            reviews.append(review)
        
        self.reviews = reviews
        return reviews
    
    def save_to_csv(self, output_dir: str = "output"):
        """Save all data to CSV files"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nSaving data to CSV files in '{output_dir}' directory...")
        
        datasets = {
            "customers": self.customers,
            "products": self.products,
            "orders": self.orders,
            "order_items": self.order_items,
            "reviews": self.reviews,
        }
        
        for name, data in datasets.items():
            if data:
                filepath = os.path.join(output_dir, f"{name}.csv")
                df = pd.DataFrame(data)
                df.to_csv(filepath, index=False)
                print(f"  ✓ Saved {len(data)} records to {filepath}")
    
    def save_to_json(self, output_dir: str = "output"):
        """Save all data to JSON files"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nSaving data to JSON files in '{output_dir}' directory...")
        
        datasets = {
            "customers": self.customers,
            "products": self.products,
            "orders": self.orders,
            "order_items": self.order_items,
            "reviews": self.reviews,
        }
        
        for name, data in datasets.items():
            if data:
                filepath = os.path.join(output_dir, f"{name}.json")
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"  ✓ Saved {len(data)} records to {filepath}")
    
    def get_summary(self) -> Dict:
        """Get a summary of generated data"""
        return {
            "customers": len(self.customers),
            "products": len(self.products),
            "orders": len(self.orders),
            "order_items": len(self.order_items),
            "reviews": len(self.reviews),
            "total_revenue": sum(item["total_price"] for item in self.order_items),
        }


def main():
    """Main function to generate e-commerce data"""
    print("=" * 60)
    print("E-commerce Synthetic Data Generator")
    print("=" * 60)
    
    # Initialize generator
    generator = EcommerceDataGenerator(seed=42)  # Seed for reproducibility
    
    # Generate data
    generator.generate_customers(count=100)
    generator.generate_products(count=50)
    generator.generate_orders(count=200)
    generator.generate_order_items()
    generator.generate_reviews(count=150)
    
    # Save to files
    generator.save_to_csv()
    generator.save_to_json()
    
    # Print summary
    print("\n" + "=" * 60)
    print("Data Generation Summary")
    print("=" * 60)
    summary = generator.get_summary()
    for key, value in summary.items():
        if key == "total_revenue":
            print(f"{key.replace('_', ' ').title()}: ${value:,.2f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    print("=" * 60)


if __name__ == "__main__":
    main()

