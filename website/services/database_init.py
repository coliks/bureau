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

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS businesses (
      id INT AUTO_INCREMENT PRIMARY KEY,
      business_id VARCHAR(255) NOT NULL,
      business_name VARCHAR(255) NOT NULL,
      business_address VARCHAR(500) NOT NULL,
      owner_name VARCHAR(255) NOT NULL,
      representative_name VARCHAR(255) NOT NULL,
      contact_number VARCHAR(20) NOT NULL,
      control_no VARCHAR(255) NOT NULL,
      application_no VARCHAR(255) NOT NULL,
      status VARCHAR(20) NOT NULL,
      building_permit_fee DECIMAL(10,2) NOT NULL,
      zoning_fee DECIMAL(10,2) NOT NULL,
      occupancy_fee DECIMAL(10,2) NOT NULL,
      fire_inspection_fee DECIMAL(10,2) NOT NULL,
      or_no VARCHAR(255) NOT NULL,
      business_images TEXT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS fsec_records (
      id INT AUTO_INCREMENT PRIMARY KEY,
      project_title VARCHAR(255) NOT NULL,
      owner_name VARCHAR(255) NOT NULL,
      address VARCHAR(500) NOT NULL,
      filing_fee DECIMAL(10,2) NOT NULL DEFAULT 200.00,
      hotworks_fee DECIMAL(10,2) NOT NULL DEFAULT 500.00,
      contact_number VARCHAR(20) NOT NULL,
      fsec_number VARCHAR(255) NULL,
      application_no VARCHAR(255) NULL,
      control_no VARCHAR(255) NULL,
      status VARCHAR(20) NOT NULL DEFAULT 'New',
      fsec_images TEXT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
"""
    )
    
    cursor.execute(
        """
    ALTER TABLE businesses ADD COLUMN IF NOT EXISTS business_images TEXT NULL
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS occupancy_records (
      id INT AUTO_INCREMENT PRIMARY KEY,
      establishment_name VARCHAR(255) NOT NULL,
      owner_name VARCHAR(255) NOT NULL,
      representative_name VARCHAR(255) NOT NULL,
      address VARCHAR(500) NOT NULL,
      contact_number VARCHAR(20) NOT NULL,
      control_no VARCHAR(255) NULL,
      application_no VARCHAR(255) NULL,
      building_permit_fee DECIMAL(10,2) NULL,
      zoning_fee DECIMAL(10,2) NULL,
      certificate_of_occupancy_fee DECIMAL(10,2) NULL,
      fire_inspection_fee DECIMAL(10,2) NOT NULL DEFAULT 0.00,
      status VARCHAR(20) NOT NULL DEFAULT 'New',
      occupancy_images TEXT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
"""
    )

    conn.commit()
    cursor.close()
    conn.close()
    
