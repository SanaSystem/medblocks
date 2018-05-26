# MedBlocks

![MedBlocks Logo](https://i.imgur.com/Dx4LfC2.png)

With Medblocks you can store your medical records (and other documents actually) securely on the IPFS. It will have a reference of it on BigChainDB with permission keys, so you can comtrol who has access to your data.

## Install
Install build tools first:
```
sudo apt install build-essential
sudo apt install python-dev
```
Clone the repository
```
git clone https://github.com/sidharthramesh/medblocks.git
cd medblocks

```
Install as command line tool
```
pip install -e .
medblocks --version
```

If you have any trouble while importing rapid-json, try running it as a normal script instead:

```
pip install -r requirements.txt
python medblocks.py --verion
```