from flask import render_template, redirect, url_for, request, flash, jsonify
from . import auth
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ...services.connection import get_db_connection
from ...models import User

@auth.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.get_by_email(email)
        
        if user and check_password_hash(user.password, password):
            if user.status == 'active':
                login_user(user, remember=True)
                return redirect(url_for('admin.dashboard'))
            elif user.status == 'pending':
                flash('Your account is waiting for admin approval!', 'error')
                return render_template('auth/login.html', current_page='login')
            else:
                flash('Account is inactive!', 'error')
                return render_template('auth/login.html', current_page='login')
        else:
            flash('Invalid email or password!', 'error')
            return render_template('auth/login.html', current_page='login')
            
    return render_template('auth/login.html', current_page='login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['POST', 'GET'])
def register_account():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        fname = request.form.get('first-name')
        lname = request.form.get('last-name')
        email = request.form.get('email')
        contact = request.form.get('contact-no')
        password1 = request.form.get('password-1')
        password2 = request.form.get('password-2')

        fields = [fname, lname, email, contact, password1, password2]
        
        fullname = f'{fname} {lname}'

        for field in fields:
            if field == '':
                return jsonify(success=False, message="Failed empty fields.")
        
        if password1 != password2:
            return jsonify(success=False, message='Password does not match!')
        
        # Check if email already exists
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        if cursor.fetchone():
            return jsonify(success=False, message='Email already registered!')
        
        # Hash the password
        hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')
        
        # Insert new user
        cursor.execute(
            'INSERT INTO users (name, email, contact, password, role, status) VALUES (%s, %s, %s, %s, %s, %s)',
            (fullname, email, contact, hashed_password, 'clerk', 'pending')
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(success=True, message='Account created successfully!')

    return render_template('auth/signup.html', current_page='sign_up')