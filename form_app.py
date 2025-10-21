import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Reneigo Scan", page_icon="🚗", layout="centered")
st.title("🚨 Reneigo Scan")
st.caption("Presented by GridCops Enterprises")

# Read query parameter
query_params = st.query_params
qr_id_list = query_params.get("id")
qr_id = str(qr_id_list[0]).strip() if qr_id_list else ""

# Load and clean CSV
df = pd.read_csv("qr_pool.csv")
df["QR_ID"] = df["QR_ID"].astype(str).str.strip()
df["Assigned"] = df["Assigned"].astype(str).str.strip()

# Debug trace
st.write(f"🧪 Scanned QR ID: '{qr_id}'")

# Match record
record = df[(df["QR_ID"] == qr_id) & (df["Assigned"] == "Yes")]

if not record.empty:
    vehicle_id = str(record["Vehicle"].values[0]).strip()
    qr_path = str(record["QRPath"].values[0]).strip()
    owner_number = "918700832234"  # Replace with actual number or pull from CSV

    st.success(f"✅ Vehicle: {vehicle_id}")
    if qr_path and os.path.exists(qr_path):
        st.image(qr_path, caption="QR Code", width=200)

    reason = st.radio("Why are you contacting the owner?", [
        "No Parking",
        "Getting Towed",
        "Emergency Contact",
        "Blocking Gate",
        "Suspicious Activity",
        "Accident Alert"
    ])

    message = f"Alert: {reason} regarding vehicle {vehicle_id} scanned via GridCops QR."
    whatsapp_link = f"https://wa.me/{owner_number}?text={message.replace(' ', '%20')}"

    if st.button("🚨 Submit Alert"):
        st.markdown(f"[Click here to send WhatsApp alert]({whatsapp_link})", unsafe_allow_html=True)
else:
    st.warning("⚠️ QR not assigned or vehicle not found.")
    st.info("If this is unexpected, please contact GridCops support.")

