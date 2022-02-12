import datetime
import json
import sys

import yoplanning_api

def get_rie_widget(api):
    res = api.get_product()
    return res["datas"]["ptabProduct"][0]

def get_time_widget(api, eating_datetime):
    # Get products of the search day
    products_dict = api.get_lines(eating_datetime)

    # Print the time and number of persons left
    if products_dict["datas"]["ptabProduct"][0]["ptabAvailability"]:
        print("Places at each hours :")
        for product in products_dict["datas"]["ptabProduct"][0]["ptabAvailability"]:
            hour = datetime.datetime.strptime(product["StartDateTime"], "%Y%m%d%H%M00000").strftime("%Y-%m-%d %H:%M")
            left_persons = product["StockAvailable"]
            print("At %s : %s places left" %(hour, left_persons))

    # Get the widget in the list
    time_widget = None
    for product in products_dict["datas"]["ptabProduct"][0]["ptabAvailability"]:
        if product["StartDateTime"] == "%s00000" %(eating_datetime.strftime("%Y%m%d%H%M")):
            time_widget = product
    
    if time_widget is None:
        print("There is no reservations at this date")
    
    return time_widget

def add_eaters(api, rie_widget, time_widget, nb_eaters):
    # Check if enough places
    if time_widget["StockAvailable"] < nb_eaters:
        print("There is %s places left at this hour but you ask for %s places. The reservation failed." %(time_widget["StockAvailable"], nb_eaters))
        sys.exit()

    # Add to cart
    add_cart_json = {}
    add_cart_json["product"] = rie_widget
    add_cart_json["qty"] = nb_eaters
    add_cart_json["type"] = "dispos"
    add_cart_json["line"] = time_widget
    api.add_cart(add_cart_json)

def add_eaters_names(api):
    # Get current cart
    res = api.get_command_state()
    current_cart = res["datas"]["cart"]

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
    api.set_command_state(data)

def set_mail(api, receiver_mail):
    # Valider l'adresse mail
    r = api.set_receiver_mail(receiver_mail)

def validate_command(api):
    # Validate
    res = api.validate_command()
    if not res["datas"]["booked"]:
        print("The reservation failed")
    # Clear
    api.clear_command()

def book_rie(eating_datetime, nb_eaters, email):
    # Connect to the yoplanning Api
    api = yoplanning_api.YoplanningApi()

    # Reservation
    rie_widget = get_rie_widget(api)
    time_widget = get_time_widget(api, eating_datetime)
    if time_widget is not None:
        add_eaters(api, rie_widget, time_widget, nb_eaters)
        add_eaters_names(api)
        set_mail(api, email)
        validate_command(api)
        print("The reservation succeeded")