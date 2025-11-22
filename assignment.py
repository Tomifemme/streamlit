import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("Sales Data Dashboard")
#file selection
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])


df = pd.read_excel(uploaded_file)
df.columns = df.columns.str.strip().str.lower()

st.subheader("Data Preview")
st.write(df.head())

st.subheader("Data Summary")
st.write(df.describe())

#Region Filter
st.subheader("Filter by Region")
if "region" in df.columns:
    regions = df["region"].dropna().unique().tolist()
    selected_region = st.selectbox("Select Region", ["All"] + regions)

    if selected_region != "All":
        filtered_df = df[df["region"] == selected_region]
    else:
        filtered_df = df
else:
     st.warning("No 'region' column found.")
filtered_df = df

st.write(filtered_df)


#Vendor Filter
st.subheader("Select Vendor")
if "name" in df.columns:
    vendors = filtered_df["name"].dropna().unique().tolist()
    selected_vendor = st.selectbox("Select Vendor", ["All"] + vendors)

    if selected_vendor != "All":
        vendor_data = filtered_df[filtered_df["name"] == selected_vendor]
        st.write(vendor_data)
    else:
        vendor_data = filtered_df
else:
    st.warning("No 'name' column found.")
    vendor_data = filtered_df

st.subheader("Graphs")

if all(col in vendor_data.columns for col in ["name", "sold units", "total sales", "sales average"]):
    if st.button("Generate Graphs"):
        names = vendor_data["name"].tolist()
        step = max(1, len(names) // 10)  # show at most ~10 labels

        # Units Sold (Bar)
        st.markdown("**Units Sold per Vendor**")
        fig1, ax1 = plt.subplots(figsize=(7, 3.5))
        ax1.bar(names, vendor_data["sold units"], color="steelblue")
        ax1.set_ylabel("Units Sold")
        ax1.set_xticks(np.arange(0, len(names), step))
        ax1.set_xticklabels([names[i] for i in range(0, len(names), step)],
                                rotation=45, ha="right", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig1)

        # Total Sales (Line)
        st.markdown("**Total Sales per Vendor**")
        fig2, ax2 = plt.subplots(figsize=(7, 3.5))
        ax2.plot(names, vendor_data["total sales"], marker="o", color="darkgreen", linewidth=1.2)
        ax2.set_ylabel("Total Sales")
        ax2.set_xticks(np.arange(0, len(names), step))
        ax2.set_xticklabels([names[i] for i in range(0, len(names), step)],
                                rotation=45, ha="right", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig2)

        # Average Sales (Scatter)
        st.markdown("**Average Sales per Vendor**")
        fig3, ax3 = plt.subplots(figsize=(7, 3.5))
        ax3.scatter(names, vendor_data["sales average"], color="darkred")
        ax3.set_ylabel("Average Sales")
        ax3.set_xticks(np.arange(0, len(names), step))
        ax3.set_xticklabels([names[i] for i in range(0, len(names), step)],
                                rotation=45, ha="right", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig3)