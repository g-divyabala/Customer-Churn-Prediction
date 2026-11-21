
import streamlit as st
import pandas as pd
import pickle
import os

# --------------------------------
# LOAD TRAINED MODEL
# --------------------------------

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="centered"
)

MODEL_PATH = "churn_prediction_bundle.pkl"

if not os.path.exists(MODEL_PATH):
    st.error("Model file not found. Please check your project folder.")
    st.stop()

with open(MODEL_PATH, "rb") as file:
    bundle = pickle.load(file)

model = bundle["model"]
scaler = bundle["scaler"]
feature_columns = bundle["feature_columns"]


# --------------------------------
# APPLICATION TITLE
# --------------------------------

st.title("Customer Churn Prediction")

st.write(
    "Enter customer details to predict whether "
    "the customer is likely to leave the company."
)

st.divider()

st.subheader("Customer Information")


# --------------------------------
# CUSTOMER INPUTS
# --------------------------------

gender = st.selectbox(
    "Gender", ["Female", "Male"]
)

senior_citizen = st.selectbox(
    "Senior Citizen", [0, 1]
)

partner = st.selectbox(
    "Partner", ["Yes", "No"]
)

dependents = st.selectbox(
    "Dependents", ["Yes", "No"]
)

tenure = st.slider(
    "Tenure (Months)", 0, 72, 12
)

phone_service = st.selectbox(
    "Phone Service", ["Yes", "No"]
)

multiple_lines = st.selectbox(
    "Multiple Lines",
    ["No", "Yes", "No phone service"]
)

internet_service = st.selectbox(
    "Internet Service",
    ["DSL", "Fiber optic", "No"]
)

online_security = st.selectbox(
    "Online Security",
    ["No", "Yes", "No internet service"]
)

online_backup = st.selectbox(
    "Online Backup",
    ["No", "Yes", "No internet service"]
)

device_protection = st.selectbox(
    "Device Protection",
    ["No", "Yes", "No internet service"]
)

tech_support = st.selectbox(
    "Tech Support",
    ["No", "Yes", "No internet service"]
)

streaming_tv = st.selectbox(
    "Streaming TV",
    ["No", "Yes", "No internet service"]
)

streaming_movies = st.selectbox(
    "Streaming Movies",
    ["No", "Yes", "No internet service"]
)

contract = st.selectbox(
    "Contract",
    ["Month-to-month", "One year", "Two year"]
)

paperless_billing = st.selectbox(
    "Paperless Billing", ["Yes", "No"]
)

payment_method = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

monthly_charges = st.number_input(
    "Monthly Charges",
    min_value=0.0,
    value=70.0
)

total_charges = st.number_input(
    "Total Charges",
    min_value=0.0,
    value=500.0
)


# --------------------------------
# PREDICTION
# --------------------------------

if st.button("Predict Churn", type="primary"):

    customer = {
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    try:

        # Create an empty row with training columns
        input_encoded = pd.DataFrame(
            0,
            index=[0],
            columns=feature_columns
        )

        # Fill numeric columns
        numeric_columns = [
            "SeniorCitizen",
            "tenure",
            "MonthlyCharges",
            "TotalCharges"
        ]

        for col in numeric_columns:
            input_encoded.loc[0, col] = customer[col]

        # Fill categorical columns
        categorical_columns = [
            "gender",
            "Partner",
            "Dependents",
            "PhoneService",
            "MultipleLines",
            "InternetService",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies",
            "Contract",
            "PaperlessBilling",
            "PaymentMethod"
        ]

        for col in categorical_columns:

            encoded_column = f"{col}_{customer[col]}"

            if encoded_column in feature_columns:
                input_encoded.loc[0, encoded_column] = 1

        # Ensure correct column order
        input_encoded = input_encoded[feature_columns]

        # Scale customer input
        input_scaled = scaler.transform(input_encoded)

        # Predict churn
        prediction = model.predict(input_scaled)[0]

        probability = model.predict_proba(
            input_scaled
        )[0][1]

        # Display result
        st.divider()
        st.subheader("Prediction Result")

        st.metric(
            "Churn Probability",
            f"{probability:.2%}"
        )

        if prediction == 1:

            st.error(
                "Customer is likely to churn!"
            )

            st.warning(
                "Consider contacting this customer "
                "with a suitable retention offer."
            )

        else:

            st.success(
                "Customer is likely to stay."
            )

    except Exception as e:

        st.error(f"Prediction error: {e}")
