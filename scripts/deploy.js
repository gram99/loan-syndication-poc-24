import hre from "hardhat";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { ethers } from "ethers";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function main() {
  console.log("🚀 Initializing Deployment Sequence for Automated Liquidation Engine...");

  // Load contract build artifacts cleanly
  const artifact = await hre.artifacts.readArtifact("LiquidationEngine");
  
  // Directly attach an external provider target to your active Hardhat Node on port 8545
  const provider = new ethers.JsonRpcProvider("http://127.0.0.1:8545");
  const signer = await provider.getSigner(0); // Selects your primary system deployment wallet
  
  console.log(`📡 Connected to node network via deployer address: ${signer.address}`);

  // Construct and execute contract creation factory deployment mechanics
  const factory = new ethers.ContractFactory(artifact.abi, artifact.bytecode, signer);
  const contract = await factory.deploy();
  
  await contract.waitForDeployment();
  const contractAddress = await contract.getAddress();

  console.log(`📡 Contract successfully bound to local EVM at: ${contractAddress}`);

  const deploymentMetadata = {
    address: contractAddress,
    network: hre.network.name,
    timestamp: new Date().toISOString()
  };

  fs.writeFileSync(
    path.join(__dirname, "../deployment.json"),
    JSON.stringify(deploymentMetadata, null, 2)
  );
  console.log("💾 Configuration mapped cleanly into deployment.json");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});