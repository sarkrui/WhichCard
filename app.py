from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_data():
    currency = request.args.get('currency', 'usd')
    URL = f"https://www.kylc.com/huilv/whichcard.html?ccy={currency}&amt=10000"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', {'id': 'content_table'})

    rows = table.find('tbody').find_all('tr')

    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip().replace('pay', '').replace('\n', '').replace(' ', '').replace('direct-multi-currency','').replace('normal','') for col in cols]
        record = {
            "Number": cols[0],
            "CardType": cols[1],
            "ExchangeRate": cols[2],
            "ForeignCurrency": cols[3],
            "ServiceFee": cols[4],
            "PurchaseRate": cols[5],
            "Result": cols[6],
        }
        data.append(record)

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)