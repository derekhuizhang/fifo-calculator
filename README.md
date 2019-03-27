# fifo-calculator
Basic implementation of FIFO calculator for portfolio management
## Usage
```
usage: fifo.py [-h] file_name

Implementation of FIFO calculator.

positional arguments:
  file_name   Path to CSV file of ledger

optional arguments:
  -h, --help  show this help message and exit
```

## How to run
1. Install and activate venv. Then install all dependencies by running:
```
virtualenv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
2. Run fifo calculator on desired test files: 
```
python fifo.py [path to test file]
```

## Design considerations
1. If the current amount of an asset is zero but P/L is nonzero (meaning that the asset was bought and then sold in the same amounts, but the price may have been different in buying and selling that asset), then the asset is not included in the count of total assets, but is included in the P/L. This is most consistent with common sense: if a portfolio does not presently include an asset, then it is not within the portfolio's asset count. However, it is still important to show how much realized profit or loss originated from an asset to provide information for future moves, so the asset is included in the P/L.
2. If the P/L is zero, it is still included in the P/L. This is consistent with the sample outputs. Also, it is important to show that the buying and selling of an asset resulted in 0 realized P/L because that provides interesting information about buy and selling timing if, for instance, the price fluctuated a lot within the past year.
3. A deque was used to record transactions as it provides O(1) implementation of insertion and removal. 
