import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page setup
st.set_page_config(page_title="Reneigo Scan", page_icon="🚗", layout="centered")
st.title("🚨 Reneigo Scan")
st.caption("Presented by GridCops Enterprises")

# Ensure alert log exists
log_path = os.path.join(os.path.dirname(__file__), "alert_log.csv")
if not os.path.exists(log_path):
    pd.DataFrame(columns=["VehicleNo", "Reason", "ContactNumber", "Timestamp", "Status"]).to_csv(log_path, index=False)

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
            st.session_state["contact_number"] = contact_number  # Persist across reruns

            # Owner number (masked or mediated)
            owner_number = "918700832234"
            message = f"🚨 Alert: {reason} for vehicle {vehicle_id}.\nPlease call back: +91-{contact_number}"
            whatsapp_link = f"https://wa.me/{owner_number}?text={message.replace(' ', '%20').replace('\n', '%0A')}"

            if st.button("🚨 Submit Alert"):
                # Log alert silently
                log_entry = pd.DataFrame([{
                    "VehicleNo": vehicle_id,
                    "Reason": reason,
                    "ContactNumber": contact_number,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Status": "Pending"
                }])
                log_entry.to_csv(log_path, mode="a", header=False, index=False)

                # Show WhatsApp link with clear instruction
                st.markdown(f"[📲 Click here to send WhatsApp alert]({whatsapp_link})", unsafe_allow_html=True)
                st.info("Your alert has been prepared. Please tap the link above to notify the vehicle owner.")
        else:
            st.warning("⚠️ Please enter your mobile number.")
    else:
        st.warning("⚠️ Vehicle not found or not active.")
        st.info("Check the number or contact GridCops support.")

# Show only user's own alerts
if os.path.exists(log_path):
    st.subheader("📋 Your Recent Alerts")
    log_df = pd.read_csv(log_path)
    if "contact_number" in st.session_state and st.session_state["contact_number"]:
        contact_number = st.session_state["contact_number"]
        user_alerts = log_df[log_df["ContactNumber"] == contact_number]
        st.dataframe(user_alerts.tail(5))
