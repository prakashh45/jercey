import streamlit as st
import pandas as pd

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Jersey Dashboard", layout="wide")
st.title("🏏 cse Jersey  Dashboard")

# ---------------- LOAD DATA ----------------
df = pd.read_excel("Untitled(Responses).xlsx")
df.columns = df.columns.str.strip()

cols = [
    "Full Name",
    "Roll No",
    "Class and div",
    "Name to Printed on jersey",
    "Choice Number to be printed on Jersey",
    "Select size for your Jersey",
    "Transaction ID"
]

newdf = df.loc[:, cols].copy()

# ---------------- PAYMENT STATUS ----------------
newdf["Payment Status"] = newdf["Transaction ID"].apply(
    lambda x: "Paid" if pd.notna(x) else "Pending"
)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filters")

class_filter = st.sidebar.multiselect(
    "Select Class",
    newdf["Class and div"].dropna().unique()
)

search = st.sidebar.text_input("Search Name / Roll No")

if class_filter:
    newdf = newdf[newdf["Class and div"].isin(class_filter)]

if search:
    newdf = newdf[
        newdf["Full Name"].str.contains(search, case=False, na=False) |
        newdf["Roll No"].astype(str).str.contains(search)
    ]

# ---------------- METRICS ----------------
paid_count = (newdf["Payment Status"]=="Paid").sum()
pending_count = (newdf["Payment Status"]=="Pending").sum()
total_amount = paid_count * 275

c1,c2,c3 = st.columns(3)
c1.metric("✅ Paid Students", paid_count)

c3.metric("💰 Total Collection ₹", total_amount)

st.divider()

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["📋 Data", "📊 Analytics", "⬇️ Export"])

# ---------------- TAB 1 ----------------
with tab1:
    def highlight(val):
        if val == "Paid":
            return "background-color: lightgreen"
        elif val == "Pending":
            return "background-color: salmon"
        return ""

    st.dataframe(
        newdf.style.map(highlight, subset=["Payment Status"]),
        use_container_width=True
    )

# ---------------- TAB 2 : DIV WISE PIE ----------------
with tab2:

    st.subheader("📊 Class / Div Wise Students Pie Chart")

    pie_data = newdf["Class and div"].value_counts()

    st.pyplot(
        pie_data.plot.pie(autopct="%1.0f%%", ylabel="").figure
    )

# ---------------- TAB 3 ----------------
with tab3:
    csv = newdf.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download CSV",
        data=csv,
        file_name="clean_jersey_data.csv",
        mime="text/csv"
    )