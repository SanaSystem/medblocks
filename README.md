![MedBlocks Logo](https://i.imgur.com/Dx4LfC2.png)

With Medblocks you can store your medical records (and other documents actually) securely on the IPFS. It will have a reference of it on BigChainDB with permission keys, so you can comtrol who has access to your data.

## Installation
MedBlocks works perfectly on Linux. It should work on windows, but I haven't tested it because some of the dependencies required build tools for windows (which was a pain to install)

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
```
Check installation
```
medblocks --version
```

If you have any trouble while importing rapid-json, try running it as a normal script instead:

```
pip install -r requirements.txt
```
Check if installed
```
python medblocks.py --verion
```

## Usage
To bring up the documentation
```
medblocks --help
```

The working of medblocks is explained in detail in this [article]().

Also check out this video demonstration for more clarity:

[Video Demonstration](https://www.youtube.com/watch?v=0PrUr3bQdwM)
