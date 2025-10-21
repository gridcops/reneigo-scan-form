import streamlit as st
import pandas as pd
import urllib.parse

# Load CSV
df = pd.read_csv("qr_pool.csv")

df["QR_ID"] = df["QR_ID"].astype(str).str.strip()
df["Assigned"] = df["Assigned"].astype(str).str.strip()

# Get QR ID from URL
query_params = st.query_params
qr_id_list = query_params.get("id")
qr_id = qr_id_list[0].strip() if qr_id_list else ""

st.title("🛡️ Reneigo Scan")
st.subheader("Presented by GridCops Enterprises")
st.write(f"🔍 Scanned QR ID: `{qr_id}`")

# Match record
record = df[df["QR_ID"] == qr_id]
if not record.empty:
    assigned = str(record["Assigned"].values[0]).strip()
    vehicle = str(record["Vehicle"].values[0]).strip()
    if assigned == "Yes" and vehicle:
        vehicle_id = vehicle

vehicle_id = ""
if not record.empty:
    assigned = record["Assigned"].values[0]
    vehicle = record["Vehicle"].values[0]
    if assigned == "Yes" and vehicle:
        vehicle_id = vehicle

# Show result
if vehicle_id:
    st.success(f"🚗 Vehicle: `{vehicle_id}`")
else:
    st.warning("⚠️ QR not assigned or vehicle not found.")
    st.info("If this is unexpected, please contact GridCops support.")

# Alert form
with st.form("alert_form"):
    reason = st.radio("Why are you contacting the owner?", [
        "🚫 No Parking", "🚓 Getting Towed", "🚨 Emergency Contact",
        "📦 Blocking Gate", "🧍 Suspicious Activity", "🚑 Accident Alert"
    ])
    submitted = st.form_submit_button("Send Alert")
    if submitted and vehicle_id:
        message = f"{reason} via Reneigo Scan — Vehicle {vehicle_id}"
        encoded = urllib.parse.quote(message)
        wa_link = f"https://wa.me/918700832234?text={encoded}"
        st.markdown(f"[Click to send WhatsApp alert]({wa_link})", unsafe_allow_html=True)
