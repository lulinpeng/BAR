// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Script} from "forge-std/Script.sol";
import {SimpleStorage} from "../src/SimpleStorage.sol";
import {console} from "forge-std/console.sol";

contract DeploySimpleStorage is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        if (deployerPrivateKey == 0) {
            console.log(unicode"PRIVATE_KEY is not set");
        }

        vm.startBroadcast(deployerPrivateKey);
        SimpleStorage simpleStorage = new SimpleStorage();
        vm.stopBroadcast();

        console.log(unicode"✅ SimpleStorage is deployed successfully");
        console.log(unicode"📄 contract address:", address(simpleStorage));
        console.log(unicode"👤 deployer address:", vm.addr(deployerPrivateKey));
        console.log(unicode"🔢 initial storage value:", simpleStorage.get());

        string memory deploymentInfo = string(
            abi.encodePacked(
                "Deployment Information:\n",
                "Contract Address: ",
                vm.toString(address(simpleStorage)),
                "\n",
                "Deployer: ",
                vm.toString(vm.addr(deployerPrivateKey)),
                "\n",
                "Network: ",
                vm.toString(block.chainid),
                "\n",
                "Timestamp: ",
                vm.toString(block.timestamp)
            )
        );
        console.log(deploymentInfo);
    }

    function deployAndInitialize(uint256 initialValue) external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorage.set(initialValue);
        vm.stopBroadcast();

        console.log(
            unicode"✅ SimpleStorage has been deployed and initialized"
        );
        console.log(unicode"📄 contract address:", address(simpleStorage));
        console.log(unicode"🔢 current storage value:", simpleStorage.get());
    }
}
