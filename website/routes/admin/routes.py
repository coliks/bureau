from flask import render_template, redirect, url_for, flash, request, jsonify, current_app, make_response
from . import admin
from flask_login import login_required, current_user
from ...services.connection import get_db_connection
import os
import uuid
import json
from datetime import datetime

@admin.route('/dashboard')
@login_required
def dashboard():
    return render_template('shared/dashboard.html', current_page='dashboard')

@admin.route('/fsec')
@login_required
def fsec():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    fsec_records, total = get_fsec_records_paginated(page, per_page)
    businesses_like = [_fsec_record_to_business_like(row) for row in fsec_records]
    # archived records are shown in the modal, fetch all for that
    all_fsec = get_all_fsec_records()
    all_businesses_like = [_fsec_record_to_business_like(row) for row in all_fsec]
    total_pages = max(1, (total + per_page - 1) // per_page)
    return render_template(
        'shared/fsec.html',
        current_page='fsec',
        businesses=businesses_like,
        all_businesses=all_businesses_like,
        page=page,
        total_pages=total_pages,
        total=total,
    )

@admin.route('/fsec/add', methods=['POST'])
@login_required
def add_fsec():
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.fsec'))

    data = request.form

    project_title = (data.get('project_title') or '').strip()
    owner_name = (data.get('owner_name') or '').strip()
    address = (data.get('address') or '').strip()
    contact_number = (data.get('contact_number') or '').strip()

    if not project_title or not owner_name or not address or not contact_number:
        flash('Please fill up all required fields!', 'error')
        return redirect(url_for('admin.fsec'))

    filing_fee = (data.get('filing_fee') or '200').strip()
    hotworks_fee = (data.get('hotworks') or '500').strip()

    def empty_to_none(value):
        value = (value or '').strip()
        return value if value else None

    fsec_number = empty_to_none(data.get('fsec_number'))
    application_no = empty_to_none(data.get('application_no'))
    control_no = empty_to_none(data.get('control_no'))

    new_images = []
    if 'fsec_images' in request.files:
        files = request.files.getlist('fsec_images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = str(uuid.uuid4()) + '_' + file.filename
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file.save(os.path.join(upload_folder, filename))
                new_images.append(filename)

    images_json = json.dumps(new_images) if new_images else None

    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO fsec_records (
            project_title, owner_name, address,
            filing_fee, hotworks_fee,
            contact_number, fsec_number, application_no, control_no,
            status, fsec_images
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (
            project_title, owner_name, address,
            filing_fee, hotworks_fee,
            contact_number, fsec_number, application_no, control_no,
            'New', images_json
        )
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash('FSEC record added successfully!', 'success')
    return redirect(url_for('admin.fsec'))

@admin.route('/fsec/edit', methods=['POST'])
@login_required
def edit_fsec():
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.fsec'))

    data = request.form
    record_id = data.get('record_id')

    if not record_id:
        flash('Invalid record!', 'error')
        return redirect(url_for('admin.fsec'))

    existing_images = []
    if data.get('existing_fsec_images'):
        try:
            existing_images = json.loads(data['existing_fsec_images'])
        except Exception:
            existing_images = []

    new_images = []
    if 'fsec_images' in request.files:
        files = request.files.getlist('fsec_images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = str(uuid.uuid4()) + '_' + file.filename
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file.save(os.path.join(upload_folder, filename))
                new_images.append(filename)

    all_images = existing_images + new_images
    images_json = json.dumps(all_images) if all_images else None

    def empty_to_none(value):
        value = (value or '').strip()
        return value if value else None

    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE fsec_records SET
            project_title = %s,
            owner_name = %s,
            address = %s,
            contact_number = %s,
            filing_fee = %s,
            hotworks_fee = %s,
            fsec_number = %s,
            application_no = %s,
            control_no = %s,
            status = %s,
            fsec_images = %s
        WHERE id = %s
        ''',
        (
            (data.get('project_title') or '').strip(),
            (data.get('owner_name') or '').strip(),
            (data.get('address') or '').strip(),
            (data.get('contact_number') or '').strip(),
            (data.get('filing_fee') or '200').strip(),
            (data.get('hotworks_fee') or '500').strip(),
            empty_to_none(data.get('fsec_number')),
            empty_to_none(data.get('application_no')),
            empty_to_none(data.get('control_no')),
            (data.get('status') or 'New').strip(),
            images_json,
            record_id
        )
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash('FSEC record updated successfully!', 'success')
    return redirect(url_for('admin.fsec'))


@admin.route('/fsec/<int:record_id>/archive', methods=['POST'])
@login_required
def archive_fsec(record_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.fsec'))
    cursor = conn.cursor()
    cursor.execute('UPDATE fsec_records SET status = %s WHERE id = %s', ('Archived', record_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash('FSEC record archived successfully!', 'success')
    return redirect(url_for('admin.fsec'))


@admin.route('/fsec/<int:record_id>/retrieve', methods=['POST'])
@login_required
def retrieve_fsec(record_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.fsec'))
    cursor = conn.cursor()
    cursor.execute('UPDATE fsec_records SET status = %s WHERE id = %s', ('New', record_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash('FSEC record retrieved successfully!', 'success')
    return redirect(url_for('admin.fsec'))


@admin.route('/fsec/<int:record_id>/delete', methods=['POST'])
@login_required
def delete_fsec(record_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.fsec'))
    cursor = conn.cursor()
    cursor.execute('DELETE FROM fsec_records WHERE id = %s', (record_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('FSEC record deleted successfully!', 'success')
    return redirect(url_for('admin.fsec'))


@admin.route('/occupancy')
@login_required
def occupancy():
    page = request.args.get('page', 1, type=int)
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    per_page = 10
    records, total = get_occupancy_records_paginated(page, per_page, date_from, date_to)
    all_records = get_all_occupancy_records()
    total_pages = max(1, (total + per_page - 1) // per_page)
    return render_template(
        'shared/occupancy.html',
        current_page='occupancy',
        records=records,
        all_records=all_records,
        page=page,
        total_pages=total_pages,
        total=total,
        date_from=date_from,
        date_to=date_to,
    )

@admin.route('/occupancy/add', methods=['POST'])
@login_required
def add_occupancy():
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.occupancy'))

    data = request.form
    establishment_name = (data.get('establishment_name') or '').strip()
    owner_name = (data.get('owner_name') or '').strip()
    representative_name = (data.get('representative_name') or '').strip()
    address = (data.get('address') or '').strip()
    contact_number = (data.get('contact_number') or '').strip()
    fire_inspection_fee = (data.get('fire_inspection_fee') or '').strip()

    if not establishment_name or not owner_name or not representative_name or not address or not contact_number or not fire_inspection_fee:
        flash('Please fill up all required fields!', 'error')
        return redirect(url_for('admin.occupancy'))

    def empty_to_none(v):
        v = (v or '').strip()
        return v if v else None

    new_images = []
    if 'occupancy_images' in request.files:
        for file in request.files.getlist('occupancy_images'):
            if file and allowed_file(file.filename):
                filename = str(uuid.uuid4()) + '_' + file.filename
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file.save(os.path.join(upload_folder, filename))
                new_images.append(filename)

    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO occupancy_records
           (establishment_name, owner_name, representative_name, address, contact_number,
            fire_inspection_fee, control_no, application_no,
            building_permit_fee, zoning_fee, certificate_of_occupancy_fee,
            status, occupancy_images)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
        (establishment_name, owner_name, representative_name, address, contact_number,
         fire_inspection_fee,
         empty_to_none(data.get('control_no')),
         empty_to_none(data.get('application_no')),
         empty_to_none(data.get('building_permit_fee')),
         empty_to_none(data.get('zoning_fee')),
         empty_to_none(data.get('certificate_of_occupancy_fee')),
         'New',
         json.dumps(new_images) if new_images else None)
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash('Occupancy record added successfully!', 'success')
    return redirect(url_for('admin.occupancy'))

@admin.route('/occupancy/edit', methods=['POST'])
@login_required
def edit_occupancy():
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.occupancy'))

    data = request.form
    record_id = data.get('record_id')
    if not record_id:
        flash('Invalid record!', 'error')
        return redirect(url_for('admin.occupancy'))

    existing_images = []
    if data.get('existing_occupancy_images'):
        try:
            existing_images = json.loads(data['existing_occupancy_images'])
        except Exception:
            existing_images = []

    new_images = []
    if 'occupancy_images' in request.files:
        for file in request.files.getlist('occupancy_images'):
            if file and allowed_file(file.filename):
                filename = str(uuid.uuid4()) + '_' + file.filename
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file.save(os.path.join(upload_folder, filename))
                new_images.append(filename)

    all_images = existing_images + new_images

    def empty_to_none(v):
        v = (v or '').strip()
        return v if v else None

    cursor = conn.cursor()
    cursor.execute(
        '''UPDATE occupancy_records SET
           establishment_name=%s, owner_name=%s, representative_name=%s,
           address=%s, contact_number=%s,
           fire_inspection_fee=%s, control_no=%s, application_no=%s,
           building_permit_fee=%s, zoning_fee=%s, certificate_of_occupancy_fee=%s,
           status=%s, occupancy_images=%s
           WHERE id=%s''',
        ((data.get('establishment_name') or '').strip(),
         (data.get('owner_name') or '').strip(),
         (data.get('representative_name') or '').strip(),
         (data.get('address') or '').strip(),
         (data.get('contact_number') or '').strip(),
         (data.get('fire_inspection_fee') or '0').strip(),
         empty_to_none(data.get('control_no')),
         empty_to_none(data.get('application_no')),
         empty_to_none(data.get('building_permit_fee')),
         empty_to_none(data.get('zoning_fee')),
         empty_to_none(data.get('certificate_of_occupancy_fee')),
         (data.get('status') or 'New').strip(),
         json.dumps(all_images) if all_images else None,
         record_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash('Occupancy record updated successfully!', 'success')
    return redirect(url_for('admin.occupancy'))

@admin.route('/occupancy/<int:record_id>/archive', methods=['POST'])
@login_required
def archive_occupancy(record_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.occupancy'))
    cursor = conn.cursor()
    cursor.execute("UPDATE occupancy_records SET status='Archived' WHERE id=%s", (record_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Record archived successfully!', 'success')
    return redirect(url_for('admin.occupancy'))

@admin.route('/occupancy/<int:record_id>/retrieve', methods=['POST'])
@login_required
def retrieve_occupancy(record_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.occupancy'))
    cursor = conn.cursor()
    cursor.execute("UPDATE occupancy_records SET status='New' WHERE id=%s", (record_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Record retrieved successfully!', 'success')
    return redirect(url_for('admin.occupancy'))

@admin.route('/occupancy/<int:record_id>/delete', methods=['POST'])
@login_required
def delete_occupancy(record_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.occupancy'))
    cursor = conn.cursor()
    cursor.execute('DELETE FROM occupancy_records WHERE id=%s', (record_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Record deleted successfully!', 'success')
    return redirect(url_for('admin.occupancy'))

def get_all_occupancy_records():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM occupancy_records ORDER BY id DESC')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@admin.route('/occupancy/export', methods=['GET'])
@login_required
def export_occupancy():
    records = get_all_occupancy_records()

    headers = [
        ('establishment_name', 'Establishment Name'),
        ('owner_name', 'Owner Name'),
        ('representative_name', 'Representative Name'),
        ('contact_number', 'Contact Number'),
        ('address', 'Address'),
        ('control_no', 'Control No'),
        ('application_no', 'Application No'),
        ('fire_inspection_fee', 'Fire Inspection Fee'),
        ('building_permit_fee', 'Building Permit Fee'),
        ('zoning_fee', 'Zoning Fee'),
        ('certificate_of_occupancy_fee', 'Certificate of Occupancy Fee'),
        ('status', 'Status'),
        ('created_at', 'Created At'),
    ]

    rows_xml = []
    header_cells = ''.join(
        f'<Cell><Data ss:Type="String">{_xml_escape(label)}</Data></Cell>'
        for _, label in headers
    )
    rows_xml.append(f'<Row>{header_cells}</Row>')

    for rec in records:
        cells = []
        for key, _ in headers:
            value = rec.get(key)
            if isinstance(value, datetime):
                value = value.isoformat(sep=' ', timespec='seconds')
            cells.append(f'<Cell><Data ss:Type="String">{_xml_escape(value)}</Data></Cell>')
        rows_xml.append(f"<Row>{''.join(cells)}</Row>")

    sheet_xml = (
        '<?xml version="1.0"?>'
        '<?mso-application progid="Excel.Sheet"?>'
        '<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:x="urn:schemas-microsoft-com:office:excel" '
        'xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">'
        '<Worksheet ss:Name="Occupancy"><Table>'
        f'{"".join(rows_xml)}'
        '</Table></Worksheet></Workbook>'
    )

    filename = f"occupancy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xls"
    response = make_response(sheet_xml)
    response.headers['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.headers['Cache-Control'] = 'no-store'
    return response

def get_occupancy_records_paginated(page, per_page, date_from='', date_to=''):
    conn = get_db_connection()
    if not conn:
        return [], 0
    cursor = conn.cursor(dictionary=True)
    offset = (page - 1) * per_page

    conditions = ["status != 'Archived'"]
    params = []

    if date_from:
        conditions.append("DATE(created_at) >= %s")
        params.append(date_from)
    if date_to:
        conditions.append("DATE(created_at) <= %s")
        params.append(date_to)

    where = ' AND '.join(conditions)

    cursor.execute(f"SELECT COUNT(*) as cnt FROM occupancy_records WHERE {where}", params)
    total = cursor.fetchone()['cnt']
    cursor.execute(
        f"SELECT * FROM occupancy_records WHERE {where} ORDER BY id DESC LIMIT %s OFFSET %s",
        params + [per_page, offset]
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows, total

@admin.route('/others')
@login_required
def others():
    return render_template('shared/others.html', current_page='others')

def get_all_users():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users ORDER BY id DESC')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

@admin.route('/users')
@login_required
def users():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page!', 'error')
        return redirect(url_for('admin.dashboard'))
    all_users = get_all_users()
    pending_users = [user for user in all_users if user['status'] == 'pending']
    active_inactive_users = [user for user in all_users if user['status'] not in ['pending', 'archived']]
    archived_users = [user for user in all_users if user['status'] == 'archived']
    return render_template('admin/user_management.html', current_page='users', active_inactive_users=active_inactive_users, pending_users=pending_users, archived_users=archived_users)

@admin.route('/users/<int:user_id>/approve', methods=['POST'])
@login_required
def approve_user(user_id):
    if current_user.role != 'admin':
        return jsonify(success=False, message='Permission denied!'), 403
    conn = get_db_connection()
    if not conn:
        return jsonify(success=False, message='Database connection error!'), 500
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET status = %s WHERE id = %s', ('active', user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(success=True, message='User approved successfully!')

@admin.route('/users/<int:user_id>/freeze', methods=['POST'])
@login_required
def freeze_user(user_id):
    if current_user.role != 'admin':
        return jsonify(success=False, message='Permission denied!'), 403
    conn = get_db_connection()
    if not conn:
        return jsonify(success=False, message='Database connection error!'), 500
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET status = %s WHERE id = %s', ('archived', user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(success=True, message='User archived successfully!')

@admin.route('/users/<int:user_id>/unfreeze', methods=['POST'])
@login_required
def unfreeze_user(user_id):
    if current_user.role != 'admin':
        return jsonify(success=False, message='Permission denied!'), 403
    conn = get_db_connection()
    if not conn:
        return jsonify(success=False, message='Database connection error!'), 500
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET status = %s WHERE id = %s', ('active', user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(success=True, message='User unarchived successfully!')

@admin.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return jsonify(success=False, message='Permission denied!'), 403
    conn = get_db_connection()
    if not conn:
        return jsonify(success=False, message='Database connection error!'), 500
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(success=True, message='User deleted successfully!')

def get_all_businesses():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM businesses ORDER BY id DESC')
    businesses = cursor.fetchall()
    cursor.close()
    conn.close()
    return businesses

def get_all_fsec_records():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM fsec_records ORDER BY id DESC')
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

def get_fsec_records_paginated(page, per_page):
    conn = get_db_connection()
    if not conn:
        return [], 0
    cursor = conn.cursor(dictionary=True)
    offset = (page - 1) * per_page
    cursor.execute("SELECT COUNT(*) as cnt FROM fsec_records WHERE status != 'Archived'")
    total = cursor.fetchone()['cnt']
    cursor.execute("SELECT * FROM fsec_records WHERE status != 'Archived' ORDER BY id DESC LIMIT %s OFFSET %s", (per_page, offset))
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records, total

def get_businesses_paginated(page, per_page):
    conn = get_db_connection()
    if not conn:
        return [], 0
    cursor = conn.cursor(dictionary=True)
    offset = (page - 1) * per_page
    cursor.execute("SELECT COUNT(*) as cnt FROM businesses WHERE status != 'Archived'")
    total = cursor.fetchone()['cnt']
    cursor.execute("SELECT * FROM businesses WHERE status != 'Archived' ORDER BY id DESC LIMIT %s OFFSET %s", (per_page, offset))
    businesses = cursor.fetchall()
    cursor.close()
    conn.close()
    return businesses, total

def _fsec_record_to_business_like(record):
    business_id = record.get('fsec_number') or f"FSEC-{record.get('id')}"
    return {
        'id': record.get('id'),
        'business_id': business_id,
        'business_name': record.get('project_title') or '',
        'business_address': record.get('address') or '',
        'owner_name': record.get('owner_name') or '',
        'representative_name': '',
        'contact_number': record.get('contact_number') or '',
        'control_no': record.get('control_no') or '',
        'application_no': record.get('application_no') or '',
        'status': record.get('status') or 'New',
        'building_permit_fee': '0',
        'zoning_fee': '0',
        'occupancy_fee': '0',
        'fire_inspection_fee': str(record.get('filing_fee') or '0'),
        'hotworks_fee': str(record.get('hotworks_fee') or '500'),
        'or_no': '',
        'business_images': record.get('fsec_images'),
        'created_at': record.get('created_at'),
        'updated_at': record.get('updated_at'),
    }

def _xml_escape(value):
    if value is None:
        return ''
    text = str(value)
    return (
        text.replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&apos;')
    )

@admin.route('/business/export', methods=['GET'])
@login_required
def export_businesses():
    businesses = get_all_businesses()

    headers = [
        ('business_id', 'Business ID'),
        ('business_name', 'Business Name'),
        ('owner_name', 'Owner Name'),
        ('representative_name', 'Representative Name'),
        ('contact_number', 'Contact Number'),
        ('business_address', 'Business Address'),
        ('control_no', 'Control No'),
        ('application_no', 'Application No'),
        ('status', 'Status'),
        ('fire_inspection_fee', 'Fire Inspection Fee'),
        ('or_no', 'OR No'),
        ('created_at', 'Created At'),
    ]

    rows_xml = []
    header_cells = ''.join(
        f'<Cell><Data ss:Type="String">{_xml_escape(label)}</Data></Cell>'
        for _, label in headers
    )
    rows_xml.append(f'<Row>{header_cells}</Row>')

    for business in businesses:
        cells = []
        for key, _ in headers:
            value = business.get(key)
            if isinstance(value, datetime):
                value = value.isoformat(sep=' ', timespec='seconds')
            cells.append(f'<Cell><Data ss:Type="String">{_xml_escape(value)}</Data></Cell>')
        rows_xml.append(f"<Row>{''.join(cells)}</Row>")

    sheet_xml = (
        '<?xml version="1.0"?>'
        '<?mso-application progid="Excel.Sheet"?>'
        '<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:x="urn:schemas-microsoft-com:office:excel" '
        'xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">'
        '<Worksheet ss:Name="Businesses"><Table>'
        f'{"".join(rows_xml)}'
        '</Table></Worksheet></Workbook>'
    )

    filename = f"businesses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xls"
    response = make_response(sheet_xml)
    response.headers['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.headers['Cache-Control'] = 'no-store'
    return response

@admin.route('/business')
@login_required
def business():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    businesses, total = get_businesses_paginated(page, per_page)
    all_businesses = get_all_businesses()
    total_pages = max(1, (total + per_page - 1) // per_page)
    return render_template(
        'shared/business.html',
        current_page='business',
        businesses=businesses,
        all_businesses=all_businesses,
        page=page,
        total_pages=total_pages,
        total=total,
    )

@admin.route('/business/add', methods=['POST'])
@login_required
def add_business():
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.business'))
    
    data = request.form
    
    new_images = []
    if 'business_images' in request.files:
        files = request.files.getlist('business_images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = str(uuid.uuid4()) + '_' + file.filename
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file.save(os.path.join(upload_folder, filename))
                new_images.append(filename)
    
    images_json = json.dumps(new_images) if new_images else None
    
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO businesses (
            business_id, business_name, business_address, owner_name, 
            representative_name, contact_number, control_no, application_no, 
            status, building_permit_fee, zoning_fee, occupancy_fee, 
            fire_inspection_fee, or_no, business_images
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''',
        (
            data['business_id'], data['business_name'], data['business_address'],
            data['owner_name'], data['representative_name'], data['contact_number'],
            data.get('control_no', ''), data.get('application_no', ''), data['status'],
            data.get('building_permit_fee', '0'), data.get('zoning_fee', '0'), data.get('occupancy_fee', '0'),
            data['fire_inspection_fee'], data['or_no'], images_json
        )
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash('Business added successfully!', 'success')
    return redirect(url_for('admin.business'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@admin.route('/business/edit', methods=['POST'])
@login_required
def edit_business():
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.business'))
    
    data = request.form
    existing_images = []
    if data.get('existing_business_images'):
        try:
            existing_images = json.loads(data['existing_business_images'])
        except:
            existing_images = []
    
    new_images = []
    if 'business_images' in request.files:
        files = request.files.getlist('business_images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = str(uuid.uuid4()) + '_' + file.filename
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file.save(os.path.join(upload_folder, filename))
                new_images.append(filename)
    
    all_images = existing_images + new_images
    images_json = json.dumps(all_images) if all_images else None

    building_permit_fee = data.get('building_permit_fee')
    zoning_fee = data.get('zoning_fee')
    occupancy_fee = data.get('occupancy_fee')

    if building_permit_fee is None or zoning_fee is None or occupancy_fee is None:
        lookup_cursor = conn.cursor()
        lookup_cursor.execute(
            'SELECT building_permit_fee, zoning_fee, occupancy_fee FROM businesses WHERE id = %s',
            (data['business_id'],)
        )
        row = lookup_cursor.fetchone()
        lookup_cursor.close()
        if row:
            if building_permit_fee is None:
                building_permit_fee = row[0]
            if zoning_fee is None:
                zoning_fee = row[1]
            if occupancy_fee is None:
                occupancy_fee = row[2]
        else:
            if building_permit_fee is None:
                building_permit_fee = '0'
            if zoning_fee is None:
                zoning_fee = '0'
            if occupancy_fee is None:
                occupancy_fee = '0'
    
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE businesses SET
            business_id = %s,
            business_name = %s,
            business_address = %s,
            owner_name = %s,
            representative_name = %s,
            contact_number = %s,
            control_no = %s,
            application_no = %s,
            status = %s,
            building_permit_fee = %s,
            zoning_fee = %s,
            occupancy_fee = %s,
            fire_inspection_fee = %s,
            or_no = %s,
            business_images = %s
        WHERE id = %s
        ''',
        (
            data['business_id_code'], data['business_name'], data['business_address'],
            data['owner_name'], data['representative_name'], data['contact_number'],
            data.get('control_no', ''), data.get('application_no', ''), data['status'],
            building_permit_fee, zoning_fee, occupancy_fee,
            data['fire_inspection_fee'], data['or_no'], images_json, data['business_id']
        )
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash('Business updated successfully!', 'success')
    return redirect(url_for('admin.business'))

@admin.route('/business/<int:business_id>/archive', methods=['POST'])
@login_required
def archive_business(business_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.business'))
    
    cursor = conn.cursor()
    cursor.execute('UPDATE businesses SET status = %s WHERE id = %s', ('Archived', business_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Business archived successfully!', 'success')
    return redirect(url_for('admin.business'))

@admin.route('/business/<int:business_id>/retrieve', methods=['POST'])
@login_required
def retrieve_business(business_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.business'))
    
    cursor = conn.cursor()
    cursor.execute('UPDATE businesses SET status = %s WHERE id = %s', ('New', business_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Business retrieved successfully!', 'success')
    return redirect(url_for('admin.business'))

@admin.route('/business/<int:business_id>/delete', methods=['POST'])
@login_required
def delete_business(business_id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection error!', 'error')
        return redirect(url_for('admin.business'))
    
    cursor = conn.cursor()
    cursor.execute('DELETE FROM businesses WHERE id = %s', (business_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Business deleted successfully!', 'success')
    return redirect(url_for('admin.business'))
