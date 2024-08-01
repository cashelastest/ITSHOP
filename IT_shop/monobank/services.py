import requests
from django.conf import settings

class MonobankAPI:
    BASE_URL = 'https://api.monobank.ua/'

    def __init__(self):
        self.token = settings.MONOBANK_TOKEN

    def _get_headers(self):
        return {
            'X-Token': self.token
        }

    def create_invoice(self, amount, redirect_url):
        url = f'{self.BASE_URL}api/merchant/invoice/create'
        headers = self._get_headers()
        data = {
            'amount': int(amount) * 100,  # Сумма в копейках
            'ccy': 980,  # UAH
            'merchantPaymInfo': {
                'reference': 'your_reference_id',
                'destination': 'Payment for services'
            },
            'redirectUrl': redirect_url
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()  # Возвращаем JSON ответ с ошибкой

    def check_payment_status(self, invoice_id):
        url = f'{self.BASE_URL}api/merchant/invoice/status'
        headers = self._get_headers()
        data = {
            'invoiceId': invoice_id
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()  # Возвращаем JSON ответ с ошибкой
