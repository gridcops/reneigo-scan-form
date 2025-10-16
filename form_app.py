import streamlit as st
import urllib.parse
import pandas as pd

# Load QR mapping
df = pd.read_csv("https://raw.githubusercontent.com/gridcops/reneigo-scan-form/main/qr_pool.csv")

# Get QR ID from URL
query_params = st.experimental_get_query_params()
qr_id = query_params.get("id", [""])[0]

# Lookup vehicle number
vehicle_id = ""
record = df[df["QR_ID"] == qr_id]
if not record.empty and record["Assigned"].values[0] == "Yes":
    vehicle_id = record["Vehicle"].values[0]

# Branding header
st.title("🛡️ Reneigo Scan")
st.subheader("Presented by GridCops Enterprises")

# Show vehicle info
if vehicle_id:
    st.markdown(f"**Vehicle:** `{vehicle_id}`")
else:
    st.warning("⚠️ QR not assigned or vehicle not found.")

# Reason selection
reason = st.radio("Why are you contacting the owner?", [
    "🚫 No Parking",
    "🚓 Getting Towed",
    "🚨 Emergency Contact",
    "📦 Blocking Gate",
    "🧍 Suspicious Activity",
    "🚑 Accident Alert"
])

# WhatsApp link
if st.button("Send Alert") and vehicle_id:
    message = f"{reason} via Reneigo Scan — Vehicle {vehicle_id}"
    encoded = urllib.parse.quote(message)
    wa_link = f"https://wa.me/918700832234?text={encoded}"  # Replace with your relay number
    st.markdown(f"[Click to send WhatsApp alert]({wa_link})", unsafe_allow_html=True)