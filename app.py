import streamlit as st 
import pandas as pd 
from web3 import Web3 
import json 
import os 

# --- 1. Dynamic Blockchain Binding --- 
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545')) 

# Autodetect addresses emitted via Hardhat build script 
if os.path.exists('deployment.json'): 
    with open('deployment.json', 'r') as f: 
        meta = json.load(f) 
    CONTRACT_ADDRESS = w3.to_checksum_address(meta['address']) 
else: 
    CONTRACT_ADDRESS = w3.to_checksum_address("0x5FbDB2315678afecb367f032d93f642f64180aa3") 

ABI = json.loads(""" 
[ 
    {"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, 
    {"inputs":[{"internalType":"address","name":"partnerBank","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"syndicateShares","outputs":[],"stateMutability":"nonpayable","type":"function"}, 
    {"inputs":[{"internalType":"string","name":"docId","type":"string"}],"name":"signVaultDocument","outputs":[],"stateMutability":"nonpayable","type":"function"}, 
    {"inputs":[{"internalType":"string","name":"docId","type":"string"}],"name":"getSignatureCount","outputs":[{"internalType":"uint256","name":"count","type":"uint256"}],"stateMutability":"view","type":"function"}, 
    {"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"SharesSyndicated","type":"event"}, 
    {"anonymous":false,"inputs":[{"indexed":true,"internalType":"string","name":"docId","type":"string"},{"indexed":true,"internalType":"address","name":"signer","type":"address"},{"indexed":false,"internalType":"uint256","name":"totalSignatures","type":"uint256"}],"name":"DocumentSigned","type":"event"} 
] 
""") 

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI) 

# --- SAFE CONNECTION & ACCOUNTS TOPOLOGY ---
if w3.is_connected(): 
    try:
        accounts = w3.eth.accounts 
        lead_bank_wallet = accounts[0] 
        hedge_fund_wallet = accounts[4] 
        total_funded = sum([contract.functions.balanceOf(acc, 1).call() for acc in accounts[1:10]]) 
    except Exception:
        accounts = ["0x0000000000000000000000000000000000000000"] * 5 
        lead_bank_wallet = accounts[0] 
        hedge_fund_wallet = accounts[4] 
        total_funded = 0
else: 
    accounts = ["0x0000000000000000000000000000000000000000"] * 5 
    lead_bank_wallet = accounts[0] 
    hedge_fund_wallet = accounts[4] 
    total_funded = 0 

# --- 2. Live On-Chain Event Thread Listener (FIXED FILTER BUG) --- 
def fetch_blockchain_events(): 
    if not w3.is_connected(): 
        return [] 
    try: 
        # Directly fetching logs eliminates the Hardhat HTTP provider filter bug
        events = contract.events.SharesSyndicated().get_logs(from_block=0) 
        log_data = [] 
        for e in events: 
            log_data.append({ 
                "Tx Hash": e.transactionHash.hex()[:18] + "...", 
                "Buyer/Partner": e.args.recipient, 
                "Allocated Volume": f"${e.args.amount:,.0f}" 
            }) 
        return log_data 
    except Exception: 
        return [] 

st.set_page_config(page_title="Automated Liquidation Engine v2", layout="wide") 

# Initialize rolling chart data history inside Streamlit session memory 
if 'metrics_history' not in st.session_state: 
    st.session_state['metrics_history'] = pd.DataFrame(columns=[ 
        "Property Value ($M)", "Implied Clearance Price ($M)", "Risk Haircut ($M)" 
    ]) 

# --- 3. Identity and Dashboard Multi-Sig Space --- 
st.sidebar.header("User Identity Context") 
user_role = st.sidebar.selectbox("Active Account Role:", ["Lead Bank (Seller)", "Hedge Fund (Buyer)"]) 
active_signer = lead_bank_wallet if user_role == "Lead Bank (Seller)" else hedge_fund_wallet 

