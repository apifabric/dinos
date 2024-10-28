# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 28, 2024 16:02:11
# Database: sqlite:////tmp/tmp.6PvL9mhPDJ/dinos/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Customer(SAFRSBaseX, Base):
    """
    description: Stores customer information, who own pets and avail petsitting services.
    """
    __tablename__ = 'customer'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone_number = Column(String)
    address = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    DinosaurList : Mapped[List["Dinosaur"]] = relationship(back_populates="customer")
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="customer")



class DinosaurType(SAFRSBaseX, Base):
    """
    description: Stores different types of dinosaurs available for petsitting.
    """
    __tablename__ = 'dinosaur_type'
    _s_collection_name = 'DinosaurType'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    species = Column(String, nullable=False)
    average_weight = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    DinosaurList : Mapped[List["Dinosaur"]] = relationship(back_populates="type")



class FoodType(SAFRSBaseX, Base):
    """
    description: Details about different food types provided to dinosaurs.
    """
    __tablename__ = 'food_type'
    _s_collection_name = 'FoodType'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    nutritional_value = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    FoodLogList : Mapped[List["FoodLog"]] = relationship(back_populates="food_type")



class HealthCondition(SAFRSBaseX, Base):
    """
    description: Health conditions or issues observed with dinosaurs.
    """
    __tablename__ = 'health_condition'
    _s_collection_name = 'HealthCondition'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    HealthRecordList : Mapped[List["HealthRecord"]] = relationship(back_populates="condition")



class ServiceType(SAFRSBaseX, Base):
    """
    description: Catalog of different services provided for dinosaur pets.
    """
    __tablename__ = 'service_type'
    _s_collection_name = 'ServiceType'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    price = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    ServiceRecordList : Mapped[List["ServiceRecord"]] = relationship(back_populates="service_type")



class Sitter(SAFRSBaseX, Base):
    """
    description: Details of assistants trained to take care of dinosaurs.
    """
    __tablename__ = 'sitter'
    _s_collection_name = 'Sitter'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    expertise = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    AppointmentList : Mapped[List["Appointment"]] = relationship(back_populates="sitter")



class Dinosaur(SAFRSBaseX, Base):
    """
    description: Individual dinosaur pets tied to a specific customer and type.
    """
    __tablename__ = 'dinosaur'
    _s_collection_name = 'Dinosaur'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    last_checkup_date = Column(DateTime)
    customer_id = Column(ForeignKey('customer.id'), nullable=False)
    type_id = Column(ForeignKey('dinosaur_type.id'), nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("DinosaurList"))
    type : Mapped["DinosaurType"] = relationship(back_populates=("DinosaurList"))

    # child relationships (access children)
    AppointmentList : Mapped[List["Appointment"]] = relationship(back_populates="dinosaur")
    FoodLogList : Mapped[List["FoodLog"]] = relationship(back_populates="dinosaur")
    HealthRecordList : Mapped[List["HealthRecord"]] = relationship(back_populates="dinosaur")



class Payment(SAFRSBaseX, Base):
    """
    description: Payment details relating to customer bookings and services.
    """
    __tablename__ = 'payment'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)



class Appointment(SAFRSBaseX, Base):
    """
    description: Booking details for each petsitting session.
    """
    __tablename__ = 'appointment'
    _s_collection_name = 'Appointment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, nullable=False)
    dinosaur_id = Column(ForeignKey('dinosaur.id'), nullable=False)
    sitter_id = Column(ForeignKey('sitter.id'), nullable=False)

    # parent relationships (access parent)
    dinosaur : Mapped["Dinosaur"] = relationship(back_populates=("AppointmentList"))
    sitter : Mapped["Sitter"] = relationship(back_populates=("AppointmentList"))

    # child relationships (access children)
    ServiceRecordList : Mapped[List["ServiceRecord"]] = relationship(back_populates="appointment")



class FoodLog(SAFRSBaseX, Base):
    """
    description: Records feeding information for each dinosaur.
    """
    __tablename__ = 'food_log'
    _s_collection_name = 'FoodLog'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    dinosaur_id = Column(ForeignKey('dinosaur.id'), nullable=False)
    food_type_id = Column(ForeignKey('food_type.id'), nullable=False)
    feeding_date = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    dinosaur : Mapped["Dinosaur"] = relationship(back_populates=("FoodLogList"))
    food_type : Mapped["FoodType"] = relationship(back_populates=("FoodLogList"))

    # child relationships (access children)



class HealthRecord(SAFRSBaseX, Base):
    """
    description: Logs health conditions associated with a dinosaur.
    """
    __tablename__ = 'health_record'
    _s_collection_name = 'HealthRecord'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    dinosaur_id = Column(ForeignKey('dinosaur.id'), nullable=False)
    condition_id = Column(ForeignKey('health_condition.id'), nullable=False)
    observation_date = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    condition : Mapped["HealthCondition"] = relationship(back_populates=("HealthRecordList"))
    dinosaur : Mapped["Dinosaur"] = relationship(back_populates=("HealthRecordList"))

    # child relationships (access children)



class ServiceRecord(SAFRSBaseX, Base):
    """
    description: Association between appointments and the services provided.
    """
    __tablename__ = 'service_record'
    _s_collection_name = 'ServiceRecord'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    appointment_id = Column(ForeignKey('appointment.id'), nullable=False)
    service_type_id = Column(ForeignKey('service_type.id'), nullable=False)

    # parent relationships (access parent)
    appointment : Mapped["Appointment"] = relationship(back_populates=("ServiceRecordList"))
    service_type : Mapped["ServiceType"] = relationship(back_populates=("ServiceRecordList"))

    # child relationships (access children)
