from flask import render_template, redirect, url_for, request
from . import clerk

@clerk.route('/dashboard')
def dashboard():
    return render_template('shared/dashboard.html')