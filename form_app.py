import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page setup
st.set_page_config(page_title="Reneigo Scan", page_icon="🚗", layout="centered")
st.title("🚨 Reneigo Scan")

# Load QR pool
pool_path = "qr_pool.csv"
if not os.path.exists(pool_path):
    st.error("❌ QR pool file not found.")
    st.stop()

df = pd.read_csv(pool_path)
df["VehicleNo"] = df["VehicleNo"].astype(str).str.strip().str.upper()
df["Status"] = df["Status"].astype(str).str.strip()

# Input vehicle number
vehicle_id = st.text_input("Enter Vehicle Number").strip().upper()

if vehicle_id:
    record = df[(df["VehicleNo"] == vehicle_id) & (df["Status"] == "Active")]

    if not record.empty:
        st.success(f"✅ Vehicle Found: {vehicle_id}")

        # Show QR image
        qr_path = str(record["QRPath"].values[0]).strip()
        if qr_path and os.path.exists(qr_path):
            st.image(qr_path, caption="QR Code", width=200)
        else:
            st.info("QR image not available.")

        # Alert reason and contact
        reason = st.radio("Reason for alert:", [
            "No Parking", "Getting Towed", "Emergency Contact",
            "Blocking Gate", "Suspicious Activity", "Accident Alert"
        ])
        contact_number = st.text_input("Your Mobile Number (for callback)").strip()

        if contact_number:
            # Owner number (masked or mediated)
            owner_number = "918700832234"
            message = f"🚨 Alert: {reason} for vehicle {vehicle_id}.\nPlease call back: +91-{contact_number}"
            whatsapp_link = f"https://wa.me/{owner_number}?text={message.replace(' ', '%20').replace('\n', '%0A')}"

            if st.button("🚨 Submit Alert"):
                st.markdown(f"[Click to send WhatsApp alert]({whatsapp_link})", unsafe_allow_html=True)

                # Log alert with SLA status
                log_entry = pd.DataFrame([{
                    "VehicleNo": vehicle_id,
                    "Reason": reason,
                    "ContactNumber": contact_number,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Status": "Pending"
                }])
                log_entry.to_csv("alert_log.csv", mode="a", header=not os.path.exists("alert_log.csv"), index=False)
                st.success("✅ Alert submitted and logged.")
        else:
            st.warning("⚠️ Please enter your mobile number.")
    else:
        st.warning("⚠️ Vehicle not found or not active.")
        st.info("Check the number or contact GridCops support.")

# Optional: Show recent alerts
if os.path.exists("alert_log.csv"):
    st.subheader("📋 Recent Alerts")
    log_df = pd.read_csv("alert_log.csv")
    st.dataframe(log_df.tail(10))
