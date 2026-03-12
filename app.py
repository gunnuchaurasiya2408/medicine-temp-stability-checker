import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Medicine Temperature Stability Checker")

# ----------------------------
# Sample CSV for users
# ----------------------------

sample_data = pd.DataFrame({
    "Time": ["08:00","09:00","10:00","11:00","12:00","13:00","14:00"],
    "Temperature": [25,26,27,30,33,29,27]
})

csv = sample_data.to_csv(index=False)

st.download_button(
    label="Download Sample Temperature CSV",
    data=csv,
    file_name="sample_temperature_log.csv",
    mime="text/csv"
)

# ----------------------------
# Medicine selection
# ----------------------------

medicine_type = st.selectbox(
    "Select Medicine Type",
    ["Insulin", "Vaccines", "Biologics", "Tablets"]
)

# ----------------------------
# Storage limits
# ----------------------------

if medicine_type == "Insulin":
    lower_limit = 2
    upper_limit = 8

elif medicine_type == "Vaccines":
    lower_limit = 2
    upper_limit = 8

elif medicine_type == "Biologics":
    lower_limit = 2
    upper_limit = 8

elif medicine_type == "Tablets":
    lower_limit = 15
    upper_limit = 30

st.write(f"Safe Storage Range: {lower_limit}°C to {upper_limit}°C")

# ----------------------------
# Upload CSV
# ----------------------------

uploaded_file = st.file_uploader("Upload temperature log (CSV)")

if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    # Clean temperature column
    data["Temperature"] = pd.to_numeric(data["Temperature"], errors="coerce")

    # ----------------------------
    # Basic statistics
    # ----------------------------

    avg_temp = data["Temperature"].mean()
    max_temp = data["Temperature"].max()
    min_temp = data["Temperature"].min()

    # ----------------------------
    # Mean Kinetic Temperature
    # ----------------------------

    temps_kelvin = data["Temperature"] + 273.15
    Ea = 83144
    R = 8.314

    mkt = (-Ea/R) / np.log(np.mean(np.exp(-Ea/(R*temps_kelvin))))
    mkt_celsius = mkt - 273.15

    # ----------------------------
    # Exposure analysis
    # ----------------------------

    exceed_hours = (data["Temperature"] > upper_limit).sum()
    below_hours = (data["Temperature"] < lower_limit).sum()

    # ----------------------------
    # Dashboard metrics
    # ----------------------------

    st.subheader("Key Stability Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Average Temp", f"{avg_temp:.2f} °C")
    col2.metric("Maximum Temp", f"{max_temp:.2f} °C")
    col3.metric("Minimum Temp", f"{min_temp:.2f} °C")
    col4.metric("MKT", f"{mkt_celsius:.2f} °C")

    # ----------------------------
    # Show data
    # ----------------------------

    st.subheader("Temperature Data")
    st.dataframe(data)

    # ----------------------------
    # Temperature graph
    # ----------------------------

    fig, ax = plt.subplots()

    ax.plot(data["Time"], data["Temperature"], marker="o")

    ax.axhline(upper_limit, color="red", linestyle="--", label="Upper Limit")
    ax.axhline(lower_limit, color="blue", linestyle="--", label="Lower Limit")

    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature Exposure")
    ax.legend()

    st.pyplot(fig)

    # ----------------------------
    # MKT display
    # ----------------------------

    st.subheader("Mean Kinetic Temperature (MKT)")
    st.write(f"MKT: {mkt_celsius:.2f} °C")

    # ----------------------------
    # Exposure analysis
    # ----------------------------

    st.subheader("Exposure Analysis")

    if exceed_hours > 0:
        st.warning(f"Temperature exceeded upper limit for {exceed_hours} hours")

    if below_hours > 0:
        st.warning(f"Temperature dropped below lower limit for {below_hours} hours")

    # ----------------------------
    # Visual Stability Status
    # ----------------------------

    st.subheader("Stability Status")

    if exceed_hours == 0 and below_hours == 0:

        st.success("🟢 SAFE — Temperature stayed within limits")
        verdict = "Product likely remains stable"

    elif exceed_hours <= 2 and below_hours <= 2:

        st.warning("🟡 WARNING — Minor temperature excursion detected")
        verdict = "Product may still be stable but review recommended"

    else:

        st.error("🔴 COMPROMISED — Stability risk due to temperature exposure")
        verdict = "Product stability may be compromised"

    # ----------------------------
    # Final verdict
    # ----------------------------

    st.subheader("Final Stability Verdict")
    st.write(verdict)

    # ----------------------------
    # Report generation
    # ----------------------------

    report = pd.DataFrame({
        "Metric": [
            "Average Temperature",
            "Maximum Temperature",
            "Minimum Temperature",
            "Mean Kinetic Temperature (MKT)"
        ],
        "Value": [
            avg_temp,
            max_temp,
            min_temp,
            mkt_celsius
        ]
    })

    report_csv = report.to_csv(index=False)

    st.download_button(
        label="Download Stability Report",
        data=report_csv,
        file_name="stability_report.csv",
        mime="text/csv"
    )
