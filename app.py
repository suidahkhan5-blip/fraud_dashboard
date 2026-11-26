import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Credit Card Fraud Dashboard", layout="wide")
st.title("Credit Card Fraud Detection Dashboard")
st.write("This dashboard shows how fraudulent transactions differ from normal transactions.")

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/nsethi31/Kaggle-Data-Credit-Card-Fraud-Detection/master/creditcard.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
class_filter = st.sidebar.multiselect(
    "Select Transaction Type",
    options=[0, 1],
    default=[0, 1],
    format_func=lambda x: "Fraud" if x == 1 else "Normal"
)
amount_filter = st.sidebar.slider(
    "Maximum Amount",
    0,
    int(df['Amount'].max()),
    int(df['Amount'].max())
)

filtered_df = df[(df['Class'].isin(class_filter)) & (df['Amount'] <= amount_filter)]

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", len(filtered_df))
col2.metric("Fraud Cases", len(filtered_df[filtered_df['Class'] == 1]))
col3.metric("Fraud Percentage", f"{filtered_df['Class'].mean()*100:.2f}%")
col4.metric("Average Amount", f"${filtered_df['Amount'].mean():.2f}")

# Graph 1
st.subheader("1. Fraud vs Normal Transactions")
fig1 = px.histogram(filtered_df, x='Class', color='Class', title="Fraud vs Normal Transactions")
st.plotly_chart(fig1)

# Graph 2
st.subheader("2. Distribution of Transaction Amount")
fig2, ax2 = plt.subplots()
sns.histplot(filtered_df['Amount'], bins=50, ax=ax2)
ax2.set_title("Distribution of Transaction Amount")
ax2.set_xlabel("Amount")
ax2.set_ylabel("Count")
st.pyplot(fig2)

# Graph 3
st.subheader("3. Time vs Amount")
fig3 = px.scatter(
    filtered_df.sample(min(1000, len(filtered_df))),
    x='Time', y='Amount', color='Class',
    title="Time vs Amount"
)
st.plotly_chart(fig3)

# Graph 4
st.subheader("4. Correlation Heatmap")
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.heatmap(filtered_df[['V1', 'V2', 'V3', 'V4', 'Amount', 'Class']].corr(), annot=True, cmap='coolwarm', ax=ax4)
ax4.set_title("Correlation Heatmap")
st.pyplot(fig4)

# Graph 5
st.subheader("5. V1 vs V2 by Transaction Class")
fig5 = px.scatter(
    filtered_df.sample(min(1000, len(filtered_df))),
    x='V1', y='V2', color='Class',
    title="V1 vs V2 by Class"
)
st.plotly_chart(fig5)

# Raw Data
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df.head(100))

# Findings
st.subheader("Key Findings")
st.write("1. Fraud cases are very rare, only 0.17% of all transactions.")
st.write("2. V2 and V4 have a strong relationship with fraud.")
st.write("3. Fraud transactions show a different pattern in Amount compared to normal transactions.")
