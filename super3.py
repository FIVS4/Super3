import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Business Dashboard",
    layout="wide"
)

# =====================
# LANGUAGE DICTIONARY
# =====================
LANG = {
    "id": {
        "title": "Dashboard Bisnis Supermarket",
        "upload": "Unggah File Excel",
        "sheet": "Pilih Sheet",
        "total_sales": "Total Pendapatan",
        "total_profit": "Total Keuntungan",
        "total_qty": "Total Produk Terjual",
        "chart1": "Pendapatan per Kategori Produk",
        "chart2": "Pendapatan per Kota",
        "chart3": "Metode Pembayaran",
        "chart4": "Tren Pendapatan Harian",
        "chart5": "Jumlah Produk Terjual per Kategori"
    },
    "en": {
        "title": "Supermarket Business Dashboard",
        "upload": "Upload Excel File",
        "sheet": "Select Sheet",
        "total_sales": "Total Revenue",
        "total_profit": "Total Profit",
        "total_qty": "Total Quantity Sold",
        "chart1": "Revenue by Product Line",
        "chart2": "Revenue by City",
        "chart3": "Payment Method Distribution",
        "chart4": "Daily Revenue Trend",
        "chart5": "Quantity Sold by Product Line"
    }
}

# =====================
# LANGUAGE SELECT
# =====================
lang_choice = st.sidebar.selectbox(
    "Language / Bahasa",
    ["Bahasa", "English"]
)

lang = LANG["id"] if lang_choice == "Bahasa" else LANG["en"]

# =====================
# TITLE
# =====================
st.title(lang["title"])

# =====================
# FILE UPLOAD
# =====================
file = st.file_uploader(lang["upload"], type=["xlsx"])

if file:
    df = pd.read_excel(file)

    # =====================
    # DATA PREPARATION
    # =====================
    df["Date"] = pd.to_datetime(df["Date"])

    # =====================
    # KPI SECTION
    # =====================
    col1, col2, col3 = st.columns(3)

    col1.metric(lang["total_sales"], f"{df['Total'].sum():,.2f}")
    col2.metric(lang["total_profit"], f"{df['gross income'].sum():,.2f}")
    col3.metric(lang["total_qty"], int(df["Quantity"].sum()))

    st.divider()

    # =====================
    # CHART 1: Revenue by Product Line
    # =====================
    st.subheader(lang["chart1"])
    revenue_product = df.groupby("Product line")["Total"].sum()
    st.bar_chart(revenue_product)

    # =====================
    # CHART 2: Revenue by City
    # =====================
    st.subheader(lang["chart2"])
    revenue_city = df.groupby("City")["Total"].sum()
    st.bar_chart(revenue_city)

    # =====================
    # CHART 3: Payment Method Distribution
    # =====================
    st.subheader(lang["chart3"])
    payment_count = df["Payment"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(payment_count, labels=payment_count.index, autopct="%1.1f%%")
    st.pyplot(fig1)

    # =====================
    # CHART 4: Daily Revenue Trend
    # =====================
    st.subheader(lang["chart4"])
    daily_sales = df.groupby("Date")["Total"].sum()
    st.line_chart(daily_sales)

    # =====================
    # CHART 5: Quantity Sold by Product Line
    # =====================
    st.subheader(lang["chart5"])
    qty_product = df.groupby("Product line")["Quantity"].sum()
    st.bar_chart(qty_product)

else:
    st.info("Silakan unggah file Excel untuk menampilkan dashboard.")
