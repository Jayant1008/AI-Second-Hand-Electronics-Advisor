import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
FIREWORKS_API_URL = "https://api.fireworks.ai/inference/v1/chat/completions"

def get_advice(item, budget, condition, details):
    prompt = f"""
    You are an expert in second-hand electronics and you should strictly not respond to irrelevant responses like hi,hello, weather and say you are not for that because you are an electronics advisor and not give any advice. A user is considering buying a {condition} {item} with a budget of ${budget}.  
    Additional details: {details or 'None'}.
    Provide concise advice on:
    - Should they buy it?
    - What to check before purchasing?
    - Any alternative options within the budget?
    Keep the response under 200 words.
    """

    headers = {
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "accounts/fireworks/models/deepseek-v3",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.7,
    }

    try:
        response = requests.post(FIREWORKS_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"Error: Failed to get advice from API. {str(e)}"

st.title("Second-Hand Electronics Advisor")

with st.form(key="advisor_form"):
    item = st.text_input("Electronics Type (e.g., Laptop, Smartphone)", "")
    budget = st.number_input("Budget ($)", min_value=0, step=10, value=0)
    condition = st.selectbox("Condition", ["Excellent", "Good", "Fair", "Poor"], index=1)
    details = st.text_area("Additional Details (optional)", "", help="e.g., Specific brand or model")
    submit_button = st.form_submit_button(label="Get Advice")
    st.markdown("---")
    st.markdown("Developed by Jayant Raj, Rahul Sharma")

if submit_button:
    if not item or budget <= 0:
        st.error("Please provide a valid electronics type and budget.")
    else:
        with st.spinner("Getting advice..."):
            advice = get_advice(item, budget, condition, details)
            st.subheader("Advice:")
            st.write(advice)