import datetime
import requests

class YoplanningApi:

    def __init__(self):
        self.base_url = "https://widget.yoplanning.com/id/90/"
        self.set_cookie()
        self.set_headers()

    def set_cookie(self):
        r = requests.get(self.base_url)
        self.php_cookie = r.cookies["PHPSESSID"]

    def set_headers(self):
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fr;q=0.8",
            "content-type": "application/json;charset=UTF-8",
            "cookie": "PHPSESSID=%s" %self.php_cookie,
            "origin": "https://widget.yoplanning.com",
            "referer": "https://widget.yoplanning.com/id/90/?P=%s" %self.php_cookie,
            "sec-ch-ua": '"Chromium";v="97", " Not;A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
        }

    def get_product(self):
        get_product_payload = {
            "pIdStructure":"bb7b7eb7-af9b-485d-b327-d8e4d786b0a3",
            "StartDate":"20220201",
            "isFilterList":"1",
            "DisplayProduct":"1",
            "DisplayCategory":"1"
        }
        params = {
            "controller": "api",
            "method": "getProduct",
            "P": self.php_cookie
        }
        r = requests.post(self.base_url, params=params, json=get_product_payload)
        return r.json()
        
    def get_lines(self, lines_date):
        search_date = lines_date.strftime("%Y%m%d")
        get_product_payload = {
            "pIdStructure": "bb7b7eb7-af9b-485d-b327-d8e4d786b0a3",
            "StartDate": search_date,
            "EndDate": search_date,
            "DisplayProduct": 1,
            "DisplayAccessory": 0,
            "DisplayDiscount": 0,
            "DisplayAvailability": 1,
            "ProductIn": "a785da3a-0a56-40a1-8294-a7768a83aff9"
        }
        params = {
            "controller": "api",
            "method": "getProduct",
            "P": self.php_cookie
        }
        r = requests.post(self.base_url, params=params, json=get_product_payload)
        return r.json()

    def add_cart(self, cart_json):
        params = {
            "controller": "api",
            "method": "addCart",
            "P": self.php_cookie
        }
        r = requests.post(self.base_url, params=params, json=cart_json, headers=self.headers)
        return r.json()

    def get_command_state(self):
        params = {
            "controller": "api",
            "method": "options",
            "P": self.php_cookie
        }
        r = requests.get(self.base_url, params=params)
        return r.json()

    def set_command_state(self, new_state):
        params = {
            "controller": "api",
            "method": "none",
            "P": self.php_cookie
        }
        r = requests.post(self.base_url, params=params, json=new_state, headers=self.headers)
        return r.json()

    def set_receiver_mail(self, receiver_mail):
        json_data = {"pEmail": receiver_mail}
        params = {
            "controller": "billing",
            "method": "save",
            "P": self.php_cookie
        }
        r = requests.post(self.base_url, params=params, json=json_data, headers=self.headers)
        return r.json()

    def validate_command(self):
        params = {
            "controller": "payment",
            "method": "book",
            "P": self.php_cookie
        }
        r = requests.post(self.base_url, params=params, headers=self.headers)
        return r.json()

    def clear_command(self):
        params = {
            "controller": "api",
            "method": "removeAll",
            "P": self.php_cookie
        }
        r = requests.post(self.base_url, params=params, headers=self.headers)
        return r.json()