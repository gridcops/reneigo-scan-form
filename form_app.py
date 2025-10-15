import streamlit as st
import urllib.parse

# Get vehicle ID from URL
vehicle_id = st.query_params["vid"] if "vid" in st.query_params else ""

if vehicle_id:
    st.markdown(f"**Vehicle:** `{vehicle_id}`")
else:
    st.warning("⚠️ Vehicle ID not found in URL.")

# Branding header
st.title("🛡️ Reneigo Scan")
st.subheader("Presented by GridCops Enterprises")
st.markdown(f"**Vehicle:** `{vehicle_id}`")

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
if st.button("Send Alert"):
    message = f"{reason} via Reneigo Scan — Vehicle {vehicle_id}"
    encoded = urllib.parse.quote(message)
    wa_link = f"https://wa.me/918700832234?text={encoded}"  # Replace with your relay number
    st.markdown(f"[Click to send WhatsApp alert]({wa_link})", unsafe_allow_html=True)