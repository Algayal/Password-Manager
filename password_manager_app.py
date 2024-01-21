""" Module providing a class that creats a password manager desktop application """

import json
import string
from random import choice, randint, shuffle
from tkinter import END, Button, Canvas, Entry, Label, PhotoImage, Tk, messagebox

import pyperclip

WORK_EMAIL = "Example@gmail.com"


class PasswordManager:
    """Password manager desktop application"""

    def __init__(self):
        self.user_website = None
        self.user_email = None
        self.user_password = None
        self.new_data = None
        self.archived_email = None
        self.archived_password = None

        self.initialize_window()
        self.labels_and_entries()
        self.image_generator()
        self.buttons_and_commands()
        self.window.mainloop()

    def initialize_window(self):
        """ "Create an empty window"""
        self.window = Tk()
        self.window.title("Password Manager")
        self.window.config(padx=40, pady=20)

    def labels_and_entries(self):
        """Create all the labels and the entry fields"""
        # Website
        self.website_label = Label(text="Website:")
        self.website_label.grid(row=1, column=0)
        self.website_label.config(padx=3, pady=3)

        self.website_entry = Entry(width=30)
        self.website_entry.focus()  # focus the cursor on this entry box
        self.website_entry.grid(row=1, column=1)

        # Email
        self.email_label = Label(text="Email/Username")
        self.email_label.grid(row=2, column=0)
        self.email_label.config(padx=3, pady=3)

        self.email_entry = Entry(width=49)
        self.email_entry.insert(0, WORK_EMAIL)
        self.email_entry.grid(row=2, column=1, columnspan=2)

        # Password
        self.password_label = Label(text="Password:")
        self.password_label.grid(row=3, column=0)
        self.password_label.config(padx=7, pady=7)

        self.password_entry = Entry(width=30)
        self.password_entry.grid(row=3, column=1)

    def image_generator(self):
        """Download the image and display it in the window"""
        self.canvas = Canvas(width=200, height=200)
        self.lock_image = PhotoImage(file="logo.png")
        self.canvas.create_image(100, 100, image=self.lock_image)
        self.canvas.grid(row=0, column=1)

    def generate_password(self):
        """Generate a random password made of letters, numbers and symbols"""
        alphabets = list(string.ascii_letters)

        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

        alphabets_list = [choice(alphabets) for letter in range(randint(8, 10))]
        numbers_list = [choice(numbers) for number in range(randint(2, 4))]
        symbols_list = [choice(symbols) for symbol in range(randint(2, 4))]

        password_list = alphabets_list + numbers_list + symbols_list
        shuffle(password_list)

        generated_password = "".join(password_list)
        self.password_entry.insert(0, generated_password)
        pyperclip.copy(generated_password)

    def buttons_and_commands(self):
        """Create all the buttons and assign them to specific functions"""
        self.generate_password_button = Button(
            text="Generate Password", width=15, command=self.generate_password
        )
        self.generate_password_button.grid(row=3, column=2)

        self.add_button = Button(text="Add", width=44, command=self.save)
        self.add_button.grid(row=4, column=1, columnspan=2)

        self.search_button = Button(text="Search", width=15, command=self.search)
        self.search_button.grid(row=1, column=2)

    def save(self):
        """Save the user's entries to a .json file and clear the input field"""

        self.user_website = self.website_entry.get()  # get hold of the inserted entry
        self.user_email = self.email_entry.get()
        self.user_password = self.password_entry.get()
        self.new_data = {
            self.user_website.lower(): {
                "email": self.user_email,
                "password": self.user_password,
            }
        }

        if len(self.user_website) == 0 or len(self.user_password) == 0:
            messagebox.showerror(
                title="Missing Information",
                message="Please fill in the missing information!",
            )

        else:
            try:
                with open("data.json", "r") as file:
                    json_data = json.load(file)
            except FileNotFoundError:
                with open("data.json", mode="w") as file:
                    json.dump(self.new_data, file, indent=4)

            else:
                json_data.update(self.new_data)

                with open("data.json", mode="w") as file:
                    json.dump(json_data, file, indent=4)  # we dump the updated data

            finally:
                # deleting the entries after being saved
                self.website_entry.delete(0, END)
                self.password_entry.delete(0, END)

    def search(self):
        """Search through the .json file for the website and display it's email and password"""
        self.user_website = self.website_entry.get()

        try:
            with open("data.json", "r") as file:
                json_data = json.load(file)

        except FileNotFoundError:
            messagebox.showerror(title="Error", message="No data file found.")

        else:
            # can also use try/except, but always use if else when possible
            if self.user_website in json_data:
                self.archived_email = json_data[self.user_website.lower()]["email"]
                self.archived_password = json_data[self.user_website.lower()][
                    "password"
                ]
                messagebox.showinfo(
                    title=self.user_website,
                    message=f"Email: {self.archived_email}\nPassword:{self.archived_password}",
                )

            else:
                messagebox.showerror(
                    title="Error", message="No details for the website exists."
                )

        self.website_entry.delete(0, END)
