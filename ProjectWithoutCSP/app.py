from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory, make_response
from flask_session import Session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)


# Root URL
@app.route('/')
def index():
    if 'user_data' in session:
        # Gather all files uploaded by all users
        files_by_all_users = []
        user_upload_dir = os.path.join('uploads')
        for username in os.listdir(user_upload_dir):
            if os.path.isdir(os.path.join(user_upload_dir, username)):
                user_files = os.listdir(os.path.join(user_upload_dir, username))
                for file in user_files:
                    files_by_all_users.append({'username': username, 'filename': file})
        
        return render_template('index.html', files=files_by_all_users)
    else:
        return redirect('/login')

# Root URL
@app.route('/index')
def home():
    if 'user_data' in session:
        return redirect('/')
    else:
        return redirect('/login')
	
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_data' in session:
        user_data = session['user_data']
        profile_picture = user_data.get('ProfilePicture')
        return render_template('dashboard.html', user_data=user_data, profile_picture=profile_picture)
    else:
        return redirect('/login')



# Login GET
@app.route('/login', methods=['GET'])
def login():
    if 'user_data' in session:
        return redirect('/dashboard')
    error = request.args.get('error')
    return render_template('login.html', error=error)


# Login
@app.route('/login', methods=['POST'])
def login_process():
    username = request.form['username']
    password = request.form['password']
    
    # Check if the user exists in the user_data.txt file
    user_data = get_user_data(username)
    if user_data and user_data['Password'] == password:
        # Save the login information to the login_data.txt file
        with open('login_data.txt', 'a') as file:
            file.write(f'Username: {username}, Password: {password}\n')
        session['user_data'] = user_data
        return redirect('/index')
    else:
        return render_template('login.html', error='Invalid username or password')

    
# Helper function to get user data from the text file
def get_user_data(username):
    with open('user_data.txt', 'r') as file:
        for line in file:
            if f'Username: {username}' in line:
                user_data = {}
                parts = line.split(', ')
                for data in parts:
                    if ':' in data:
                        key, value = data.split(': ')
                        user_data[key] = value
                return user_data
    return None


# Logout
@app.route('/logout')
def logout():
    # Remove the user data from the session
    session.pop('user_data', None)
    # Clear the cookies by setting their expiration time to a past date
    response = make_response(redirect('/login'))
    response.set_cookie('username', '', expires=0)
    # Add more cookies if you have set more

    return response
    
# Signup GET
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')
    
    
#helper function for signup same user name
def username_exists(username):
    # Check if the username already exists in user_data.txt
    with open('user_data.txt', 'r') as file:
        for line in file:
            if f'Username: {username}' in line:
                return True
    return False

# Signup
@app.route('/signup', methods=['POST'])
def signup_process():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    middle_name = request.form['middleName']
    date_of_birth = request.form['dob']
    favorite_color = request.form['favoriteColor']
    profile_picture = request.files['profilePicture']
    address = request.form['address']
    phone_number = request.form['phoneNumber']
    email = request.form['email']
    about = request.form['about']

    # Check if the username already exists
    if username_exists(username):
        # Return the error message to the template
        return render_template('signup.html', error='Username already exists. Please choose a different one.')
    else:
        # Save the user information to the user_data.txt file
        with open('user_data.txt', 'a') as file:
            file.write(f'Username: {username}, Password: {password}, First Name: {first_name}, Last Name: {last_name}, Middle Name: {middle_name}, Date of Birth: {date_of_birth}, Favorite Color: {favorite_color}, Address: {address}, Phone Number: {phone_number}, Email: {email}, About: {about}\n')
        return redirect('/dashboard')


# Update profile
@app.route('/update', methods=['GET'])
def update():
    if 'user_data' in session:
        user_data = get_user_data(session['user_data']['Username'])
        if user_data:
            return render_template('update.html', user_data=user_data)
        else:
            return "User data not found"
    else:
        return redirect('/login')



