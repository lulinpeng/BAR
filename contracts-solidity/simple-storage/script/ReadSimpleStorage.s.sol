// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Script} from "forge-std/Script.sol";
import {console} from "forge-std/console.sol";

interface ISimpleStorage {
    function get() external view returns (uint256);
    function owner() external view returns (address);
    function getBalance() external view returns (uint256);
}

contract ReadSimpleStorage is Script {
    function run() external view {
        address payable contractAddress = payable(
            vm.envAddress("CONTRACT_ADDRESS")
        );

        ISimpleStorage simpleStorage = ISimpleStorage(contractAddress);
        console.log(unicode"📄 contract address: %s", contractAddress);
        console.log(unicode"🔢 current value: %s", simpleStorage.get());
        console.log(unicode"👤 contract owner: %s", simpleStorage.owner());
        console.log(
            unicode"💰 contract balance: %s ETH",
            vm.toString(address(contractAddress).balance / 1e18)
        );
        console.log(unicode"🌐 chain ID: %s", block.chainid);
    }
}
