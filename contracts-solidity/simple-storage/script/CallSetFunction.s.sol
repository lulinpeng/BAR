// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Script} from "forge-std/Script.sol";
import {SimpleStorage} from "../src/SimpleStorage.sol";
import {console} from "forge-std/console.sol";

contract CallSetFunction is Script {
    // address payable constant CONTRACT_ADDRESS =
    //     payable(0x9089bc120Ab13F8e831AA5f3D2a46BC8aa3a5a22);

    function run() external {
        address payable contractAddress = payable(
            vm.envAddress("CONTRACT_ADDRESS")
        );

        uint256 privateKey = vm.envUint("PRIVATE_KEY");

        console.log(unicode"=== calling set function ===");
        console.log(unicode"contract address: %s", contractAddress);
        console.log(unicode"caller: %s", vm.addr(privateKey));
        console.log(
            unicode"current storage value: %s",
            SimpleStorage(contractAddress).get()
        );

        uint256 newValue = 888;

        vm.startBroadcast(privateKey);
        SimpleStorage(contractAddress).set(newValue);
        vm.stopBroadcast();

        console.log(unicode"✅ set(%s) is called successfully", newValue);

        uint256 currentValue = SimpleStorage(contractAddress).get();
        console.log(unicode"✅ current storage value: %s", currentValue);
    }

    function setMultipleValues() external {
        uint256 privateKey = vm.envUint("PRIVATE_KEY");
        address payable contractAddress = payable(
            vm.envAddress("CONTRACT_ADDRESS")
        );
        uint256[] memory values = new uint256[](3);
        values[0] = 100;
        values[1] = 200;
        values[2] = 300;

        vm.startBroadcast(privateKey);

        for (uint256 i = 0; i < values.length; i++) {
            console.log("value[%d]: %s", i, values[i]);
            SimpleStorage(contractAddress).set(values[i]);
        }

        vm.stopBroadcast();

        console.log("final value: %s", SimpleStorage(contractAddress).get());
    }
}
