from flask import render_template, redirect, url_for
from . import admin

@admin.route('/dashboard')
def dashboard():
    return render_template('shared/dashboard.html', current_page='dashboard')

@admin.route('/business')
def business():
    return render_template('shared/business.html', current_page='business')

@admin.route('/fsec')
def fsec():
    return render_template('shared/fsec.html', current_page='fsec')

@admin.route('/occupancy')
def occupancy():
    return render_template('shared/occupancy.html', current_page='occupancy')

@admin.route('/others')
def others():
    return render_template('shared/others.html', current_page='others')


@admin.route('/users')
def users():
    return render_template('admin/user_management.html', current_page='users')