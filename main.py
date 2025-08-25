import json
from cryptography.fernet import Fernet
import pyperclip
import os

file_name = 'data.json'
key_file = 'key.key'



def load_key():
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
        return key



def load_database():
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.load(file)
    return {}


def save_database(data_base):
    with open(file_name, "w") as file:
        json.dump(data_base, file, indent=4)



def add(f, data_base):
    site = input("Enter the site name: ")
    login = input("Enter your login: ")
    password = input("Enter your password: ")

    encrypted_password = f.encrypt(password.encode()).decode()
    pyperclip.copy(password) 

    data_base[site] = [login, encrypted_password]
    save_database(data_base)
    print(f"Password for {site} saved and copied to clipboard!")


def view(f, data_base):
    if not data_base:
        print("No entries found.")
        return
    for site, (login, encrypted_password) in data_base.items():
        decrypted_password = f.decrypt(encrypted_password.encode()).decode()
        print(f"Site: {site}\nLogin: {login}\nPassword: {decrypted_password}\n")


def copy(f, data_base):
    site = input("Enter the site name you want to copy the password for: ")
    if site in data_base:
        decrypted_password = f.decrypt(data_base[site][1].encode()).decode()
        pyperclip.copy(decrypted_password)
        print("Password copied to clipboard.")
    else:
        print("Site not found.")


def main():
    key = load_key()
    f = Fernet(key)
    data_base = load_database()

    while True:
        mode = input("Choose a mode: add, view, copy, or quit: ").lower()
        if mode == "add":
            add(f, data_base)
        elif mode == "view":
            view(f, data_base)
        elif mode == "copy":
            copy(f, data_base)
        elif mode == "quit":
            break
        else:
            print("Invalid mode. Please try again.")


if __name__ == '__main__':
    main()
