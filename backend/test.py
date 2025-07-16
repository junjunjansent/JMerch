from faker import Faker
fake = Faker()

person = fake.simple_profile()
print(person)

name = person.get("name").split(" ") if person.get("name") else None
name = name if name and len(name) > 1 else ["John", "Doe"]
print(name)