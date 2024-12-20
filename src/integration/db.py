import psycopg2
from psycopg2 import sql
from datetime import datetime

# Function to connect to the PostgreSQL database
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="MyChatbotDB1.0",
            user="cesar",
            password="ParolaBDLicenta2025",
            host="db",  # Assuming the db service name in docker-compose.yml
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

# Function to create tables if they do not exist
def create_log_table():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS message_log (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                user_name TEXT NOT NULL,
                message_sent TEXT,
                message_received TEXT,
                voice_transcription TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            '''
            cursor.execute(create_table_query)
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Error creating log table: {e}")
        finally:
            conn.close()

# Function to save log data to the database
def save_message_log(user_id, user_name, message_sent, message_received, voice_transcription=None):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = '''
            INSERT INTO message_log (user_id, user_name, message_sent, message_received, voice_transcription)
            VALUES (%s, %s, %s, %s, %s);
            '''
            cursor.execute(insert_query, (user_id, user_name, message_sent, message_received, voice_transcription))
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Error saving log data: {e}")
        finally:
            conn.close()
