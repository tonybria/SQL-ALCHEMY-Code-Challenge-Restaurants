#!/usr/bin/env python3

# Import necessary libraries
from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import data models from 'model' module
from model import Restaurant, Customer, Review

# Create an instance of the Faker library for generating fake data
fake = Faker()

if __name__ == '__main__':
    # Create a database engine using SQLAlchemy and specify the database file ('restaurant.db' in this case)
    engine = create_engine('sqlite:///restaurant.db')
    
    # Create a session maker for interacting with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # The following lines delete all records from the Restaurant, Customer, and Review tables.
    # This clears the database tables of any existing data.
    session.query(Restaurant).delete()
    session.query(Customer).delete()
    session.query(Review).delete()

    # Create a new instance of Faker to generate fake data
    fake = Faker()

    # Create a list to store generated restaurant objects
    restaurants = []
    # Generate 10 fake restaurant records
    for i in range(10):
        restaurant = Restaurant(
            name=fake.unique.name(),  # Generate a unique fake restaurant name
            price=random.randint(1000, 7500),  # Generate a random price between 1000 and 7500
        )
        # Add the restaurant object to the session and the list
        session.add(restaurant)
        restaurants.append(restaurant)

    # Create a list to store generated customer objects
    customers = []
    # Generate 10 fake customer records
    for i in range(10):
        customer = Customer(
            first_name=fake.first_name(),  # Generate a fake first name
            last_name=fake.last_name(),    # Generate a fake last name
        )
        # Add the customer object to the session and the list
        session.add(customer)
        customers.append(customer)

    # Create a list to store generated review objects
    reviews = []
    # Loop through the list of restaurants and generate random reviews for each restaurant
    for restaurant in restaurants:
        for i in range(random.randint(1, 5)):  # Generate 1 to 5 reviews for each restaurant
            review = Review(
                star_rating=random.randint(1, 10),  # Generate a random star rating between 1 and 10
                restaurant_id=random.randint(1, 10),  # Generate a random restaurant ID between 1 and 10
                customer_id=random.randint(1, 10),    # Generate a random customer ID between 1 and 10
            )
            # Add the review object to the session and the list
            session.add(review)
            reviews.append(review)

    # Use bulk_save_objects to efficiently save all the generated objects (restaurants, customers, reviews) to the database
    session.bulk_save_objects(restaurants)
    session.bulk_save_objects(customers)
    session.bulk_save_objects(reviews)

    # Commit the changes to the database to persist the generated data
    session.commit()