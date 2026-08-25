from faker import Faker
import csv

fake = Faker()

with open("customers.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["id", "name", "email", "phone", "city"])

    for i in range(1, 101):
        writer.writerow([
            i,
            fake.name(),
            fake.email(),
            fake.phone_number(),
            fake.city()
        ])

print("100 fake customers created!")