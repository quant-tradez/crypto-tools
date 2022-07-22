# Crypto scanner

- Install git on your computer. 
- Make sure you have python 3 and pip installed on your computer. 
- Open a terminal.
- Clone the repository: 
```
git clone https://github.com/quant-tradez/crypto-tools.git
```
- cd into the repository: 
```
cd crypto-tools
```
- Create a binance api key: [binance.com/en/support/faq/360002502072]()
- Create a file called config.py with two variables containing your api key and secret : 
```python
api_key = '<copy-your-api-key-here>'
api_secret = '<copy-your-api-secret-here>'
```
- Install virtualenv: 
```
pip install virtualenv
```
- Create virtualenv for the project: 
```
virtualenv venv
```
- Activate virtual env:
```
source venv/bin/activate
```
- Install package requirements:
```
pip install -r requirements.txt
```
- All ready. Run it ! 
```
python scanner.py --ticker_suffix 'USDT' --start_str '1 day ago UTC'
```

![Preview](https://github.com/quant-tradez/crypto-tools/blob/master/screenshots/screenshot.png)
