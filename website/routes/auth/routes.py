from flask import render_template, redirect, url_for, request, flash, jsonify
from . import auth

from ...services.connection import get_db_connection

@auth.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('auth/login.html', current_page='login')

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
            raise jsonify(success=False, message='Password does not match!')
        

        return jsonify(success=True, message='Account created successfully!')

    return render_template('auth/signup.html', current_page='sign_up')