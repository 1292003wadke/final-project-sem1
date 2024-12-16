import tkinter as tk
from tkinter import messagebox
import requests

# Function to handle user login
def login_user():
    username = entry_username.get()
    password = entry_password.get()

    # Validate input fields
    if not username or not password:
        messagebox.showerror('Error', 'Both username and password are required.')
        return

    # Define the data to be sent to Flask backend for login
    data = {
        'username': username,
        'password': password
    }

    try:
        response = requests.post('http://127.0.0.1:5000/login', data=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            messagebox.showinfo('Success', 'Login Successful')
            # Redirect to user dashboard or open a new window (example: open_dashboard())
            open_dashboard()  # You can define this function to open the next window
        else:
            messagebox.showerror('Error', 'Invalid username or password')
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error', f'Error connecting to backend: {e}')

# Function to open the dashboard window (you can implement more functionality)
def open_dashboard():
    dashboard_window = tk.Toplevel(root)  # New window
    dashboard_window.title("User Dashboard")

    # Add content for the dashboard window
    tk.Label(dashboard_window, text="Welcome to your dashboard!", font=("Helvetica", 14)).pack(pady=20)
    tk.Button(dashboard_window, text="Logout", command=dashboard_window.destroy).pack(pady=10)

# Create the Tkinter window
root = tk.Tk()
root.title("Housing Ecard - User Login")

# Create and pack the labels and entry fields with some padding
tk.Label(root, text="Username").pack(padx=20, pady=5)
entry_username = tk.Entry(root)
entry_username.pack(padx=20, pady=5)

tk.Label(root, text="Password").pack(padx=20, pady=5)
entry_password = tk.Entry(root, show="*")  # Hide password input
entry_password.pack(padx=20, pady=5)

# Create and pack the login button
tk.Button(root, text="Login", command=login_user).pack(padx=20, pady=20)

# Start the Tkinter event loop
root.mainloop()
