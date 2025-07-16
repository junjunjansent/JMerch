# PYTHONPATH=. python3 initialise/data_generation.py

from flask import Flask, jsonify


# ---------- data faker functions
from faker import Faker
from app.utils.bcrypt import hash_password
import random

fake = Faker() # initialise

def generate_user_simple():
    while True:
        try:
            sex_selected = random.choice(["M", "F", "X"])
            person = fake.simple_profile(sex=sex_selected)
            return {"username": person.get("username"),
                    "email": person.get("mail"),
                    "password": hash_password("12345678")}
        except:
            print("FAIL cause fake.simple_profile() has issues")

def generate_user_complex():
    while True:
        try: 
            sex_selected = random.choice(["M", "F", "X"])
            gender={"M":"male", "F":'female',"X": 'non-binary'}
            gender_selected = gender[sex_selected]
            
            person = fake.simple_profile(sex=sex_selected)
            name = person.get("name").split(" ") if person.get("name") else None
            name = name if name and len(name) > 1 else [fake.first_name(), fake.last_name()]
            return {"username": person.get("username"),
                    "email": person.get("mail"),
                    "password": hash_password("12345678"),
                    "first_name": name[0], 
                    "last_name": name[1],
                    "gender": gender_selected,
                    "birthday": fake.date_of_birth(maximum_age=100), 
                    "phone_number": fake.msisdn(),
                    "profile_photo": fake.image_url(),
                    "default_shipping_address": person.get("address")}
        except:
            print("FAIL cause fake.simple_profile() has issues")


# ---------- define app & db_connection
from app.db.db_connection import get_db_connection


def seed_users_route():
    try:
        (connection, cursor) = get_db_connection()
        
        # delete all data
        cursor.execute("DELETE FROM users;")

        print("users_simple_list creating")
        # generate faker user data
        users_simple_list = [generate_user_simple() for x in range(5)]
        
        print("users_simple_list inserted to db")
        # insert basic users
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s);", ("user1", "user1@test.com", hash_password("12345678"),))
        list(map(lambda data: cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s);", (data["username"], data["email"], data["password"])),
            users_simple_list))
        
        print("users_complex_list creating")
        # generate faker complex user
        users_complex_list = [generate_user_complex() for x in range(5)]

        print("users_complex_list inserted to db")   
        # insert complex users
        list(map(lambda data: cursor.execute("INSERT INTO users (username, email, password, first_name, last_name, gender, birthday, phone_number, profile_photo, default_shipping_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                                             (data["username"], data["email"], data["password"], data["first_name"], data["last_name"], data["gender"], data["birthday"], data["phone_number"], data["profile_photo"], data["default_shipping_address"])),
            users_complex_list))

        # save changes
        connection.commit() # save data

    except Exception as err:
        connection.rollback()
        print("error -- ", str(err))
    finally:
        cursor.close()
        connection.close()


# ----- run generator

if __name__ == '__main__':
    seed_users_route()
    