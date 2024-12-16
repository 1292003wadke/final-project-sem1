import tkinter as tk
from tkinter import messagebox
import requests

# Flask base URL
FLASK_BASE_URL = "http://127.0.0.1:5000"

# Register User
def register_user():
    # Gather user details from the Tkinter form
    name = name_entry.get()
    aadhaar = aadhaar_entry.get()
    pan = pan_entry.get()
    mobile = mobile_entry.get()
    password = password_entry.get()

    # Send POST request to the Flask registration route
    response = requests.post(f'{FLASK_BASE_URL}/register', data={
        'name': name,
        'aadhaar': aadhaar,
        'pan': pan,
        'mobile': mobile,
        'password': password
    })
    
    if response.status_code == 200:
        messagebox.showinfo("Success", "Registration successful!")
    else:
        messagebox.showerror("Error", "Registration failed! Please try again.")

# Login User
def login_user():
    # Gather login credentials from the Tkinter form
    username = username_entry.get()
    password = password_entry.get()

    # Send POST request to the Flask login route
    response = requests.post(f'{FLASK_BASE_URL}/login', data={
        'username': username,
        'password': password
    })

    if response.status_code == 200:
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Invalid username or password. Please try again.")

# Admin Login
def admin_login():
    username = admin_username_entry.get()
    password = admin_password_entry.get()

    response = requests.post(f'{FLASK_BASE_URL}/admin', data={
        'username': username,
        'password': password
    })

    if response.status_code == 200:
        messagebox.showinfo("Success", "Admin login successful!")
        open_admin_dashboard()
    else:
        messagebox.showerror("Error", "Invalid admin credentials. Please try again.")

# Open Admin Dashboard
def open_admin_dashboard():
    admin_dashboard_window = tk.Toplevel()
    admin_dashboard_window.title("Admin Dashboard")

    # Fetch users from Flask backend (simulate with dummy data)
    response = requests.get(f'{FLASK_BASE_URL}/dashboard')

    if response.status_code == 200:
        users = response.json()  # assuming the response is JSON
        for user in users:
            user_frame = tk.Frame(admin_dashboard_window)
            user_frame.pack(pady=5, fill='x', padx=20)
            
            user_label = tk.Label(user_frame, text=f"{user['name']} - {user['status']}", anchor='w')
            user_label.pack(side='left', padx=10)
            
            # Approve Button
            approve_button = tk.Button(user_frame, text="Approve", command=lambda user_id=user['id']: update_user_status(user_id, 'Approved'))
            approve_button.pack(side='left', padx=5)
            
            # Reject Button
            reject_button = tk.Button(user_frame, text="Reject", command=lambda user_id=user['id']: update_user_status(user_id, 'Rejected'))
            reject_button.pack(side='left', padx=5)
    else:
        messagebox.showerror("Error", "Failed to load users.")

# Update User Status (Admin Dashboard)
def update_user_status(user_id, status):
    try:
        response = requests.get(f'{FLASK_BASE_URL}/update_status/{user_id}/{status}')
        if response.status_code == 200:
            messagebox.showinfo('Success', f'User status updated to {status}')
            open_admin_dashboard()  # Refresh dashboard after update
        else:
            messagebox.showerror('Error', 'Failed to update status')
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error', f'Error connecting to backend: {e}')

# Tkinter UI
root = tk.Tk()
root.title("Housing Ecard")

# Login Form
login_frame = tk.Frame(root)
login_frame.pack(padx=10, pady=10)

tk.Label(login_frame, text="Username").grid(row=0, column=0)
tk.Label(login_frame, text="Password").grid(row=1, column=0)

username_entry = tk.Entry(login_frame)
password_entry = tk.Entry(login_frame, show="*")

username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)

login_button = tk.Button(login_frame, text="Login", command=login_user)
login_button.grid(row=2, columnspan=2)

# Register Form
register_frame = tk.Frame(root)
register_frame.pack(padx=10, pady=10)

tk.Label(register_frame, text="Name").grid(row=0, column=0)
tk.Label(register_frame, text="Aadhaar").grid(row=1, column=0)
tk.Label(register_frame, text="PAN").grid(row=2, column=0)
tk.Label(register_frame, text="Mobile").grid(row=3, column=0)
tk.Label(register_frame, text="Password").grid(row=4, column=0)

name_entry = tk.Entry(register_frame)
aadhaar_entry = tk.Entry(register_frame)
pan_entry = tk.Entry(register_frame)
mobile_entry = tk.Entry(register_frame)
password_entry = tk.Entry(register_frame, show="*")

name_entry.grid(row=0, column=1)
aadhaar_entry.grid(row=1, column=1)
pan_entry.grid(row=2, column=1)
mobile_entry.grid(row=3, column=1)
password_entry.grid(row=4, column=1)

register_button = tk.Button(register_frame, text="Register", command=register_user)
register_button.grid(row=5, columnspan=2)

# Admin Login Form
admin_login_frame = tk.Frame(root)
admin_login_frame.pack(padx=10, pady=10)

tk.Label(admin_login_frame, text="Admin Username").grid(row=0, column=0)
tk.Label(admin_login_frame, text="Admin Password").grid(row=1, column=0)

admin_username_entry = tk.Entry(admin_login_frame)
admin_password_entry = tk.Entry(admin_login_frame, show="*")

admin_username_entry.grid(row=0, column=1)
admin_password_entry.grid(row=1, column=1)

admin_login_button = tk.Button(admin_login_frame, text="Admin Login", command=admin_login)
admin_login_button.grid(row=2, columnspan=2)

# Start Tkinter main loop
root.mainloop()
