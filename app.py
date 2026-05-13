import streamlit as st
import pandas as pd
from web3 import Web3
import json

# 1. Connection & Setup
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
CONTRACT_ADDRESS = w3.to_checksum_address("0x5FbDB2315678afecb367f032d93f642f64180aa3")
ABI = json.loads("""
[
    {"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"partnerBank","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"syndicateShares","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"_loanId","type":"uint256"},{"internalType":"uint256","name":"_newValue","type":"uint256"}],"name":"updateMarketValue","outputs":[],"stateMutability":"nonpayable","type":"function"}
]
""")
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

if w3.is_connected():
    accounts = w3.eth.accounts
    total_funded = sum([contract.functions.balanceOf(acc, 1).call() for acc in accounts[0:10]])
    buyer_wallet = accounts[9]
else:
    total_funded = 0

st.set_page_config(page_title="Automated Liquidation Engine", layout="wide")

# 2. Sidebar: Identity & The Digital Vault
st.sidebar.header("User Identity")
user_role = st.sidebar.selectbox("View Dashboard As:", ["Lead Bank (Seller)", "Hedge Fund (Buyer)"])
st.sidebar.divider()

st.sidebar.subheader("📉 Market Stress Test")
market_value = st.sidebar.slider("Property Market Value ($M)", 5.0, 15.0, 12.0)

# AUTOMATION: Trigger NPL state if value drops below $10M
if market_value < 10.0:
    st.sidebar.error("⚠️ MARGIN CALL: Collateral < 100%")
    auto_status = "Non-Performing (NPL)"
else:
    auto_status = "Performing"

loan_status = st.sidebar.select_slider(
    "Loan Performance Status",
    options=["Performing", "Delinquent", "Non-Performing (NPL)"],
    value=auto_status
)

st.sidebar.divider()

# DIGITAL VAULT SECTION
st.sidebar.header("📂 Digital Vault")
st.sidebar.caption("Secured via IPFS Hash Verification")
with st.sidebar.expander("View Asset Documents", expanded=False):
    st.write("**Validated On-Chain:** ✅")
    st.button("📄 Appraisal_Report_2026.pdf")
    st.button("🌿 Phase_I_Environmental.pdf")
    st.button("🏗️ Property_Condition_Assess.pdf")
    st.info("Vault Access Logged to Blockchain")

# 3. Main Header
st.title(f"🛡️ PoC #24: Automated Liquidation & Margin Call Engine")
st.caption(f"Asset Digital Twin: {CONTRACT_ADDRESS}")

# 4. Metrics & Valuation
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Principal Balance", "$10,000,000")
with m2:
    st.metric("On-Chain Syndication", f"${total_funded:,.0f}")
with m3:
    val = "6.25%" if loan_status == "Performing" else "45.0% Price (55% Discount)"
    st.metric("Yield / Pricing", val)

st.divider()

# 5. Conditional Views
if user_role == "Lead Bank (Seller)":
    st.subheader("🏦 Lead Bank Management Console")
    if loan_status != "Non-Performing (NPL)":
        st.info("Loan is healthy. Primary syndication active.")
        partner = st.selectbox("Select Institution:", options=accounts[1:5])
        amt = st.number_input("Syndication Amount ($)", value=1000000)
        if st.button("Finalize Syndication"):
            tx = contract.functions.syndicateShares(partner, int(amt)).transact({'from': accounts[0]})
            st.success(f"Syndicated! TX: {tx.hex()}")
    else:
        st.warning("NPL status detected. Listing for secondary sale enabled.")
        # Default value changed to 45 (Matches 55% discount)
        ask_price = st.slider("Secondary Market Ask Price (% of Par)", 30, 85, 45) 
        
        mv = (10000000 * ask_price) / 100
        hc = 10000000 - mv
        st.bar_chart(pd.DataFrame({"Market Value ($)": [mv], "Discount/Haircut ($)": [hc]}), color=["#2ecc71", "#e74c3c"])
        
        if st.button("🚀 Update Marketplace Listing"):
            st.session_state['npl_price'] = ask_price
            st.success(f"Listing updated to {ask_price}% of Par (55% Discount Applied).")

else:
    st.subheader("💰 Institutional Buyer Portal")
    if loan_status != "Non-Performing (NPL)":
        st.info("No distressed opportunities available at this time.")
    else:
        price = st.session_state.get('npl_price', 45)
        st.error(f"OPPORTUNITY: Distressed Loan available at {price}% of Par")
        invest_amt = st.number_input("Investment Amount ($)", value=2000000)
        cost = (invest_amt * price) / 100
        
        col_a, col_b = st.columns(2)
        col_a.metric("Par Value of Shares", f"${invest_amt:,.0f}")
        col_b.metric("Acquisition Cost", f"${cost:,.0f}", delta=f"-{100-price}%")
        
        if st.button("Confirm Secondary Purchase"):
            tx = contract.functions.syndicateShares(buyer_wallet, int(invest_amt)).transact({'from': accounts[0]})
            st.balloons()
            st.success(f"Trade Executed! Principal assigned to Hedge Fund wallet: {buyer_wallet}")

# 6. Simplified Ledger
st.markdown("---")
st.table(pd.DataFrame({
    'Lender Role': ['Lead Bank', 'Active Partners/Buyers'],
    'Total Exposure': ['$10,000,000 (Gross)', f'${total_funded:,.0f} (Net)']
}))
