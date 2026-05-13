# 🛡️ Automated Liquidation & Margin Call Engine

**Author:** Gram99
<br>
**Primary Audience:** Institutional Asset Managers & Commercial Lenders, Secondary Market Debt Buyers & Arbitrageurs, Regulatory Compliance & Operations Officers, and Enterprise Blockchain Architects.

---

## Description of Proof of Concept (PoC) Engine

The Automated Liquidation & Margin Call Engine is a enterprise-grade decentralized finance (DeFi) Proof-of-Concept (PoC0 that demonstrates an automated corporate debt syndication and secondary market liquidation pipeline. The engine automatically monitors underlying asset evaluations via simulated oracles, trips margin calls upon loan-to-value (LTV) breaches, and handles secondary distribution mechanics through a multi-signature verified asset vault.

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

