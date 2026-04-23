from flask import render_template, redirect, url_for
from . import admin

@admin.route('/dashboard')
def dashboard():
    return render_template('shared/dashboard.html')