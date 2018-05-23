event_contract_abi = """[
	{
		"constant": false,
		"inputs": [
			{
				"name": "_ipfsHash",
				"type": "string"
			},
			{
				"name": "_permittedAddress",
				"type": "address"
			},
			{
				"name": "_key",
				"type": "string"
			}
		],
		"name": "addKey",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_ipfsHash",
				"type": "string"
			},
			{
				"name": "_patientAddress",
				"type": "address"
			}
		],
		"name": "addMedBlock",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_something",
				"type": "string"
			}
		],
		"name": "emitString",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"name": "patientAddress",
				"type": "address"
			},
			{
				"indexed": true,
				"name": "phoneNumber",
				"type": "string"
			}
		],
		"name": "NumberDeclaration",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"name": "patientAddress",
				"type": "address"
			},
			{
				"indexed": false,
				"name": "ipfsHash",
				"type": "string"
			}
		],
		"name": "MedBlock",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"name": "ipfsHash",
				"type": "string"
			},
			{
				"indexed": true,
				"name": "permittedAddress",
				"type": "address"
			},
			{
				"indexed": false,
				"name": "key",
				"type": "string"
			}
		],
		"name": "Key",
		"type": "event"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_mobile",
				"type": "string"
			}
		],
		"name": "register",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"name": "someString",
				"type": "string"
			}
		],
		"name": "String",
		"type": "event"
	}
]"""