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
st.write(f"🧪 Available IDs: {df['QR_ID'].tolist()}")

# Match record
record = df[(df["QR_ID"] == qr_id) & (df["Assigned"] == "Yes")]

if not record.empty:
    vehicle_id = str(record["Vehicle"].values[0]).strip()
    st.success(f"✅ Vehicle: {vehicle_id}")
    
    # Optional: Show QR image
    qr_path = str(record["QRPath"].values[0]).strip()
    if qr_path and os.path.exists(qr_path):
        st.image(qr_path, caption="QR Code", width=200)

    # Alert form
    st.subheader("Why are you contacting the owner?")
    reason = st.radio("Select a reason:", [
        "No Parking",
        "Getting Towed",
        "Emergency Contact",
        "Blocking Gate",
        "Suspicious Activity",
        "Accident Alert"
    ])
    st.button("🚨 Submit Alert")
else:
    st.warning("⚠️ QR not assigned or vehicle not found.")
    st.info("If this is unexpected, please contact GridCops support.")
