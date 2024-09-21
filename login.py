import streamlit as st
import psycopg2
import re
from passlib.context import CryptContext
import test

# Database connection details
DB_HOST = "localhost"
DB_NAME = "project_DRONA_db"
DB_USER = "DRONA_user"
DB_PASSWORD = "kaliyug"
DB_PORT = 5432  # Default PostgreSQL port

# Hashing context for password storage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def connect_to_postgres():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def register_user(username, password, email, mobile):
    conn = connect_to_postgres()
    if conn is None:
        return False, "Database connection error."

    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 1 FROM users WHERE username = %s OR email = %s OR mobile = %s
        """, (username, email, mobile))
        existing_user = cursor.fetchone()

        if existing_user:
            return False, "Username, email, or mobile number already exists."

        # Hash the password and insert new user
        hashed_password = pwd_context.hash(password)
        cursor.execute("""
            INSERT INTO users (username, hashed_password, email, mobile) VALUES (%s, %s, %s, %s)
        """, (username, hashed_password, email, mobile))
        conn.commit()
        return True, "Registration successful!"
    except Exception as e:
        print(f"Error registering user: {e}")
        return False, "Error registering user."
    finally:
        cursor.close()
        conn.close()

def validate_login(username, password):
    conn = connect_to_postgres()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT hashed_password FROM users WHERE username = %s
        """, (username,))
        stored_password = cursor.fetchone()
        if stored_password is None:
            return False  # Username not found

        # Verify password using the hashing context
        if pwd_context.verify(password, stored_password[0]):
            st.session_state["username"] = username
            return True
        return False
    except Exception as e:
        print(f"Error validating login: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def apply_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-size: 100% 100%;
            background-position: 0px 0px;
            background-image: linear-gradient(174deg, #6D00B7FF 0%, #228080FF 96%);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show_login():
    st.title("Login")
    apply_css()
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("Username", key="login_username_input")
        password = st.text_input("Password", type="password", key="login_password_input")
        login_button = st.button("Login", key="login_button")

    if login_button:
        if not username or not password:
            st.error("Both fields are required.")
        elif validate_login(username, password):
            st.session_state["logged_in"] = True
            st.success("Login successful!")
            st.rerun()  # Refresh the page to load the main app
        else:
            st.error("Invalid username or password")
    
    with col2:
        register_button = st.button("Register", key="register_button")

    # Show register page if the register button is clicked
    if register_button:
        st.session_state["show_register"] = True
        st.session_state["show_login"] = False
        st.rerun()  # Refresh to show the register page

def show_register_page():
    st.title("Register")
    apply_css()
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        new_username = st.text_input("New Username", key="register_username_input")
        new_password = st.text_input("New Password", type="password", key="register_password_input")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password_input")
        email = st.text_input("Email", key="email_input")
        mobile = st.text_input("Mobile Number", key="mobile_input")
        register_button = st.button("Register", key="register_button_register")

    if register_button:
        if not new_username or not new_password or not confirm_password or not email or not mobile:
            st.error("All fields are required.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("Invalid email format.")
        elif not re.match(r"^\d{10}$", mobile):
            st.error("Invalid mobile number format.")
        else:
            success, message = register_user(new_username, new_password, email, mobile)
            if success:
                st.success(message)
                st.session_state["show_register"] = False
                st.session_state["show_login"] = True
                st.rerun()  # Refresh the page to go back to login page
            else:
                st.error(message)
    
    with col2:
        login_button = st.button("Back to Login", key="back_to_login_button")

    if login_button:
        st.session_state["show_register"] = False
        st.session_state["show_login"] = True
        st.rerun()  # Back to login page

# Initialize session state for login/register visibility
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "show_login" not in st.session_state:
    st.session_state["show_login"] = True
if "show_register" not in st.session_state:
    st.session_state["show_register"] = False

# Main logic to show login or register page based on session state
if not st.session_state["logged_in"]:
    if st.session_state["show_login"]:
        show_login()
    elif st.session_state["show_register"]:
        show_register_page()
else:
    st.sidebar.write(f"Welcome Back, {st.session_state.get('username', 'User')}!")
    sign_out = st.sidebar.button("Sign Out", key="sign_out_button")

    if sign_out:
        st.session_state["logged_in"] = False
        st.session_state["show_login"] = True
        st.rerun()

    test.show()  # Call the main application function
