from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from flask_mail import Message, Mail

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key')  # Ensure this is stored securely
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout (30 minutes)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.housing_ecard
users_collection = db.users
ecard_history_collection = db.ecard_history  # History collection

# Email setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 's.p.d.o.w2452016@gmail.com'  # Your Gmail email
app.config['MAIL_PASSWORD'] = 'jnxo dgeq htrd lqnp'  # Use the generated App Password for Gmail
mail = Mail(app)

# E-card save directory
ECARD_SAVE_DIR = 'static/ecards/'  # Folder to save e-cards for future downloads
os.makedirs(ECARD_SAVE_DIR, exist_ok=True)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        aadhaar = request.form['aadhaar']
        pan = request.form['pan']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']

        if not name or not aadhaar or not pan or not mobile or not password:
            flash('All fields are required!', 'error')
            return render_template('register.html')

        if len(aadhaar) != 12 or not aadhaar.isdigit():
            flash('Invalid Aadhaar number!', 'error')
            return render_template('register.html')
        if len(pan) != 10 or not pan.isalnum():
            flash('Invalid PAN number!', 'error')
            return render_template('register.html')
        if len(mobile) != 10 or not mobile.isdigit():
            flash('Invalid mobile number!', 'error')
            return render_template('register.html')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = {
            'name': name,
            'aadhaar': aadhaar,
            'pan': pan,
            'mobile': mobile,
            'email': email,
            'status': 'In process',  # Default status
            'password': hashed_password
        }

        users_collection.insert_one(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'name': username})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = str(user['_id'])
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html')

    return render_template('login.html')


# Admin login route (with secure hashed password)
hashed_admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and bcrypt.checkpw(password.encode('utf-8'), hashed_admin_password):
            session['admin'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid admin credentials', 'error')
            return render_template('admin_login.html')

    # For GET request, render the login page
    return render_template('admin_login.html')


# Admin dashboard route
@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin'))

    users = users_collection.find({'status': 'In process'})
    return render_template('dashboard.html', users=users)

# View User route
@app.route('/view_user/<user_id>')
def view_user(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('dashboard'))
    return render_template('view_user.html', user=user)

# Update user status (approve/reject)
@app.route('/update_status/<user_id>/<status>', methods=['GET'])
def update_status(user_id, status):
    if status not in ['Approved', 'Rejected', 'In process']:
        return 'Invalid status', 400

    result = users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'status': status}}
    )

    if result.modified_count > 0:
        flash('Status updated successfully!', 'success')
        # You can add a check here to trigger actions on status change (e.g., generate e-card if approved)
        if status == 'Approved':
            return generate_ecard(user_id)  # Call e-card generation if approved
        return redirect(url_for('dashboard'))
    else:
        flash('Error updating status', 'error')
        return redirect(url_for('dashboard'))


# E-card generation (PDF) and sending via email
@app.route('/generate_ecard/<user_id>')
def generate_ecard(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)})

    # Get approval info (add the approved_by field in the users collection)
    approved_by = "approved by @darshan_sachin_wadke"  # Placeholder for admin name
    status = user.get('status', 'In process')  # Get status (default to 'In process')

    # Generate PDF e-card
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Set background color for card
    c.setFillColorRGB(0.8, 0.9, 0.9)  # Light blue color for background
    c.rect(30, 600, 550, 150, fill=1)  # Background for the main card area

    # Title: E-card Heading
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(200, 740, "Housing E-card")

    # User Details Section (Name, Aadhaar, PAN, Mobile)
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)

    # Name
    c.drawString(40, 670, f"Name: {user['name']}")
    # Aadhaar
    c.drawString(40, 650, f"Aadhaar: {user['aadhaar']}")
    # PAN
    c.drawString(40, 630, f"PAN: {user['pan']}")
    # Mobile
    c.drawString(40, 610, f"Mobile: {user['mobile']}")

    # Status and Approved By (Admin info)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 590, f"Status: {status}")
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(40, 570, f"{approved_by}")  # Show who approved it

    # Draw a line separator for the footer
    c.setFillColorRGB(0.6, 0.6, 0.6)
    c.rect(30, 600, 550, 1, fill=1)

    # Footer Section: Additional Information
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.drawString(200, 40, "For official use only")
    c.drawString(40, 40, "Issued by Housing Society")

    # Finalize the card design
    c.showPage()
    c.save()

    buffer.seek(0)

    # Save the PDF e-card to the server's filesystem
    ecard_filename = f"{user['name']}_ecard.pdf"
    ecard_path = os.path.join(ECARD_SAVE_DIR, ecard_filename)
    with open(ecard_path, 'wb') as f:
        f.write(buffer.read())

    # Email the e-card
    msg = Message("Your E-card", recipients=[user['email']])
    msg.body = "Please find your e-card attached."
    msg.attach(ecard_filename, "application/pdf", buffer.read())

    try:
        mail.send(msg)
        flash('E-card sent successfully!', 'success')

        # Update e-card history
        ecard_history_collection.insert_one({
            'user_id': user_id,
            'ecard_generated_on': datetime.now(),
            'status': 'Generated',
            'ecard_path': ecard_path  # Save the path to the e-card
        })
    except Exception as e:
        flash(f"Error sending e-card: {e}", 'error')
        print(f"Email sending failed: {e}")

    return redirect(url_for('dashboard'))

# E-card download route (for admin or user)
@app.route('/download_ecard/<user_id>')
def download_ecard(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)})

    # Get the e-card file path from the database
    ecard_data = ecard_history_collection.find_one({'user_id': user_id, 'status': 'Generated'})
    if not ecard_data:
        flash('E-card not generated yet', 'error')
        return redirect(url_for('dashboard'))

    ecard_path = ecard_data.get('ecard_path')
    if not ecard_path or not os.path.exists(ecard_path):
        flash('E-card not found', 'error')
        return redirect(url_for('dashboard'))

    return send_file(ecard_path, as_attachment=True, download_name=f"{user['name']}_ecard.pdf", mimetype='application/pdf')

@app.route('/delete_user/<user_id>', methods=['GET'])
def delete_user(user_id):
    result = users_collection.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count > 0:
        flash('User deleted successfully!', 'success')
    else:
        flash('Error deleting user', 'error')
    return redirect(url_for('dashboard'))


# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('admin', None)  # Remove admin session as well
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
