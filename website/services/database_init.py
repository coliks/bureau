from .connection import get_db_connection


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      email VARCHAR(255) NOT NULL,
      contact VARCHAR(20) NULL,
      birthdate DATE NULL,
      address VARCHAR(500) NULL,
      password VARCHAR(255) NOT NULL,
      avatar_url VARCHAR(500) NULL,
      role VARCHAR(20) NOT NULL,
      status VARCHAR(20) NOT NULL
    )
"""
    )
    conn.commit()
    cursor.close()
    conn.close()
    
