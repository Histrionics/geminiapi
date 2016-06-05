""" Wrapper for the Gemini API """

import requests
import time
import base64
import hashlib
import json
import hmac

class GeminiSession:

    def __init__(self, apiKey, apiSecret, sandbox=False):
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.sandbox = sandbox

        if sandbox is False:
            self.apiUrl = 'https://api.gemini.com/v1/'
        else:
            self.apiUrl = 'https://api.sandbox.gemini.com/v1/'

    def get_symbols(self):
        try: 
            return requests.get(self.apiUrl + 'symbols').json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_ticker(self, symbol):
        try: 
            return requests.get(self.apiUrl + 'pubticker/' + symbol).json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_current_order_book(self, symbol, limit_bids=None, limit_asks=None):
        limits = {}
        if limit_bids is not None:
            limits["limit_bids"] = limit_bids
        if limit_asks is not None:
            limits["limit_asks"] = limit_asks
        
        try:
            return requests.get(self.apiUrl + symbol, params=limits).json()
        except requests.exceptions.RequestException as e:
            raise e

    def new_order(self, symbol, amount, price, side, order_type=None, client_order_id=None):
        
        fields = {
                'request': '/v1/order/new',
                'nonce': self.get_nonce(),

                # Request-specific items
                'symbol': symbol,       # Or any symbol from the /symbols api
                'amount': amount,        # Once again, a quoted number
                'price': price,
                'side': side,            # must be "buy" or "sell"
                'type': 'exchange limit',  # the order type; only "exchange limit" supported
        }

        if client_order_id is not None:
            fields['client_order_id'] = client_order_id
        
        if order_type is not None:
            fields['order_type'] = [order_type]
        
        try:
            return requests.post(self.apiUrl + 'order/new', headers=self.create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e
    
    def get_nonce(self):
        return int(round(time.time() * 1000))


    def cancel_order(self, order_id):
        fields = {
            'request': '/v1/order/cancel',
            'nonce': self.get_nonce(),
            'order_id': order_id
        }

        try:
            return requests.post(self.apiUrl + 'order/cancel', headers=self.create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def cancel_all_session_orders(self):
        fields = {
            'request': '/v1/order/cancel/session',
            'nonce': self.get_nonce(),
        }

        try:
            return requests.post(self.apiUrl + 'order/cancel/session', headers=self.create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e
    
    def cancel_all_active_orders(self):
        fields = {
            'request': '/v1/order/cancel/all',
            'nonce': self.get_nonce(),
        }

        try:
            return requests.post(self.apiUrl + 'order/cancel/all', headers=self.create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_order_status(self, order_id):
        fields = {
            'request': '/v1/order/status',
            'nonce': self.get_nonce(),
            'order_id': order_id
        }

        try:
            return requests.post(self.apiUrl + 'order/status', headers=self.create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_all_order_status(self):
        fields = {
            'request': '/v1/order',
            'nonce': self.get_nonce(),
        }

        try:
            return requests.post(self.apiUrl + 'order/status', headers=self.create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_past_trades(self, symbol, limit_trades=None, timestamp=None):
        fields = {
            'request': '/v1/mytrades',
            'nonce': self.get_nonce(),
            'symbol': symbol,
        }

        if limit_trades is not None:
            fields["limit_trades"] = limit_trades

        if timestamp is not None:
            fields["timestamp"] = timestamp

        try:
            return requests.post(self.apiUrl + 'mytrades', headers=self.create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_trade_volume(self):
        fields = {
            'request': '/v1/tradevolume',
            'nonce': self.get_nonce(),
        }

        try:
            return requests.post(self.apiUrl + 'tradevolume', headers=self.create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_balances(self):
        fields = {
            'request': '/v1/balances',
            'nonce': self.get_nonce(),
        }

        try:
            return requests.post(self.apiUrl + 'balances', headers=self.create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def heartbeat(self):
        fields = {
            'request': '/v1/heartbeat',
            'nonce': self.get_nonce(),
        }

        try:
            return requests.post(self.apiUrl + 'heartbeat', headers=self.create_payload(fields)).json()
        except requests.exceptions.RequestException as e:
            raise e

    def create_payload(self, fields):

        encodedFields = base64.b64encode(json.dumps(fields).encode())

        headers = {
            'X-GEMINI-APIKEY': self.apiKey,
            'X-GEMINI-PAYLOAD': encodedFields,
            'X-GEMINI-SIGNATURE':  hmac.new(self.apiSecret.encode(), encodedFields, digestmod=hashlib.sha384).hexdigest()
        }

        return headers