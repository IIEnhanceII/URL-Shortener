import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def short_code_exists(pipiurl):
    """
    Checks whether a short code already exists in the database.
    Returns True if exists, False otherwise.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT 1 FROM dmforlink WHERE pipiurl = %s LIMIT 1"
    cursor.execute(query, (pipiurl,))

    exists = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return exists


def insert_url(original, pipiurl):
    """
    Inserts a new URL mapping into the database.
    Raises an exception if insertion fails.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = "INSERT INTO dmforlink (original, pipiurl) VALUES (%s, %s)"
        cursor.execute(query, (original, pipiurl))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()


def get_original(pipiurl):
    """
    Fetches the original URL using the short code.
    Returns the original URL if found, otherwise None.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT original FROM dmforlink WHERE pipiurl = %s"
    cursor.execute(query, (pipiurl,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]
    return None