st.sidebar.divider() 
st.sidebar.subheader("📉 Market Stress Test System") 
market_value = st.sidebar.slider("Property Evaluation ($M)", 5.0, 15.0, 12.0) 

if market_value < 10.0: 
    st.sidebar.error("⚠️ MARGIN CALL TRIPPED: LTV Violation") 
    auto_status = "Non-Performing (NPL)" 
else: 
    auto_status = "Performing" 

loan_status = st.sidebar.select_slider( 
    "Asset Real-Time Rating Status", 
    options=["Performing", "Delinquent", "Non-Performing (NPL)"], 
    value=auto_status 
) 

st.sidebar.divider() 

# --- 4. Cryptographic Vault Engine --- 
st.sidebar.header("📂 Multi-Sig Document Vault") 
st.sidebar.caption("Enforced Cryptographic Asset Control via Ledger Verification") 

with st.sidebar.expander("Audit Asset Underwriting Package", expanded=True): 
    docs = { 
        "appraisal": "📄 Appraisal_Report_2026.pdf", 
        "env": "🌿 Phase_I_Environmental.pdf" 
    } 
    for doc_key, doc_name in docs.items(): 
        # --- SAFE SIGNATURE READING ---
        sig_count = 0
        if w3.is_connected(): 
            try:
                sig_count = contract.functions.getSignatureCount(doc_key).call()
            except Exception:
                sig_count = 0
                
        st.write(f"**{doc_name}**") 
        st.caption(f"Signatures Captured: `{sig_count} / 2 required`") 
        
        if sig_count >= 2: 
            st.success("✅ Document Fully Executed & Unlocked") 
        else: 
            st.warning("🔒 Pending Multi-Sig Verification") 
            
        if st.button(f"Sign & Attest {doc_key.capitalize()}", key=f"sig_{doc_key}"): 
            if w3.is_connected(): 
                tx = contract.functions.signVaultDocument(doc_key).transact({'from': active_signer}) 
                st.toast(f"Attestation Logged! Tx: {tx.hex()[:10]}...") 
                st.rerun() 

# --- 5. Main Control Panel Interface --- 
st.title("🛡️ Automated Liquidation & Margin Call Engine") 
st.caption(f"On-Chain Asset Representation (Digital Twin): {CONTRACT_ADDRESS}") 

m1, m2, m3 = st.columns(3) 
with m1: 
    st.metric("Total Asset Principal Value", "$10,000,000") 
with m2: 
    st.metric("On-Chain Secondary Volume", f"${total_funded:,.0f}") 
with m3: 
    val = "6.25% Net Yield" if loan_status == "Performing" else "Special Distressed Terms (55% Haircut)" 
    st.metric("Asset Pricing Framework", val) 

st.divider() 

# --- 6. Role-Based Execution Blocks --- 
if user_role == "Lead Bank (Seller)": 
    st.subheader("🏦 Settlement Management Interface (Lead Bank)") 
    if loan_status != "Non-Performing (NPL)": 
        st.info("Portfolio operational parameters performing within tolerance limits.") 
        partner = st.selectbox("Assign Primary Participant Wallet:", options=accounts[1:4]) 
        amt = st.number_input("Syndicate Offering Allocation ($)", value=1000000) 
        if st.button("Commit Syndication Trade"): 
            tx = contract.functions.syndicateShares(partner, int(amt)).transact({'from': lead_bank_wallet}) 
            st.success(f"Syndication Order Confirmed! Blockchain transaction: {tx.hex()}") 
    else: 
        st.warning("Automated Liquidator Flag: Undercollateralization Event.") 
        ask_price = st.slider("Target Liquidation Clearance Pricing (% of Par)", 30, 85, 45) 
        
        mv = (10000000 * ask_price) / 100 
        hc = 10000000 - mv 
        
        new_snapshot = pd.DataFrame([{ 
            "Property Value ($M)": market_value, 
            "Implied Clearance Price ($M)": mv / 1000000, 
            "Risk Haircut ($M)": hc / 1000000 
        }]) 
        st.session_state['metrics_history'] = pd.concat([st.session_state['metrics_history'], new_snapshot], ignore_index=True).tail(15) 
        
        st.subheader("📈 Real-Time Asset Degradation & Liquidation Curves") 
        st.line_chart(st.session_state['metrics_history']) 
        
        if st.button("🚀 Push Update to Secondary Marketplace"): 
            st.session_state['npl_price'] = ask_price 
            st.success(f"Asynchronous update broadcast to marketplace at {ask_price}% of Par.") 
