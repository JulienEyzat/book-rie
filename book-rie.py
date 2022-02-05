import datetime
import json
import requests

def get_cookie():
    r = requests.get("https://widget.yoplanning.com/id/90/")
    P = r.cookies["PHPSESSID"]
    return P

def set_headers(P):
    cookie = "PHPSESSID=%s" %(P)
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,fr;q=0.8",
        "content-type": "application/json;charset=UTF-8",
        "cookie": cookie,
        "origin": "https://widget.yoplanning.com",
        "referer": "https://widget.yoplanning.com/id/90/?P=%s" %(P),
        "sec-ch-ua": '"Chromium";v="97", " Not;A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }
    return headers

def get_rie_widget(headers, P):
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
        "P": P
    }
    r = requests.post("https://widget.yoplanning.com/id/90/", params=params, json=get_product_payload)

    return r.json()["datas"]["ptabProduct"][0]

def get_time_widget(headers, P, eating_datetime):
    # Get products of the search day
    search_datetime = eating_datetime.strftime("%Y%m%d")
    get_product_payload = {
        "pIdStructure": "bb7b7eb7-af9b-485d-b327-d8e4d786b0a3",
        "StartDate": search_datetime,
        "EndDate": search_datetime,
        "DisplayProduct": 1,
        "DisplayAccessory": 0,
        "DisplayDiscount": 0,
        "DisplayAvailability": 1,
        "ProductIn": "a785da3a-0a56-40a1-8294-a7768a83aff9"
    }
    params = {
        "controller": "api",
        "method": "getProduct",
        "P": P
    }
    r = requests.post("https://widget.yoplanning.com/id/90/", params=params, json=get_product_payload)

    # Get the widget in the list
    products_dict = r.json()
    time_widget = None
    for product in products_dict["datas"]["ptabProduct"][0]["ptabAvailability"]:
        if product["StartDateTime"] == "%s00000" %(eating_datetime.strftime("%Y%m%d%H%M")):
            time_widget = product
    
    return time_widget

def add_eaters(headers, P, rie_widget, time_widget, nb_eaters):
    add_cart_json = {}
    add_cart_json["product"] = rie_widget
    add_cart_json["qty"] = nb_eaters
    add_cart_json["type"] = "dispos"
    add_cart_json["line"] = time_widget
    params = {
        "controller": "api",
        "method": "addCart",
        "P": P
    }
    r = requests.post("https://widget.yoplanning.com/id/90/", params=params, json=add_cart_json, headers=headers)

def add_eaters_names(headers, P):
    # Get current cart
    params = {
        "controller": "api",
        "method": "options",
        "P": P
    }
    r = requests.get("https://widget.yoplanning.com/id/90/", params=params)
    current_cart = r.json()["datas"]["cart"]

    # Add value of name in cart json
    cart_list_id = next(iter(current_cart["list"]))
    nb_part_in_cart = len(current_cart["list"][cart_list_id]["participants"])
    for i in range(nb_part_in_cart):
        for j in range(2):
            current_cart["list"][cart_list_id]["participants"][i]["ptabField"][j]["value"] = "x"
            current_cart["list"][cart_list_id]["participants"][i]["ptabField"][j]["onError"] = False
        current_cart["list"][cart_list_id]["participants"][i]["defaultPrice"] = 0
        current_cart["list"][cart_list_id]["participants"][i]["defaultPriceHT"] = 0
        current_cart["list"][cart_list_id]["participants"][i]["discount"] = 0
        current_cart["list"][cart_list_id]["participants"][i]["editCard"] = True
        current_cart["list"][cart_list_id]["participants"][i]["nb_participants_by_prod"] = nb_part_in_cart
        current_cart["list"][cart_list_id]["participants"][i]["price"] = 0
        current_cart["list"][cart_list_id]["participants"][i]["priceHT"] = 0
        current_cart["list"][cart_list_id]["participants"][i]["taxes"] = {"details": [], "total_amount": "0.000000"}
        current_cart["list"][cart_list_id]["participants"][i]["taxesAccessories"] = {"details": [], "total_amount": "0.0"}

    # Add other properties in cart json
    current_cart["list"][cart_list_id]["options"]["id"] = 0
    current_cart["list"][cart_list_id]["options"]["isValid"] = True
    current_cart["list"][cart_list_id]["options"]["line"]["pwywPrice"] = None
    current_cart["list"][cart_list_id]["options"]["metaTabAccessory"] = []
    current_cart["list"][cart_list_id]["options"]["oneUndone"] = False
    current_cart["list"][cart_list_id]["options"]["nbPartInCart"] = 1
    current_cart["list"][cart_list_id]["options"]["showThisProd"] = False

    data = {
        "currentCart": current_cart
    }

    # Push names on the site
    params = {
        "controller": "api",
        "method": "none",
        "P": P
    }
    r = requests.post("https://widget.yoplanning.com/id/90/", params=params, json=data, headers=headers)

def set_mail(headers, P, receiver_mail):
    # Valider l'adresse mail
    json_data = {"pEmail": receiver_mail}
    params = {
        "controller": "billing",
        "method": "save",
        "P": P
    }
    r = requests.post("https://widget.yoplanning.com/id/90/", params=params, json=json_data, headers=headers)

def validate_command(headers, P):
    # Validate
    params = {
        "controller": "payment",
        "method": "book",
        "P": P
    }
    r = requests.post("https://widget.yoplanning.com/id/90/", params=params, headers=headers)
    if not r.json()["datas"]["booked"]:
        print("The reservation failed")
    # Clear
    params = {
        "controller": "api",
        "method": "removeAll",
        "P": P
    }
    r = requests.post("https://widget.yoplanning.com/id/90/", params=params, headers=headers)

if __name__ == "__main__":
    P = get_cookie()
    # print(P)
    headers = set_headers(P)
    eating_datetime = datetime.datetime.strptime('2022-02-07 13:45', '%Y-%m-%d %H:%M')
    rie_widget = get_rie_widget(headers, P)
    time_widget = get_time_widget(headers, P, eating_datetime)
    add_eaters(headers, P, rie_widget, time_widget, 1)
    add_eaters_names(headers, P)
    set_mail(headers, P, "jean.dodru@yopmail.com")
    validate_command(headers, P)