# Update profile
@app.route('/update', methods=['POST'])
def update_process():
    if 'user_data' in session:
        username = session['user_data']['Username']
        
        # Get the updated form data
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        middle_name = request.form.get('middleName')
        date_of_birth = request.form.get('dob')
        favorite_color = request.form.get('favoriteColor')
        password = request.form.get('password')
        profile_picture = request.files.get('profilePicture')
        if profile_picture:
            # Ensure a secure filename
            filename = secure_filename(profile_picture.filename)
            # Save the uploaded profile picture to the user's directory
            profile_picture.save(os.path.join('uploads', username, filename))
        address = request.form.get('address')
        phone_number = request.form.get('phoneNumber')
        email = request.form.get('email')
        about = request.form.get('about')
        
        # Load the user data from the file
        with open('user_data.txt', 'r') as file:
            lines = file.readlines()
        
        # Find the line with the current user's data and update it
        for i, line in enumerate(lines):
            if f'Username: {username}' in line:
                user_data_parts = line.strip().split(', ')
                updated_user_data = [
                    f'Username: {username}',
                    f'Password: {password}',
                    f'First Name: {first_name}',
                    f'Last Name: {last_name}',
                    f'Middle Name: {middle_name}',
                    f'Date of Birth: {date_of_birth}',
                    f'Favorite Color: {favorite_color}',
                    f'Address: {address}',
                    f'Phone Number: {phone_number}',
                    f'Email: {email}',
                    f'About: {about}'
                ]
                lines[i] = ', '.join(updated_user_data) + '\n'
                break
        
        # Write the updated user data back to the file
        with open('user_data.txt', 'w') as file:
            file.writelines(lines)
        
        # Update the session with the new user data
        session['user_data']['First Name'] = first_name
        session['user_data']['Last Name'] = last_name
        session['user_data']['Middle Name'] = middle_name
        session['user_data']['Date of Birth'] = date_of_birth
        session['user_data']['Favorite Color'] = favorite_color
        session['user_data']['Address'] = address
        session['user_data']['Phone Number'] = phone_number
        session['user_data']['Email'] = email
        session['user_data']['About'] = about
        session['user_data']['ProfilePicture'] = filename
        
        return redirect('/dashboard')
    else:
        return redirect('/login')

        
# File upload
@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

# File upload
@app.route('/upload', methods=['POST'])
def upload_process():
    if 'user_data' in session:
        file = request.files['file']
        username = session['user_data']['Username']
        user_upload_dir = os.path.join('uploads', username)
        
        # Create the user's directory if it doesn't exist
        if not os.path.exists(user_upload_dir):
            os.makedirs(user_upload_dir)
        
        # Save the uploaded file to the user's directory
        file_path = os.path.join(user_upload_dir, file.filename)
        file.save(file_path)
        
        # Log the file upload in a text file
        with open('upload_log.txt', 'a') as f:
            f.write(f'Uploaded file: {file_path}\n')
        
        # Generate URL for the uploaded file
        file_url = url_for('uploaded_file', username=username, filename=file.filename, _external=True)
        
        # Render the upload.html template with the file URL
        return render_template('upload.html', file_url=file_url)
    else:
        return redirect('/login')
        
# Serve uploaded files
@app.route('/uploads/<username>/<filename>')
def uploaded_file(username, filename):
    return send_from_directory(os.path.join('uploads', username), filename)


# Route for the XSS snippets page
@app.route('/xss_snippets', methods=['GET', 'POST'])
def xss_snippets():
    if request.method == 'POST':
        # Get the JavaScript code from the form
        javascript_code = request.form.get('javascript_code')
        
        # Store the JavaScript code (You can replace this with your preferred storage method)
        with open('xss_snippets.txt', 'a') as file:
            file.write(javascript_code + '\n')
        
        # Redirect to the snippets page after submission
        return redirect('/snippets')
    else:
        # Render the XSS snippets page template
        return render_template('xss_snippets.html')



@app.route('/snippets')
def snippets():
    # Load XSS snippets data from the file (You can replace this with your preferred data loading method)
    snippets = []
    if os.path.exists('xss_snippets.txt'):
        with open('xss_snippets.txt', 'r') as file:
            snippets = file.readlines()

    # Render the snippets page template with the XSS snippets data
    # Ensure that the snippets are rendered as raw HTML to enable execution of JavaScript
    return render_template('snippets.html', snippets=snippets)

# Route for serving profile pictures
@app.route('/profile_picture/<username>/<filename>')
def profile_picture(username, filename):
    return send_from_directory(os.path.join('uploads', username), filename)






if __name__ == '__main__':
    app.run()

