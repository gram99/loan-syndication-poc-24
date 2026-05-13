# 🛡️ Automated Liquidation & Margin Call Engine

**Author:** Gram99
<br>
**Primary Audiences:** Institutional Asset Managers & Commercial Lenders, Secondary Market Debt Buyers & Arbitrageurs, Regulatory Compliance & Operations Officers, and Enterprise Blockchain Architects.

## Project Description:

The project demonstrates a 2026-standard financial infrastructure for the lifecycle management of multifamily loans. It uses ERC-1155 Smart Contracts to manage both the unique underlying asset (NFT) and its fractional participation shares (Fungible Tokens). The project features an automated Liquidation & Margin Call engine that is an enterprise-grade decentralized finance (DeFi) Proof-of-Concept (PoC) that demonstrates an automated corporate debt syndication and secondary market liquidation pipeline. The engine automatically monitors underlying asset evaluations via simulated oracles, trips margin calls upon loan-to-value (LTV) breaches, and handles secondary distribution mechanics through a multi-signature verified asset vault. 

---

## 🚀 Key Features

- **On-Chain Digital Twin:** Every loan is minted as a unique digital asset with a verified contract address.
- **Atomic Syndication:** Lead banks can distribute risk to consortium partners with T+0 instant settlement.
- **NPL Pivot Logic:** Real-time transition from "Performing" to "Non-Performing" status, triggering secondary market listing and valuation haircuts.
- **Dual-Role Dashboard:** Toggle between Lead Bank (Seller) and Hedge Fund (Buyer) perspectives.
- **Digital Vault:** Integrated access to IPFS-verified Appraisal Reports and Phase I Environmental documents.
- **Asset Degradation & Liquidation Curve Charting:** Real-time charting of implied clearance price, property value, and risk haircut.

---

## 🛠️ Technical Stack

- **Blockchain Engine:** Hardhat (Local Private Ethereum Node)
- **Smart Contracts:** Solidity (OpenZeppelin ERC-1155 Standard)
- **Frontend/UI:** Streamlit (Python)
- **Web3 Bridge:** Web3.py
- **Environment:** GitHub Codespaces & GitHub Repository

## 🏗️ System Architecture

The application is structured into three decoupled structural tiers:
1. **Smart Contracts (`Solidity 0.8.20`)**: Enforces state logic for gross par distributions, programmatic syndication ledger re-assignments, and cryptographic multi-sig vault attestation tracking.
2. **EVM Tooling (`Hardhat 3 / EDR`)**: Pure ECMAScript Module (ESM) environment driving compilation, deployment tracking configurations, and a local simulated consensus network.
3. **Control Interface (`Streamlit`)**: A reactive risk dashboard featuring conditional role perspectives, live contract event telemetry streams, and session clearing tools.

---

## 🚦 Core Operational Workflows

### 1. Primary Syndication Setup (Lead Bank)
The loan originates at a **$10,000,000 Gross Principal Balance** assigned to the Lead Bank holding account. While the property evaluation remains healthy ($\ge \$10\text{M}$), the Lead Bank can distribute allocations to participating institutional wallets.

### 2. Automated Margin Call Trigger
* **The Threshold**: When the Property Market Value drops below **$10.0M**, the system identifies a breach of required coverage limits.
* **The Automation**: The interface instantly locks primary syndication paths, flags the asset as **Non-Performing (NPL)**, and enables a secondary market auction pane.

### 3. Market Stress Test Clearance (55% Haircut)
* To clear risk, the Lead Bank slides market clearance pricing to **45% of Par** (representing a strict 55% discount haircut).
* Clicking *Push Update to Secondary Marketplace* serializes state changes across the dashboard environment.

### 4. Cryptographic Vault Review & Secondary Execution
* Changing perspectives to the **Hedge Fund Buyer** updates the terminal viewport.
* The buyer must navigate to the *Multi-Sig Document Vault* and click *Sign & Attest Appraisal*. 
* The on-chain ledger records the identity signature. Once requirements are checked, the *Confirm Secondary Purchase* trigger unlocks, liquidating the target par rights via a live block transaction.

---

## 🔧 Installation & Dependencies

The system runs completely enclosed within a standard Node.js and Python container space:

```bash
# Node JS Core Tooling
npm install --save-dev hardhat @nomicfoundation/hardhat-ethers ethers

# Python Requirements
pip install streamlit web3 pandas
```

