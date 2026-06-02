from website.services.connection import get_db_connection
from werkzeug.security import generate_password_hash

def create_default_users():
    conn = get_db_connection()
    if not conn:
        print("Could not connect to the database!")
        return
    
    cursor = conn.cursor(dictionary=True)
    
    default_users = [
        {
            'name': 'Admin User',
            'email': 'admin@example.com',
            'contact': '09123456789',
            'password': 'admin123',
            'role': 'admin',
            'status': 'active'
        },
        {
            'name': 'Clerk User',
            'email': 'clerk@example.com',
            'contact': '09987654321',
            'password': 'clerk123',
            'role': 'clerk',
            'status': 'active'
        }
    ]
    
    for user in default_users:
        # Check if user already exists
        cursor.execute('SELECT * FROM users WHERE email = %s', (user['email'],))
        if cursor.fetchone():
            print(f"User with email {user['email']} already exists, skipping.")
            continue
        
        hashed_password = generate_password_hash(user['password'], method='pbkdf2:sha256')
        
        cursor.execute(
            'INSERT INTO users (name, email, contact, password, role, status) VALUES (%s, %s, %s, %s, %s, %s)',
            (user['name'], user['email'], user['contact'], hashed_password, user['role'], user['status'])
        )
        print(f"Added default user: {user['email']}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Default users creation complete!")

if __name__ == '__main__':
    create_default_users()
