import mysql.connector
import bcrypt
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Harish@0710",
        database="expenses"
    )

def login(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        stored_hash = user['password'].encode('utf-8') if isinstance(user['password'],str) else user['password']

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return True
    return False

def register(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False
    
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO Users (username, password) VALUES (%s, %s)",(username, hashed_pw))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_user_id(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM Users WHERE username = %s", (username, ))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def insert_budget(username, month, amount):
    user_id = get_user_id(username)
    if user_id:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO budgets (user_id, month, amount) VALUES (%s, %s, %s)", (user_id, month, amount))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
def fetch_budgets(username):
    user_id = get_user_id(username)
    if user_id:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * from budgets WHERE user_id = %s", (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    

def check_month(username, month):
    user_id = get_user_id(username)
    if user_id:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT month FROM budgets WHERE user_id = %s and month = %s",(user_id, month))
        r = cursor.fetchone()
        cursor.close()
        conn.close()
        return True if r else False 
    
def insert_expenses(username, date, category, amount, payment_mode):
    user_id = get_user_id(username)
    if user_id:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Expenses (user_id, date, category, amount, payment_mode)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, date, category, amount, payment_mode))
        conn.commit()
        cursor.close()
        conn.close()
        return True

def fetch_expenses(username, month):
    user_id = get_user_id(username)
    if user_id:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Expenses WHERE user_id = %s and DATE_FORMAT(date, '%Y-%m') = %s", (user_id, month))
        r = cursor.fetchall()
        cursor.close()
        conn.close()
        return r
    else:
        return None
    
def fetch_month_budget(username, month):
    user_id = get_user_id(username)
    if user_id:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM budgets WHERE user_id = %s and month = %s", (user_id, month))
        am = cursor.fetchone()
        cursor.close()
        conn.close()
        return am[0]
    else:
        return None

def fetch_expense_for_delete(username):
    user_id = get_user_id(username)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT expense_id, category, amount, date FROM expenses WHERE user_id = %s ORDER BY date DESC", (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    df = pd.DataFrame(rows, columns=['expense_id', 'category', 'amount','date'])
    return df

def delete_expense(username, expense_id):
    user_id = get_user_id(username)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE user_id = %s and expense_id = %s", (user_id, expense_id))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def fetch_expenses_user(username):
    user_id = get_user_id(username)
    if user_id:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Expenses WHERE user_id = %s", (user_id,))
        r = cursor.fetchall()
        cursor.close()
        conn.close()
        return r
    else:
        return None