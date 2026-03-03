import streamlit as st
import bcrypt
from utils.logger import log_info, log_error

# -----------------------------
# Hash Password
# -----------------------------
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# -----------------------------
# Verify Password
# -----------------------------
def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)

# -----------------------------
# SIGN UP FUNCTION
# -----------------------------
def signup(cursor, db):

    st.subheader("📝 Create New Account")

    new_username = st.text_input("Choose Username")
    new_password = st.text_input("Choose Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    role = st.selectbox("Select Role", ["Manager", "Admin"])

    if st.button("Sign Up"):

        if not new_username or not new_password:
            st.warning("All fields are required.")
            return

        if new_password != confirm_password:
            st.error("Passwords do not match.")
            return

        # Check if username exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (new_username,))
        existing_user = cursor.fetchone()

        if existing_user:
            st.error("Username already exists.")
            return

        try:
            hashed_pw = hash_password(new_password)

            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                (new_username, hashed_pw.decode(), role),
            )
            db.commit()

            log_info(f"New user created: {new_username} with role {role}")
            st.success("Account created successfully! Please login.")

        except Exception as e:
            log_error(f"Error during signup: {e}")
            st.error("Something went wrong.")


# -----------------------------
# LOGIN FUNCTION
# -----------------------------
def login(cursor, db):

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = None

    if st.session_state.authenticated:
        return True

    st.title("🔐 Inventory System")

    auth_option = st.radio("Select Option", ["Login", "Sign Up"])

    if auth_option == "Login":

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                if verify_password(password, user["password_hash"].encode()):
                    st.session_state.authenticated = True
                    st.session_state.role = user["role"]
                    st.session_state.username = user["username"]

                    log_info(f"User {username} logged in successfully.")
                    st.rerun()
                else:
                    log_error(f"Failed login attempt for user {username}.")
                    st.error("Invalid credentials")
            else:
                st.error("User not found")

    else:
        signup(cursor, db)

    return False


# -----------------------------
# LOGOUT
# -----------------------------
def logout():
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None