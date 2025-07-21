# PYTHONPATH=. python3 initialise/data_generation.py

# ---------- data faker functions
from faker import Faker
from app.utils.bcrypt import hash_password
from app.shared_constants.product_categories import product_categories_tuple
import random

fake = Faker() # initialise

def randomize_none(value, p=0.2):
    # randomize None with probability of < 0.2
    return None if random.random() < p else value

def generate_user_simple():
    while True:
        try:
            sex_selected = random.choice(["M", "F", "X"])
            person = fake.simple_profile(sex=sex_selected)
            return {"username": person.get("username"),
                    "email": person.get("mail"),
                    "password": hash_password("12345678")}
        except:
            print(">> FAIL cause fake.simple_profile() has issues")

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
            print(">> FAIL cause fake.simple_profile() has issues")

def generate_product(user_list):
    while True:
        try:
            return {
                "product_name": fake.catch_phrase(),
                "product_description": randomize_none(fake.paragraph(), 0.3),
                "owner_user_id": random.choice(user_list),
                "category": random.choice(product_categories_tuple),
                "main_display_photo": randomize_none(fake.image_url(), 0.3),
                "default_delivery_time": randomize_none(random.randint(1,60), 0.6),
                # "viewable_to": fake.,
                "is_active": randomize_none(False, 0.7),
            }
        except:
            print(">> FAIL due to some hidden has issues")


# ---------- define app & db_connection
from app.db.db_connection import get_db_connection


def seed_users_route():

    try:
        (connection, cursor) = get_db_connection()
        
        # ----- delete all data
        cursor.execute("DELETE FROM products;")
        cursor.execute("DELETE FROM users;")

        # ----- generate users
        print("--- Users ---")
        # generate faker user data
        print("users_simple_list creating")
        users_simple_list = [generate_user_simple() for x in range(5)]
        
        # insert basic users
        print("users_simple_list inserting to db")
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s);", ("user1", "user1@test.com", hash_password("12345678"),))
        list(map(lambda data: cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s);", (data["username"], data["email"], data["password"])),
            users_simple_list))
        
        # generate faker complex user
        print("users_complex_list creating")
        users_complex_list = [generate_user_complex() for x in range(5)]

        # insert complex users
        print("users_complex_list inserting to db")   
        list(map(lambda data: cursor.execute("INSERT INTO users (username, email, password, first_name, last_name, gender, birthday, phone_number, profile_photo, default_shipping_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                                             (data["username"], data["email"], data["password"], data["first_name"], data["last_name"], data["gender"], data["birthday"], data["phone_number"], data["profile_photo"], data["default_shipping_address"])),
            users_complex_list))
        
        # double users
        print("users done")
        connection.commit() # save data
        cursor.execute("SELECT id FROM users;")
        user_list = [row["id"] for row in cursor.fetchall()]
        print(user_list)

        # ----- generate products
        print("--- Products ---")
        # generate products
        print("products_list creating")
        products_list = [generate_product(user_list) for x in range(50)]
        # insert products
        print("products_list inserting to db")   
        list(map(lambda data: cursor.execute("INSERT INTO products (product_name, product_description, owner_user_id, category, main_display_photo, default_delivery_time, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s);", (data["product_name"], data["product_description"], data["owner_user_id"], data["category"], data["main_display_photo"], data["default_delivery_time"], data["is_active"])),
            products_list))

        print("products done")

        # ----- save changes
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
    