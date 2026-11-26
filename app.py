import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Credit Card Fraud Detection", layout="wide")

# PREMIUM BANKING THEME - Dark Navy + Gold + Teal
st.markdown("""
<style>
.stApp { background-color: #0F172A; }
h1 { color: #FFFFFF !important; text-align: left; font-size: 42px !important; }
h2, h3 { color: #F8FAFC !important; }
p, label, span { color: #CBD5E1 !important; }
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    padding: 22px; border-radius: 16px;
    border: 1px solid #334155;
    border-left: 4px solid #F59E0B;
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
}
div[data-testid="stMetricLabel"] { color: #94A3B8 !important; font-size: 14px !important; }
div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 30px !important; }
section[data-testid="stSidebar"] { background-color: #1E293B !important; }
div[data-testid="stExpander"] { background-color: #1E293B; }
</style>
""", unsafe_allow_html=True)

st.title("💳 Credit Card Fraud Detection")
st.markdown("**🔒 Secure Banking Analytics  |  Real-time Transaction Monitoring**")
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv("creditcard.csv")

df = load_data()

# FILTERS
st.sidebar.header("⚙️ Filters")
txn_type = st.sidebar.radio("Transaction Type", ["All", "Normal", "Fraud"])
max_amt = st.sidebar.slider("Maximum Amount", 0, int(df['Amount'].max()), int(df['Amount'].max()))

if txn_type == "Fraud":
    df = df[df['Class'] == 1]
elif txn_type == "Normal":
    df = df[df['Class'] == 0]
df = df[df['Amount'] <= max_amt]

# CARDS
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Transactions", f"{len(df):,}")
c2.metric("Fraud Cases", f"{(df['Class']==1).sum():,}")
c3.metric("Fraud Rate", f"{df['Class'].mean()*100:.2f}%")
c4.metric("Avg Amount", f"${df['Amount'].mean():.2f}")

# CHART 1 - Teal + Gold
st.subheader("1. Distribution of Transaction Amount")
fig1 = px.histogram(df, x="Amount", color="Class", color_discrete_map={0:"#14B8A6", 1:"#F59E0B"}, nbins=50, template="plotly_dark")
fig1.update_layout(paper_bgcolor="#0F172A", plot_bgcolor="#0F172A")
st.plotly_chart(fig1, use_container_width=True)

# CHART 2
st.subheader("2. Time vs Amount")
fig2 = px.scatter(df, x="Time", y="Amount", color="Class", color_discrete_map={0:"#14B8A6", 1:"#F59E0B"}, opacity=0.6, template="plotly_dark")
fig2.update_layout(paper_bgcolor="#0F172A", plot_bgcolor="#0F172A")
st.plotly_chart(fig2, use_container_width=True)

# CHART 3
st.subheader("3. Correlation Heatmap")
fig, ax = plt.subplots(figsize=(10,6))
fig.patch.set_facecolor('#0F172A')
ax.set_facecolor('#0F172A')
sns.heatmap(df[['Time','V1','V2','V3','V4','Amount','Class']].corr(), cmap="YlGnBu", annot=True, ax=ax, annot_kws={'color':'white'})
ax.tick_params(colors='white')
st.pyplot(fig)

# CHART 4
st.subheader("4. V1 vs V2 by Transaction Class")
fig4 = px.scatter(df, x="V1", y="V2", color="Class", color_discrete_map={0:"#14B8A6", 1:"#F59E0B"}, opacity=0.6, template="plotly_dark")
fig4.update_layout(paper_bgcolor="#0F172A", plot_bgcolor="#0F172A")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("5. Key Findings")
st.info("1. Fraud cases are very rare, only 0.17%")
st.info("2. V2 and V4 have a strong relationship with fraud")
st.info("3. Fraud transactions show a different pattern")

if st.checkbox("Show Raw Data"):
    st.dataframe(df.head(20))
