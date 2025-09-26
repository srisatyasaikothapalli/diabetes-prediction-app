import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from auth import login_user, register_user

# Load trained model
model = pickle.load(open("diabetes_model.pkl", "rb"))

# Page config
st.set_page_config(page_title="Diabetes Prediction AI", page_icon="🧠")
st.title("🩺 Diabetes Prediction AI")

# --- Initialize session state ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

# --- Sidebar menu ---
if st.session_state['logged_in']:
    choice = st.sidebar.selectbox("Menu", ["Home", "Logout"])
else:
    choice = st.sidebar.selectbox("Menu", ["Login", "Register"])

# ---------------- Logout ----------------
if choice == "Logout":
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.success("You have been logged out!")
    choice = "Login"  # reset menu

# ---------------- Authentication ----------------
if not st.session_state['logged_in']:
    if choice == "Login":
        st.subheader("🔑 Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success(f"Welcome {username}!")
            else:
                st.error("Invalid username or password!")

    elif choice == "Register":
        st.subheader("📝 Register")
        username = st.text_input("Username", key="reg_username")
        password = st.text_input("Password", type="password", key="reg_password")
        password2 = st.text_input("Confirm Password", type="password", key="reg_password2")
        if st.button("Register"):
            if password != password2:
                st.error("Passwords do not match!")
            else:
                if register_user(username, password):
                    st.success("You can now login from the Login page.")

# ---------------- Prediction Page ----------------
if st.session_state['logged_in']:
    st.subheader(f"📋 Enter Medical Details, {st.session_state['username']}")

    age = st.number_input("Age (in years)", min_value=1, max_value=120, value=30)
    glucose = st.number_input("Glucose Level (Blood sugar, mg/dL)", min_value=0, max_value=300, value=100)
    blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0, max_value=200, value=80)
    skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20)
    insulin = st.number_input("Insulin Level (µU/mL)", min_value=0, max_value=900, value=80)
    bmi = st.number_input("BMI (Body Mass Index, weight/height²)", min_value=0.0, max_value=70.0, value=25.0, format="%.1f")
    dpf = st.number_input("Diabetes Pedigree Function (DPF)", min_value=0.0, max_value=2.5, value=0.5, format="%.2f")

    if st.button("🔍 Predict"):
        inputs = np.array([[glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
        prediction = model.predict(inputs)[0]
        probability = model.predict_proba(inputs)[0][1] * 100

        st.subheader("📊 Prediction Result")
        if prediction == 1:
            st.error("⚠️ High Risk of Diabetes")
            st.markdown(f"🔬 **AI Probability:** {probability:.2f}%")
            st.info("🧪 Please consult a certified medical professional for further diagnosis and tests.")
        else:
            st.success("✅ Low Risk of Diabetes")
            st.markdown(f"🔬 **AI Probability:** {probability:.2f}%")
            st.info("💡 You seem to be at low risk, but regular checkups are recommended.")

        # Visualization
        features = ["Glucose", "BP", "SkinThickness", "Insulin", "BMI", "DPF", "Age"]
        values = [glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]

        fig, ax = plt.subplots(figsize=(10, 4))
        sns.barplot(x=features, y=values, palette="coolwarm", ax=ax)
        ax.set_title("Your Medical Inputs")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("⚠️ This tool is for **educational/demo** purposes. For actual diagnosis, consult a medical professional.")
