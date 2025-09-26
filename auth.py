import streamlit as st
import pandas as pd
import bcrypt
import os

USER_FILE = "users.csv"

# Create file if not exists
if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["username", "password"])
    df.to_csv(USER_FILE, index=False)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register_user(username, password):
    df = pd.read_csv(USER_FILE)
    if username in df['username'].values:
        st.error("Username already exists!")
        return False
    hashed_pw = hash_password(password)
    df = pd.concat([df, pd.DataFrame({"username": [username], "password": [hashed_pw]})])
    df.to_csv(USER_FILE, index=False)
    st.success("User registered successfully!")
    return True

def login_user(username, password):
    df = pd.read_csv(USER_FILE)
    if username in df['username'].values:
        hashed_pw = df[df['username'] == username]['password'].values[0]
        if check_password(password, hashed_pw):
            return True
    return False
