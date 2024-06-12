import tkinter as tk
from tkinter import Label, Entry, Button, Listbox, simpledialog, messagebox, END, Frame, Canvas, Scrollbar
import sqlite3
from PIL import Image, ImageTk
import os

NETFLIX_BLACK = "#141414"
NETFLIX_RED = "#E50914"
NETFLIX_WHITE = "#FFFFFF"
NETFLIX_GRAY = "#757575"

# Connect to the SQLite database
conn = sqlite3.connect('icecream.db')
cursor = conn.cursor()

# Create a table to store flavors if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS flavors
              (name TEXT, seasonal INTEGER, ingredients TEXT, allergens TEXT)''')
conn.commit()

# Create a table to store cart items if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS cart
              (name TEXT, allergens TEXT)''')
conn.commit()

# Create a temporary table for suggested flavors
cursor.execute('''CREATE TEMPORARY TABLE suggested_flavors
              (name TEXT, seasonal INTEGER, ingredients TEXT, allergens TEXT)''')
conn.commit()

# Clear the cart table on application start
cursor.execute("DELETE FROM cart")
conn.commit()

# Clear the flavors and suggested_flavors tables on application start
cursor.execute("DELETE FROM flavors")
conn.commit()
cursor.execute("DELETE FROM suggested_flavors")
conn.commit()

# Insert values for flavors
flavors_to_insert = [
    ("Vanilla", 0, "Milk, Sugar, Vanilla Extract", "Milk"),
    ("Chocolate", 0, "Milk, Sugar, Chocolate", "Milk"),
    ("Strawberry", 1, "Milk, Sugar, Strawberry", "Milk"),
    ("Butterscotch", 0, "Milk, Sugar, Butterscotch Flavoring", "Milk"),
    ("Cookies and Cream", 0, "Milk, Sugar, Chocolate Cookies", "Milk, Wheat"),
    ("Pista", 0, "Milk, Sugar, Pistachio Nuts", "Milk, Nuts"),
    ("Mango", 1, "Milk, Sugar, Mango Pulp", "Milk")
]

cursor.executemany("INSERT INTO flavors (name, seasonal, ingredients, allergens) VALUES (?, ?, ?, ?)", flavors_to_insert)
conn.commit()
print("Inserted default flavors into the flavors table")

class IceCreamParlorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ice Cream Parlor")
        self.root.geometry("800x600")
        self.root.configure(bg=NETFLIX_BLACK)  # Setting background color

        self.create_main_window()

    def create_main_window(self):
        self.clear_window()

        self.home_label = Label(self.root, text="SHARKS ICE CREAM PARLOUR", font=("Arial", 24), fg=NETFLIX_WHITE, bg=NETFLIX_BLACK)
        self.home_label.pack(pady=20)

        self.flavors_button = Button(self.root, text="View Flavors", command=self.open_flavors_window, bg=NETFLIX_RED, fg=NETFLIX_WHITE, font=("Arial", 14))
        self.flavors_button.pack(pady=10)

        self.cart_button = Button(self.root, text="View Cart", command=self.open_cart_window, bg=NETFLIX_RED, fg=NETFLIX_WHITE, font=("Arial", 14))
        self.cart_button.pack(pady=10)

        self.suggest_button = Button(self.root, text="Suggest a Flavor", command=self.open_suggest_window, bg=NETFLIX_RED, fg=NETFLIX_WHITE, font=("Arial", 14))
        self.suggest_button.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def open_flavors_window(self):
        self.clear_window()

        self.frame = Frame(self.root, bg=NETFLIX_BLACK)
        self.frame.pack(expand=True, fill="both")
        self.frame.columnconfigure(0, weight=1)

        self.scrollbar = Scrollbar(self.frame, orient="vertical")
        self.canvas = Canvas(self.frame, bg=NETFLIX_BLACK, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = Frame(self.canvas, bg=NETFLIX_BLACK)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.load_flavors()

        self.search_label = Label(self.inner_frame, text="Search Flavors:", font=("Arial", 12), fg=NETFLIX_WHITE,
                                  bg=NETFLIX_BLACK)
        self.search_label.grid(row=0, column=0, pady=(10, 5), sticky="w")

        self.search_entry = Entry(self.inner_frame, width=30)
        self.search_entry.grid(row=0, column=1, pady=(10, 5), padx=(5, 0))
        # Bind the <Return> event to call the search_flavors method
        self.search_entry.bind('<Return>', lambda event: self.search_flavors())

        self.search_button = Button(self.inner_frame, text="Search", command=self.search_flavors, bg=NETFLIX_RED,
                                    fg=NETFLIX_WHITE, font=("Arial", 12))
        self.search_button.grid(row=0, column=2, pady=(10, 5), padx=(5, 0))

        self.back_button = Button(self.inner_frame, text="Back", command=self.create_main_window, bg=NETFLIX_RED,
                                  fg=NETFLIX_WHITE, font=("Arial", 12))
        self.back_button.grid(row=0, column=3, pady=(10, 5), padx=(5, 0))

        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_flavors(self):
        cursor.execute("SELECT name FROM flavors")
        flavors = cursor.fetchall()

        row_index = 1
        col_index = 0

        for flavor in flavors:
            if col_index == 3:
                row_index += 1
                col_index = 0

            self.create_flavor_button(flavor[0], row_index, col_index)
            col_index += 1

        cursor.execute("SELECT name FROM suggested_flavors")
        suggested_flavors = cursor.fetchall()

        for flavor in suggested_flavors:
            if col_index == 3:
                row_index += 1
                col_index = 0

            self.create_flavor_button(flavor[0], row_index, col_index)
            col_index += 1

    def create_flavor_button(self, flavor_name, row, column):
        image_path = os.path.join("C:/Users/admin/PycharmProjects/pythonProject3", f"{flavor_name}.jpg")
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((100, 100), Image.LANCZOS)

            photo = ImageTk.PhotoImage(image)
            button = Button(self.inner_frame, text=flavor_name, image=photo, compound="top", bg=NETFLIX_RED, fg=NETFLIX_WHITE, font=("Arial", 12), command=lambda name=flavor_name: self.add_to_cart(name))
            button.image = photo  # Keep a reference to avoid garbage collection
            button.grid(row=row, column=column, padx=10, pady=10)
        else:
            button = Button(self.inner_frame, text=flavor_name, bg=NETFLIX_RED, fg=NETFLIX_WHITE, font=("Arial", 12), command=lambda name=flavor_name: self.add_to_cart(name))
            button.grid(row=row, column=column, padx=10, pady=10)

    def search_flavors(self):
        query = self.search_entry.get().lower()
        for widget in self.inner_frame.winfo_children():
            if isinstance(widget, Button):
                widget.destroy()

        cursor.execute("SELECT name FROM flavors WHERE LOWER(name) LIKE ?", ('%' + query + '%',))
        flavors = cursor.fetchall()
        row_index = 1
        col_index = 0
        for flavor in flavors:
            if col_index == 3:
                row_index += 1
                col_index = 0

            self.create_flavor_button(flavor[0], row_index, col_index)
            col_index += 1

        cursor.execute("SELECT name FROM suggested_flavors WHERE LOWER(name) LIKE ?", ('%' + query + '%',))
        suggested_flavors = cursor.fetchall()
        for flavor in suggested_flavors:
            if col_index == 3:
                row_index += 1
                col_index = 0

            self.create_flavor_button(flavor[0], row_index, col_index)
            col_index += 1

        # Add the back button again
        self.back_button = Button(self.inner_frame, text="Back", command=self.create_main_window, bg=NETFLIX_RED,
                                  fg=NETFLIX_WHITE, font=("Arial", 12))
        self.back_button.grid(row=row_index, column=0, columnspan=3, pady=(10, 5), padx=(200, 0), sticky="w")

    def add_to_cart(self, flavor_name):
        cursor.execute("SELECT * FROM flavors WHERE name=?", (flavor_name,))
        flavor = cursor.fetchone()
        if not flavor:
            cursor.execute("SELECT * FROM suggested_flavors WHERE name=?", (flavor_name,))
            flavor = cursor.fetchone()

        if flavor:
            allergies = simpledialog.askstring("Input", f"Enter Allergies (comma separated) for {flavor_name}:")
            if allergies is not None and allergies.strip() != "":
                cursor.execute("INSERT INTO cart (name, allergens) VALUES (?, ?)", (flavor_name, allergies))
                conn.commit()
                messagebox.showinfo("Cart", f"Added {flavor_name} to cart with allergies: {allergies}.")
            else:
                cursor.execute("INSERT INTO cart (name, allergens) VALUES (?, ?)", (flavor_name, None))
                conn.commit()
                messagebox.showinfo("Cart", f"Added {flavor_name} to cart.")
        else:
            messagebox.showerror("Error", "Flavor not found.")

    def open_cart_window(self):
        self.clear_window()
        self.cart_listbox = Listbox(self.root, width=50, height=10)
        self.cart_listbox.pack(padx=10, pady=10)
        self.load_cart()

        self.back_button = Button(self.root, text="Back", command=self.create_main_window, bg=NETFLIX_RED, fg=NETFLIX_WHITE, font=("Arial", 14))
        self.back_button.pack(pady=10)

    def load_cart(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.cart_label = Label(self.root, text="Cart Items", font=("Arial", 18), fg=NETFLIX_WHITE, bg=NETFLIX_BLACK)
        self.cart_label.pack(pady=10)

        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side="right", fill="y")

        self.cart_frame = Frame(self.root, bg=NETFLIX_BLACK)
        self.cart_frame.pack(fill="both", expand=True)

        self.cart_canvas = Canvas(self.cart_frame, bg=NETFLIX_BLACK, yscrollcommand=scrollbar.set)
        self.cart_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.cart_canvas.yview)

        self.cart_frame_inner = Frame(self.cart_canvas, bg=NETFLIX_BLACK)
        self.cart_canvas.create_window((0, 0), window=self.cart_frame_inner, anchor="nw")

        cursor.execute("SELECT * FROM cart")
        cart_items = cursor.fetchall()

        row_index = 0
        for item in cart_items:
            flavor_name = item[0]
            allergens = item[1]
            image_path = os.path.join("C:/Users/admin/PycharmProjects/pythonProject3",
                                      f"{flavor_name}.jpg")
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                button = Button(self.cart_frame_inner, text=flavor_name, image=photo, compound="top",
                                bg=NETFLIX_RED, fg=NETFLIX_WHITE, font=("Arial", 12),
                                command=lambda name=flavor_name: self.remove_from_cart(name))
                button.image = photo  # Keep a reference to avoid garbage collection
                button.grid(row=row_index, column=0, padx=10, pady=10)

                if allergens:
                    allergens_label = Label(self.cart_frame_inner, text=f"Allergens: {allergens}", bg=NETFLIX_BLACK,
                                            fg=NETFLIX_WHITE, font=("Arial", 10))
                    allergens_label.grid(row=row_index + 1, column=0, padx=10, pady=5)
            else:
                label = Label(self.cart_frame_inner, text=flavor_name, bg=NETFLIX_BLACK, fg=NETFLIX_WHITE,
                              font=("Arial", 12))
                label.grid(row=row_index, column=0, padx=10, pady=10)

                if allergens:
                    allergens_label = Label(self.cart_frame_inner, text=f"Allergens: {allergens}", bg=NETFLIX_BLACK,
                                            fg=NETFLIX_WHITE, font=("Arial", 10))
                    allergens_label.grid(row=row_index + 1, column=0, padx=10, pady=5)

            row_index += 2  # Increase by 2 to leave space for allergens if present

        self.cart_frame_inner.update_idletasks()
        self.cart_canvas.config(scrollregion=self.cart_canvas.bbox("all"))

    def remove_from_cart(self, flavor_name):
        cursor.execute("DELETE FROM cart WHERE name=?", (flavor_name,))
        conn.commit()
        self.load_cart()

    def open_suggest_window(self):
        self.clear_window()
        self.flavor_name_label = Label(self.root, text="Enter Flavor Name:", font=("Arial", 14), fg=NETFLIX_WHITE, bg=NETFLIX_BLACK)
        self.flavor_name_label.pack(pady=5)
        self.flavor_name_entry = Entry(self.root)
        self.flavor_name_entry.pack(pady=5)
        self.ingredients_label = Label(self.root, text="Enter Ingredients (comma separated):", font=("Arial", 14), fg=NETFLIX_WHITE, bg=NETFLIX_BLACK)
        self.ingredients_label.pack(pady=5)
        self.ingredients_entry = Entry(self.root)
        self.ingredients_entry.pack(pady=5)
        self.allergens_label = Label(self.root, text="Enter Allergens (comma separated):", font=("Arial", 14), fg=NETFLIX_WHITE, bg=NETFLIX_BLACK)
        self.allergens_label.pack(pady=5)
        self.allergens_entry = Entry(self.root)
        self.allergens_entry.pack(pady=5)
        self.submit_suggest_button = Button(self.root, text="Submit", command=self.suggest_flavor, bg=NETFLIX_RED, fg=NETFLIX_WHITE, font=("Arial", 14))
        self.submit_suggest_button.pack(pady=10)
        self.back_button = Button(self.root, text="Back", command=self.create_main_window, bg=NETFLIX_RED, fg=NETFLIX_WHITE, font=("Arial", 14))
        self.back_button.pack(pady=10)

    def suggest_flavor(self):
        flavor_name = self.flavor_name_entry.get()
        ingredients = self.ingredients_entry.get().split(", ")
        allergens = self.allergens_entry.get().split(", ")
        if self.allergens_entry.get().strip() != "":
            pass
        else:
            allergens = None
        if flavor_name and ingredients:

            cursor.execute("SELECT COUNT(*) FROM suggested_flavors WHERE name=?", (flavor_name,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO suggested_flavors (name, seasonal, ingredients, allergens) VALUES (?, ?, ?, ?)",
                               (flavor_name, 0, ", ".join(ingredients), ", ".join(allergens) if allergens else None))
                conn.commit()
                messagebox.showinfo("Suggestion", f"Suggested {flavor_name} has been added.")
            else:
                messagebox.showwarning("Warning", f"Flavor {flavor_name} is already suggested.")
        else:
            messagebox.showerror("Error", "Flavor name and ingredients are required.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ice Cream Parlor")
    root.geometry("800x600")
    root.resizable(False, False)  # Disable resizing
    app = IceCreamParlorApp(root)
    root.mainloop()