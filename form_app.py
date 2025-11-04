import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page config
st.set_page_config(page_title="Reneigo Scan", page_icon="🚗", layout="centered")
st.title("🚨 Reneigo Scan")
st.caption("Presented by GridCops Enterprises")

# Load and clean CSV
df = pd.read_csv("qr_pool.csv")
df["VehicleNo"] = df["VehicleNo"].astype(str).str.strip().str.upper()
df["Status"] = df["Status"].astype(str).str.strip()

# Input from user
vehicle_id = st.text_input("Enter your Vehicle Number").strip().upper()

if vehicle_id:
    record = df[(df["VehicleNo"] == vehicle_id) & (df["Status"] == "Active")]

    if not record.empty:
        st.success(f"✅ Vehicle Found: {vehicle_id}")

        # Always send to mediator
        owner_number = "918700832234"

        # Show QR image if available
        qr_path = str(record["QRPath"].values[0]).strip()
        if qr_path and os.path.exists(qr_path):
            st.image(qr_path, caption="QR Code", width=200)
        else:
            st.info("QR image not available for this vehicle.")

        # Reason selection
        reason = st.radio("Why are you contacting the owner?", [
            "No Parking",
            "Getting Towed",
            "Emergency Contact",
            "Blocking Gate",
            "Suspicious Activity",
            "Accident Alert"
        ])

        # Contact number input
        contact_number = st.text_input("Your Mobile Number (for callback)").strip()

        if contact_number:
            # WhatsApp alert message
            message = f"🚨 Alert: {reason} regarding vehicle {vehicle_id}.\nPlease call back: +91-{contact_number}"
            whatsapp_link = f"https://wa.me/{owner_number}?text={message.replace(' ', '%20').replace('\n', '%0A')}"

            if st.button("🚨 Submit Alert"):
                st.markdown(f"[Click here to send WhatsApp alert]({whatsapp_link})", unsafe_allow_html=True)

                # Log the alert
                log_entry = pd.DataFrame([{
                    "VehicleNo": vehicle_id,
                    "Reason": reason,
                    "ContactNumber": contact_number,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                log_entry.to_csv("alert_log.csv", mode="a", header=False, index=False)

                st.success("✅ Alert submitted and logged successfully.")
        else:
            st.warning("⚠️ Please enter your mobile number for callback.")
    else:
        st.warning("⚠️ Vehicle not found or not active.")
        st.info("Please check the number or contact Reneigo Scan support.")
