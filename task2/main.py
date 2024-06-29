from pymongo import MongoClient
from bson.objectid import ObjectId

# Establish a connection to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")
db = client["cat_database"]
collection = db["cats"]


def create_cat(name, age, features):
    cat = {"name": name, "age": age, "features": features}
    collection.insert_one(cat)
    print(f"Cat {name} added successfully!")


def read_all_cats():
    cats = collection.find()
    for cat in cats:
        print(cat)


def read_cat_by_name(name):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"No cat found with the name {name}")


def update_cat_age(name, new_age):
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count > 0:
        print(f"Cat {name} age updated to {new_age}")
    else:
        print(f"No cat found with the name {name}")


def add_feature_to_cat(name, feature):
    result = collection.update_one({"name": name}, {"$push": {"features": feature}})
    if result.matched_count > 0:
        print(f"Feature '{feature}' added to cat {name}")
    else:
        print(f"No cat found with the name {name}")


def delete_cat_by_name(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Cat {name} deleted")
    else:
        print(f"No cat found with the name {name}")


def delete_all_cats():
    result = collection.delete_many({})
    print(f"All cats deleted. Total deleted: {result.deleted_count}")


def main():
    while True:
        print("\nCat Database Management")
        print("1. Add a new cat")
        print("2. View all cats")
        print("3. Find a cat by name")
        print("4. Update cat's age by name")
        print("5. Add a feature to a cat by name")
        print("6. Delete a cat by name")
        print("7. Delete all cats")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter cat's name: ")
            age = int(input("Enter cat's age: "))
            features = input("Enter cat's features (comma-separated): ").split(",")
            create_cat(name, age, features)
        elif choice == "2":
            read_all_cats()
        elif choice == "3":
            name = input("Enter cat's name to find: ")
            read_cat_by_name(name)
        elif choice == "4":
            name = input("Enter cat's name to update age: ")
            new_age = int(input("Enter new age: "))
            update_cat_age(name, new_age)
        elif choice == "5":
            name = input("Enter cat's name to add feature: ")
            feature = input("Enter new feature: ")
            add_feature_to_cat(name, feature)
        elif choice == "6":
            name = input("Enter cat's name to delete: ")
            delete_cat_by_name(name)
        elif choice == "7":
            delete_all_cats()
        elif choice == "8":
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
