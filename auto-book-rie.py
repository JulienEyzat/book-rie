import datetime
import json

import booker

def get_params():
    # Get params json
    with open("auto_params.json") as file:
        params = json.load(file)
    
    # Eating datetime
    eating_datetime = datetime.datetime.today()
    eating_datetime = eating_datetime.replace(hour=params["eating_hours"]["hour"], minute=params["eating_hours"]["minute"])

    # Nb eaters
    today_weekday = str(datetime.date.today().weekday())
    nb_eaters = params["eaters_by_weekday"][today_weekday]

    # Email
    email = params["email"]

    return eating_datetime, nb_eaters, email

if __name__ == "__main__":
    # Params
    eating_datetime, nb_eaters, email = get_params()

    booker.book_rie(eating_datetime, nb_eaters, email)