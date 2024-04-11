from datetime import datetime
from app import get_db_connection
import psycopg2
import psycopg2.extras

# Funciones para manejar usuarios
def add_user(name, paid=False):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, paid, payment_date) VALUES (%s, %s, %s)",
                (name, paid, None))
    conn.commit()
    cur.close()
    conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

def get_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def update_payment_status(user_id, paid):
    conn = get_db_connection()
    cur = conn.cursor()
    if paid:
        cur.execute("UPDATE users SET paid = TRUE, payment_date = %s WHERE id = %s", (datetime.now(), user_id))
    else:
        cur.execute("UPDATE users SET paid = FALSE, payment_date = NULL WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

def add_financial_event(amount):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO financial_events (amount, date) VALUES (%s, %s)", (amount, datetime.now()))
    conn.commit()
    cur.close()
    conn.close()

def delete_financial_event(event_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM financial_events WHERE id = %s", (event_id,))
    conn.commit()
    cur.close()
    conn.close()

def get_financial_events():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM financial_events")
    events = cur.fetchall()
    cur.close()
    conn.close()
    return events

def reset_payment_status(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET paid = FALSE, payment_date = NULL WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
