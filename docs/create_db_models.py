# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Customer(Base):
    """description: Stores customer information, who own pets and avail petsitting services."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)

class DinosaurType(Base):
    """description: Stores different types of dinosaurs available for petsitting."""
    __tablename__ = 'dinosaur_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    species = Column(String, nullable=False)
    average_weight = Column(Float, nullable=True)

class Dinosaur(Base):
    """description: Individual dinosaur pets tied to a specific customer and type."""
    __tablename__ = 'dinosaur'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    last_checkup_date = Column(DateTime, nullable=True, default=datetime.datetime.now)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    type_id = Column(Integer, ForeignKey('dinosaur_type.id'), nullable=False)

class ServiceType(Base):
    """description: Catalog of different services provided for dinosaur pets."""
    __tablename__ = 'service_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=True)

class Sitter(Base):
    """description: Details of assistants trained to take care of dinosaurs."""
    __tablename__ = 'sitter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    expertise = Column(String, nullable=True)

class Appointment(Base):
    """description: Booking details for each petsitting session."""
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_time = Column(DateTime, nullable=False)
    dinosaur_id = Column(Integer, ForeignKey('dinosaur.id'), nullable=False)
    sitter_id = Column(Integer, ForeignKey('sitter.id'), nullable=False)

class ServiceRecord(Base):
    """description: Association between appointments and the services provided."""
    __tablename__ = 'service_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_id = Column(Integer, ForeignKey('appointment.id'), nullable=False)
    service_type_id = Column(Integer, ForeignKey('service_type.id'), nullable=False)

class FoodType(Base):
    """description: Details about different food types provided to dinosaurs."""
    __tablename__ = 'food_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    nutritional_value = Column(Float, nullable=True)

class FoodLog(Base):
    """description: Records feeding information for each dinosaur."""
    __tablename__ = 'food_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dinosaur_id = Column(Integer, ForeignKey('dinosaur.id'), nullable=False)
    food_type_id = Column(Integer, ForeignKey('food_type.id'), nullable=False)
    feeding_date = Column(DateTime, nullable=False)

class HealthCondition(Base):
    """description: Health conditions or issues observed with dinosaurs."""
    __tablename__ = 'health_condition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)

class HealthRecord(Base):
    """description: Logs health conditions associated with a dinosaur."""
    __tablename__ = 'health_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dinosaur_id = Column(Integer, ForeignKey('dinosaur.id'), nullable=False)
    condition_id = Column(Integer, ForeignKey('health_condition.id'), nullable=False)
    observation_date = Column(DateTime, nullable=False)

class Payment(Base):
    """description: Payment details relating to customer bookings and services."""
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)

# SQLite database creation
db_path = "system/genai/temp/model.sqlite"
engine = create_engine(f'sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Sample Data
customer1 = Customer(name="John Doe", email="john@example.com", phone_number="1234567890", address="123 Jurassic Street")
customer2 = Customer(name="Jane Smith", email="jane@example.com", phone_number="0987654321", address="456 Fossil Ave")
session.add_all([customer1, customer2])

dinosaur_type1 = DinosaurType(species="T-Rex", average_weight=10000)
dinosaur_type2 = DinosaurType(species="Velociraptor", average_weight=500)
session.add_all([dinosaur_type1, dinosaur_type2])

dinosaur1 = Dinosaur(name="Rexy", age=5, customer_id=1, type_id=1)
dinosaur2 = Dinosaur(name="Blue", age=3, customer_id=2, type_id=2)
session.add_all([dinosaur1, dinosaur2])

service_type1 = ServiceType(description="Walking", price=50.0)
service_type2 = ServiceType(description="Grooming", price=75.0)
session.add_all([service_type1, service_type2])

sitter1 = Sitter(name="Alan Grant", expertise="Large carnivores")
sitter2 = Sitter(name="Ellie Sattler", expertise="Herbivores")
session.add_all([sitter1, sitter2])

appointment1 = Appointment(date_time=datetime.datetime.now(), dinosaur_id=1, sitter_id=1)
appointment2 = Appointment(date_time=datetime.datetime.now(), dinosaur_id=2, sitter_id=2)
session.add_all([appointment1, appointment2])

service_record1 = ServiceRecord(appointment_id=1, service_type_id=1)
service_record2 = ServiceRecord(appointment_id=2, service_type_id=2)
session.add_all([service_record1, service_record2])

food_type1 = FoodType(name="Herbivore Mix", nutritional_value=100.0)
food_type2 = FoodType(name="Carnivore Delight", nutritional_value=200.0)
session.add_all([food_type1, food_type2])

food_log1 = FoodLog(dinosaur_id=1, food_type_id=2, feeding_date=datetime.datetime.now())
food_log2 = FoodLog(dinosaur_id=2, food_type_id=1, feeding_date=datetime.datetime.now())
session.add_all([food_log1, food_log2])

health_condition1 = HealthCondition(description="Healthy")
health_condition2 = HealthCondition(description="Mild Cold")
session.add_all([health_condition1, health_condition2])

health_record1 = HealthRecord(dinosaur_id=1, condition_id=1, observation_date=datetime.datetime.now())
health_record2 = HealthRecord(dinosaur_id=2, condition_id=2, observation_date=datetime.datetime.now())
session.add_all([health_record1, health_record2])

payment1 = Payment(customer_id=1, amount=150.0, payment_date=datetime.datetime.now())
payment2 = Payment(customer_id=2, amount=125.0, payment_date=datetime.datetime.now())
session.add_all([payment1, payment2])

session.commit()
session.close()
