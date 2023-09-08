# Import necessary libraries and create an SQLite database engine
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Create a SQLAlchemy engine that connects to an SQLite database file named 'restaurant.db'
engine = create_engine('sqlite:///restaurant.db')

# Create a base class for declarative models
Base = declarative_base()

# Create a session maker for interacting with the database using the engine
Session = sessionmaker(bind=engine)
session = Session()

# Define the Restaurant class with SQLAlchemy ORM
class Restaurant(Base):
    __tablename__ = 'restaurants'

    # Define columns for the 'restaurants' table
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    price = Column(Integer)

    # Define relationships with the 'Review' and 'Customer' models
    reviews_relationship = relationship('Review', back_populates='restaurant')
    customers = relationship(
        'Customer',
        secondary='reviews',
        back_populates='restaurants',
        viewonly=True)

    def get_reviews(self):
        return [review.star_rating for review in self.reviews_relationship]
    
    def get_customers(self):
        return [customer.first_name for customer in self.customers]
    
    def fanciest_restaurant(self):
        return max([review.star_rating for review in self.reviews_relationship])
    
    
    def __repr__(self):
        return f'Restaurant(name={self.name}, price={self.price})'
    
    

# Define the Customer class with SQLAlchemy ORM
class Customer(Base):
    __tablename__ = 'customers'

    # Define columns for the 'customers' table
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(10))
    last_name = Column(String(10))

    # Define relationships with the 'Review' and 'Restaurant' models
    reviews_relationship = relationship('Review', back_populates='customer')
    restaurants = relationship(
        'Restaurant',
        secondary='reviews',
        back_populates='customers',
        viewonly=True)

    def get_reviews(self):
        return self.reviews_relationship
    
    def get_restaurants(self):
        return [restaurant.name for restaurant in self.restaurants]
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def favorite_restaurant(self):
        return max(self.get_reviews())
    
    # Add a method to add a review for a restaurant
    def add_review(self, restaurant,rating):
        new_review = Review(restaurant_id=restaurant, customer_id=self.id, star_rating=rating)
        session.add(new_review)
    session.commit() 

    def favorite_restaurant(self):
        return max(self.get_reviews())
    
   
    def __repr__(self):
        return f'Customer(first_name={self.first_name}, last_name={self.last_name})'

# Define the Review class with SQLAlchemy ORM
class Review(Base):
    __tablename__ = 'reviews'

    # Define columns for the 'reviews' table
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    # Define relationships with the 'Restaurant' and 'Customer' models
    restaurant = relationship('Restaurant', back_populates='reviews_relationship')
    customer = relationship('Customer', back_populates='reviews_relationship')

    def customer_name(self):
        return self.customer
    
    def full_review(self):
        return f'{self.restaurant.name} rated by {self.customer.get_full_name()} with {self.star_rating} stars.'
    
    def __repr__(self):
        return f'Review(star_rating={self.star_rating})'
    
# Create the 'restaurants' table in the database   {self.restaurant.name}
Base.metadata.create_all(engine)






customer = session.query(Customer).filter_by(id=1).first()
print(customer.get_reviews())

review = session.query(Review).filter_by(id=1).first()
print(review.customer_name())

add_review = session.query(Customer).filter_by(id=1).first()
print(add_review.get_reviews())

full_review = session.query(Review).filter_by(id=1).first()
print(review.full_review())

customer = session.query(Customer).filter_by(id=1).first()
print(customer.get_full_name())