from flask import render_template, redirect, url_for, request
from . import auth

@auth.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('auth/login.html', current_page='login')

@auth.route('/register', methods=['POST', 'GET'])
def register_account():
    return render_template('auth/signup.html', current_page='sign_up')