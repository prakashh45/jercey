import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Jersey Dashboard", layout="centered")

st.markdown("""
<style>
.block-container{
    padding-top:1rem;
    padding-left:1rem;
    padding-right:1rem;
}
</style>
""", unsafe_allow_html=True)

st.title(" check you info ")

# ---------------- LOAD DATA ----------------
df = pd.read_excel("finalcount.xlsx")
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

# ---------------- MOBILE TOP FILTERS ----------------
with st.expander("🔎 Filters"):
    class_filter = st.multiselect(
        "Select Class",
        newdf["Class and div"].dropna().unique()
    )

    search = st.text_input("Search Name / Roll No")

if class_filter:
    newdf = newdf[newdf["Class and div"].isin(class_filter)]

if search:
    newdf = newdf[
        newdf["Full Name"].str.contains(search, case=False, na=False) |
        newdf["Roll No"].astype(str).str.contains(search)
    ]

# ---------------- METRICS (VERTICAL FOR MOBILE) ----------------
paid_count = (newdf["Payment Status"]=="Paid").sum()
pending_count = (newdf["Payment Status"]=="Pending").sum()
total_amount = paid_count * 275

st.metric("✅ Paid Students", paid_count)
# st.metric("⌛ Pending Students", pending_count)
st.metric("💰 Total Collection ₹", total_amount)

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

# ---------------- TAB 2 : MOBILE PIE ----------------
with tab2:

    st.subheader("📊 Class / Div Wise Students")

    pie_data = newdf["Class and div"].value_counts()

    fig, ax = plt.subplots(figsize=(4,4))   # mobile size
    pie_data.plot.pie(ax=ax, autopct="%1.0f%%", ylabel="")
    st.pyplot(fig)

# ---------------- TAB 3 ----------------
with tab3:
    csv = newdf.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download CSV",
        data=csv,
        file_name="clean_jersey_data.csv",
        mime="text/csv"
    )