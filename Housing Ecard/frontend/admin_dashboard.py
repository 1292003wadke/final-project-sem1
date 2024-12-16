import tkinter as tk
from tkinter import messagebox
import requests

# Function to update user status
def update_user_status(user_id, status):
    try:
        # Send a GET request to update the user status in the backend
        response = requests.get(f'http://127.0.0.1:5000/update_status/{user_id}/{status}')
        
        if response.status_code == 200:
            messagebox.showinfo('Success', f'User status updated to {status}')
            # Optionally refresh the dashboard after updating
            refresh_user_list()
        else:
            messagebox.showerror('Error', 'Failed to update status')
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error', f'Error connecting to backend: {e}')

# Function to refresh the user list (you can make a backend request to fetch updated data)
def refresh_user_list():
    # Clear the window and reload the user list
    for widget in root.winfo_children():
        widget.destroy()
    
    load_users()

# Function to load and display users
def load_users():
    # Sample users (replace with dynamic data from backend)
    users = [
        {'id': '123', 'name': 'John Doe', 'status': 'In process'},
        {'id': '124', 'name': 'Jane Smith', 'status': 'In process'}
    ]
    
    # Display the user list with options to approve/reject
    for user in users:
        user_frame = tk.Frame(root)
        user_frame.pack(pady=5, fill='x', padx=20)
        
        user_label = tk.Label(user_frame, text=f"{user['name']} ({user['status']})", anchor='w')
        user_label.pack(side='left', padx=10)
        
        # Approve Button
        approve_button = tk.Button(user_frame, text="Approve", command=lambda user_id=user['id']: update_user_status(user_id, 'Approved'))
        approve_button.pack(side='left', padx=5)
        
        # Reject Button
        reject_button = tk.Button(user_frame, text="Reject", command=lambda user_id=user['id']: update_user_status(user_id, 'Rejected'))
        reject_button.pack(side='left', padx=5)

# Create the Tkinter window for Admin Dashboard
root = tk.Tk()
root.title("Housing Ecard - Admin Dashboard")

# Load users when the dashboard opens
load_users()

# Start the Tkinter event loop
root.mainloop()
