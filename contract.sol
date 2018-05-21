pragma solidity ^0.4.21;

contract MedBlockData {
    address emergencyAddress;
    struct MedBlock{
        string ipfsHash;
        bool approved;
        mapping(address=>string) keys;
    }
    
    mapping (string=>address) mobiles;
    mapping (address=>MedBlock[]) data;

    modifier onlyOwner(address a) {
        require(msg.sender==a);
        _;
    }

    function register(string _mobile ) external {
        mobiles[_mobile] = msg.sender;
    }

    function addBlock(string ipfsHash, address _address, string _key) external {
        data[_address].push(MedBlock(ipfsHash, false));
        MedBlock storage medblock = data[_address];
        medblock.keys[_address] = _key;
    }

    function addEmergencyBlock(string ipfsHash, address _address, string _key, string _emergencyKey) external {
        data[_address].push(MedBlock(ipfsHash, false));
        MedBlock storage medblock = data[_address];
        medblock.keys[_address] = _key;
        medblock.keys[emergencyAddress] = _emergencyKey;
    }
    
    function addKey(address patientAddress, int medBlockIndex, address permitAddress, string key) external onlyOwner(patientAddress){
        MedBlock storage medblock = data[patientAddress];
        medblock.keys[permitAddress] = key;
    }
}