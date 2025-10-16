import streamlit as st
import pandas as pd

# Load QR pool
CSV_URL = "https://raw.githubusercontent.com/gridcops/reneigo-scan-form/main/qr_pool.csv"
df = pd.read_csv(CSV_URL)

st.title("🛠️ QR Assignment Panel")
st.subheader("GridCops Admin — Reneigo Scan")

# Select QR ID
qr_id = st.selectbox("Select QR ID to assign", df[df["Assigned"] != "Yes"]["QR_ID"].tolist())

# Enter vehicle number
vehicle = st.text_input("Enter Vehicle Number")

# Confirm assignment
if st.button("Assign Vehicle"):
    idx = df[df["QR_ID"] == qr_id].index[0]
    df.at[idx, "Vehicle"] = vehicle
    df.at[idx, "Assigned"] = "Yes"
    st.success(f"✅ QR `{qr_id}` assigned to vehicle `{vehicle}`")

    # Show updated row
    st.dataframe(df[df["QR_ID"] == qr_id])

    # Optional: Save locally for now
    df.to_csv("updated_qr_pool.csv", index=False)
    st.info("📁 Saved as updated_qr_pool.csv — ready to push to GitHub")
