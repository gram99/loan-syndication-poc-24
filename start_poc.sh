#!/bin/bash
echo "🛑 Clearing previous running processes..."
pkill -f "hardhat" || true
pkill -f "streamlit" || true

echo "🚀 1. Launching Hardhat Network Node in background..."
npx hardhat node > hardhat_node.log 2>&1 &
NODE_PID=$!

echo "⏳ Waiting for local block network to initialize..."
sleep 5

echo "📜 2. Running Smart Contract Deployment Engine..."
npx hardhat run scripts/deploy.js --network localhost

echo "🛡️ 3. Initializing Streamlit UI Control Dashboard..."
streamlit run app.py
