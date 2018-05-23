pragma solidity ^0.4.21;

contract MedBlocks {
    event NumberDeclaration(address indexed patientAddress, string indexed phoneNumber);
    event MedBlock(address indexed patientAddress, string ipfsHash);
    event Key(string indexed ipfsHash, address indexed permittedAddress, string key);
    address public emergencyAddress;
    

    function register(string _mobile) external {
        emit NumberDeclaration(msg.sender, _mobile);
    }

    function addMedBlock(string _ipfsHash, address _patientAddress) external {
        emit MedBlock(_patientAddress, _ipfsHash);
    }
    
    function addKey(string _ipfsHash, address _permittedAddress, string _key) external {
        emit Key(_ipfsHash, _permittedAddress, _key);
    }
    
}