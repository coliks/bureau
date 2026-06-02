from flask_login import UserMixin
from .services.connection import get_db_connection

class User(UserMixin):
    def __init__(self, id, name, email, contact, birthdate, address, password, avatar_url, role, status):
        self.id = id
        self.name = name
        self.email = email
        self.contact = contact
        self.birthdate = birthdate
        self.address = address
        self.password = password
        self.avatar_url = avatar_url
        self.role = role
        self.status = status
    
    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return User(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                contact=user_data.get('contact'),
                birthdate=user_data.get('birthdate'),
                address=user_data.get('address'),
                password=user_data['password'],
                avatar_url=user_data.get('avatar_url'),
                role=user_data['role'],
                status=user_data['status']
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return User(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                contact=user_data.get('contact'),
                birthdate=user_data.get('birthdate'),
                address=user_data.get('address'),
                password=user_data['password'],
                avatar_url=user_data.get('avatar_url'),
                role=user_data['role'],
                status=user_data['status']
            )
        return None
