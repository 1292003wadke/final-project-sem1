import tkinter as tk
from tkinter import messagebox
import requests

# Function to handle admin login
def admin_login():
    username = entry_username.get()
    password = entry_password.get()

    # Validate input fields
    if not username or not password:
        messagebox.showerror('Error', 'Both username and password are required.')
        return

    # Define the data to be sent to Flask backend for admin login
    data = {
        'username': username,
        'password': password
    }

    try:
        response = requests.post('http://127.0.0.1:5000/admin', data=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            messagebox.showinfo('Success', 'Admin Login Successful')
            open_admin_dashboard()  # You can define this function to open the admin dashboard
        else:
            messagebox.showerror('Error', 'Invalid admin credentials')
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error', f'Error connecting to backend: {e}')

# Function to open the admin dashboard window (you can add more functionalities here)
def open_admin_dashboard():
    dashboard_window = tk.Toplevel(root)  # New window
    dashboard_window.title("Admin Dashboard")

    # Add content for the admin dashboard window
    tk.Label(dashboard_window, text="Welcome to the Admin Dashboard!", font=("Helvetica", 14)).pack(pady=20)
    tk.Button(dashboard_window, text="Logout", command=dashboard_window.destroy).pack(pady=10)

# Create the Tkinter window
root = tk.Tk()
root.title("Housing Ecard - Admin Login")

# Create and pack the labels and entry fields with some padding
tk.Label(root, text="Username").pack(padx=20, pady=5)
entry_username = tk.Entry(root)
entry_username.pack(padx=20, pady=5)

tk.Label(root, text="Password").pack(padx=20, pady=5)
entry_password = tk.Entry(root, show="*")  # Hide password input
entry_password.pack(padx=20, pady=5)

# Create and pack the login button
tk.Button(root, text="Login", command=admin_login).pack(padx=20, pady=20)

# Start the Tkinter event loop
root.mainloop()
