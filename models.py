from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import os

database_path = 'postgresql://postgres:kandis@localhost:5432/capstone'

db = SQLAlchemy()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Person
Have title and release year
'''


class Shelter(db.Model):
    __tablename__ = 'shelters'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    state = Column(String)
    address = Column(String)

    def __init__(self, name, city, state, address):
        self.name = name
        self.city = city
        self.state = state
        self.address = address

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'city': self.city,
          'state': self.state,
          'address': self.address
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Animal(db.Model):
    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    species = Column(String)
    breed = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelters.id'))

    def __init__(self, name, gender, age, species, breed, shelter_id):
        self.name = name
        self.gender = gender
        self.age = age
        self.species = species
        self.breed = breed
        self.shelter_id = shelter_id

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'gender': self.gender,
          'age': self.age,
          'species': self.species,
          'breed': self.breed,
          'shelter_id': self.shelter_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()