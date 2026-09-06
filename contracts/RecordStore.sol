// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RecordStore {
    mapping(uint => bytes32) public records;
    uint public recordCount;

    event RecordStored(uint id, bytes32 hash);

    function storeRecord(bytes32 hash) public returns (uint) {
        uint currentId = recordCount;
        records[currentId] = hash;
        emit RecordStored(currentId, hash);
        recordCount++;
        return currentId;
    }

    function getRecord(uint id) public view returns (bytes32) {
        return records[id];
    }
}