else: 
    st.subheader("💰 Distressed Debt Arbitrage Portal (Hedge Fund)") 
    if loan_status != "Non-Performing (NPL)": 
        st.info("Scanning decentralized asset registries for distressed opportunities...") 
    else: 
        # --- SAFE SIGNATURE READING FOR HEDGE FUND ---
        appraisal_sigs = 0
        if w3.is_connected():
            try:
                appraisal_sigs = contract.functions.getSignatureCount("appraisal").call() 
            except Exception:
                appraisal_sigs = 0
                
        price = st.session_state.get('npl_price', 45) 
        st.error(f"⚠️ DISCOVERY EVENT: Distressed Asset Portfolio Available at {price}% of Face Value") 
        invest_amt = st.number_input("Target Principal Acquisition Target ($)", value=2000000) 
        cost = (invest_amt * price) / 100 
        
        ca, cb = st.columns(2) 
        ca.metric("Face Value of Purchased Rights", f"${invest_amt:,.0f}") 
        cb.metric("Required Capital Deployment Cost", f"${cost:,.0f}", delta=f"-{100-price}% System Discount") 
        
        if appraisal_sigs < 1: 
            st.error("❌ Purchase Prohibited: Cryptographic Appraisal Document must have 1 valid Multi-Sig Attestation inside Vault.") 
            st.button("Confirm Secondary Purchase", disabled=True) 
        else: 
            if st.button("Confirm Secondary Purchase"): 
                tx = contract.functions.syndicateShares(hedge_fund_wallet, int(invest_amt)).transact({'from': lead_bank_wallet}) 
                st.balloons() 
                st.success(f"Liquidation Asset Acquired! Tx Profile: {tx.hex()}") 

# --- 7. Live Ledger Registry & Active Event Feeds --- 
st.markdown("---") 
l1, l2 = st.columns([1, 1]) 
with l1: 
    st.subheader("📊 Current Capital Stack Ledger") 
    st.table(pd.DataFrame({ 
        'Structured Account Role': ['Lead Bank System Holdings', 'Secondary Market Participants'], 
        'Net Capital Balance': ['$10,000,000 Total Gross Allocation', f'${total_funded:,.0f} Total Settled Net'] 
    })) 
with l2: 
    st.subheader("📡 Live Smart Contract Event Stream") 
    logs = fetch_blockchain_events() 
    if logs: 
        st.dataframe(pd.DataFrame(logs), use_container_width=True) 
    else: 
        st.caption("Monitoring node event bus... No recent trades cleared to block history.") 

# --- 8. System Orchestration Reset Engine --- 
st.sidebar.markdown("---") 
st.sidebar.subheader("⚙️ System Control Panel") 
if st.sidebar.button("🔄 Reset Proof-of-Concept Engine"): 
    if 'npl_price' in st.session_state: 
        del st.session_state['npl_price'] 
    if 'metrics_history' in st.session_state: 
        del st.session_state['metrics_history'] 
    if w3.is_connected(): 
        try: 
            tx = contract.functions.syndicateShares(accounts[0], total_funded).transact({'from': accounts[0]}) 
            st.toast("On-Chain Asset State Reset Success!") 
        except Exception: 
            st.toast("Session initialized. Run terminal deployment to clear deep logs.") 
    st.success("Dashboard runtime reset complete.") 
    st.rerun()
