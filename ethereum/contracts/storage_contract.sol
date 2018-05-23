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
        MedBlock[] storage medblocks = data[_address];
        MedBlock storage medblock;
        medblock.ipfsHash = ipfsHash;
        medblock.approved = false;
        medblock.keys[_address] = _key;
        medblocks.push(medblock);
    }

    function addEmergencyBlock(string ipfsHash, address _address, string _key, string _emergencyKey) external {
        MedBlock[] storage medblocks = data[_address];
        MedBlock storage medblock;
        medblock.ipfsHash = ipfsHash;
        medblock.approved = false;
        medblock.keys[_address] = _key;
        medblock.keys[emergencyAddress] = _emergencyKey;
        medblocks.push(medblock);
    }
    
    function addKey(address patientAddress, uint medBlockIndex, address permitAddress, string key) external onlyOwner(patientAddress){
        MedBlock[] storage medblocks = data[patientAddress];
        MedBlock storage medblock = medblocks[medBlockIndex];
        medblock.keys[permitAddress] = key;
    }
}