---

## 🚀 One-Click Execution Guide

To initialize the entire infrastructure suite, execute the automated orchestration handler script from your workspace root terminal:

```bash
./start_poc.sh
```

The automation script cleans the workspace environment, initializes an internal blockchain server on port `8545`, maps out contract data inside `deployment.json`, and deploys the functional dashboard.

---

## 📈 Demo Workflow

**1. Syndication:** As a Lead Bank, select a partner from the dropdown and syndicate $1,000,000. Refresh to see the "On-Chain Funding" metric update.
<br>
<br>
**2. Distress Simulation:** Use the sidebar slider to move the loan to Non-Performing (NPL). Observe the valuation "Haircut" chart.
<br>
<br>
**3. Secondary Trade:** Switch roles to Hedge Fund, review the Appraisal in the Digital Vault, and purchase the distressed debt at the listed market discount.

---

## 📘 User Guide: Institutional NPL & Syndication Marketplace

Framework: Ethereum (ERC-1155) & Streamlit

1. **Overview** This platform provides a blockchain-based "Digital Twin" environment for managing multifamily loans. It enables Lead Banks to syndicate primary debt and manage distressed assets (NPLs) via a transparent, on-chain secondary marketplace.

2. **System Roles**

## 🏦 Lead Bank (Seller)

- **Primary Action:** Distribute loan risk to partner institutions.
- **NPL Management:** Toggle asset status to "Non-Performing" to trigger secondary market listings and capital haircuts.
- **Vault Control:** Manage the "Digital Vault" containing appraisals and environmental reports.

## 💰 Hedge Fund (Buyer)

- **Primary Action:** Scout for distressed debt opportunities.
- **Due Diligence:** Review on-chain verified documents in the Digital Vault.
- **Execution:** Purchase fractional loan shares at a market-determined discount.

3. **Operational Workflow**
   
## Phase A: Primary Syndication

1. Ensure the status is set to "Performing."
2. Select a Partner Bank address from the consortium dropdown.
3. Enter the Syndication Amount (e.g., $1,000,000).
4. Click "Finalize Syndication" to mint shares directly to the partner's wallet.

## Phase B: NPL Pivot & Valuation
1. Toggle the Loan Performance Status to "Non-Performing (NPL)."
2. The dashboard will shift to a "Distressed" state (Red UI).
3. Use the Secondary Market Slider to set the "Ask Price" (e.g., 65% of Par).
4. Review the Valuation Analysis chart to visualize the implied capital haircut.

## Phase C: Secondary Sale
1. Click "List NPL for Secondary Sale" to broadcast the asset.
2. Switch the view to "Hedge Fund (Buyer)."
3. Execute the purchase to simulate the transfer of distressed debt to a third-party fund.

4. **The Digital Vault**
   
Located in the sidebar, the Digital Vault provides an immutable link between the financial
asset and its physical due diligence.

- **Appraisal Reports:** Real-time property valuations.
- **Phase I Environmental:** Risk assessment documentation.
- **Verification:** All documents are noted as "Verified On-Chain," representing an IPFSbacked audit trail.

---

## 📺 Screenshots

<img width="1869" height="923" alt="Screenshot 2026-05-13 at 2 01 57 PM" src="https://github.com/user-attachments/assets/00aa3100-f834-4635-9745-d6779c3510c4" />
<br>
<br>
<img width="1881" height="924" alt="Screenshot 2026-05-13 at 2 01 29 PM" src="https://github.com/user-attachments/assets/78736608-5a4a-4177-bd42-36adf5b6c2f2" />
<br>
<br>
<img width="1858" height="835" alt="Screenshot 2026-05-13 at 2 02 47 PM" src="https://github.com/user-attachments/assets/b252ff14-808b-49e8-b7c4-5efa7f47c52d" />
<br>
<br>
<img width="1897" height="871" alt="Screenshot 2026-05-13 at 2 03 22 PM" src="https://github.com/user-attachments/assets/79b519f9-9ea9-49b2-8d35-64d349886e7b" />
<br>
<br>
<img width="1854" height="936" alt="Screenshot 2026-05-13 at 2 02 24 PM" src="https://github.com/user-attachments/assets/e1e2ae70-dec2-44a9-a6b1-3b2e1c2d99f6" />

