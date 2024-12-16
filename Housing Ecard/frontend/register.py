import tkinter as tk
from tkinter import messagebox
import requests

# Register User
def register_user():
    name = entry_name.get()
    aadhaar = entry_aadhaar.get()
    pan = entry_pan.get()
    mobile = entry_mobile.get()
    password = entry_password.get()

    # Validate user input
    if not name or not aadhaar or not pan or not mobile or not password:
        messagebox.showerror('Error', 'All fields are required!')
        return

    # Define the data to be sent to Flask backend
    data = {
        'name': name,
        'aadhaar': aadhaar,
        'pan': pan,
        'mobile': mobile,
        'password': password
    }

    try:
        # Send POST request to Flask backend for user registration
        response = requests.post('http://127.0.0.1:5000/register', data=data)

        # Check if the request was successful
        if response.status_code == 200:
            messagebox.showinfo('Success', 'Registration Successful')
        else:
            messagebox.showerror('Error', 'Registration Failed: ' + response.text)
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error', f'Error connecting to backend: {e}')

# Create the Tkinter window
root = tk.Tk()
root.title("Housing Ecard - Registration")

# Create and pack the labels and entry fields
tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Aadhaar").pack()
entry_aadhaar = tk.Entry(root)
entry_aadhaar.pack()

tk.Label(root, text="PAN").pack()
entry_pan = tk.Entry(root)
entry_pan.pack()

tk.Label(root, text="Mobile").pack()
entry_mobile = tk.Entry(root)
entry_mobile.pack()

tk.Label(root, text="Password").pack()
entry_password = tk.Entry(root, show="*")  # Hide password input
entry_password.pack()

# Create and pack the register button
tk.Button(root, text="Register", command=register_user).pack()

# Start the Tkinter event loop
root.mainloop()
