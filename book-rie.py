import argparse
import datetime

import booker

def parse_arguments():
    parser = argparse.ArgumentParser(description='Command places at the RIE')
    parser.add_argument('-d', "--date", type=str, default=datetime.date.today().strftime("%Y-%m-%d"), help='The date for the reservation')
    parser.add_argument('-t', "--time", type=str, default="12:15", help='The time (hours:minutes) for the reservation')
    parser.add_argument('-p', "--persons", type=int, default=15, help='Number of persons eating at the RIE')
    parser.add_argument('-e', "--email", type=str, required=True, help='The mail of the person receiving the reservation')
    args = parser.parse_args()
    return args

def clean_arguments(args):
    eating_datetime = datetime.datetime.strptime("%s %s" %(args.date, args.time), '%Y-%m-%d %H:%M')
    nb_eaters = args.persons
    email = args.email
    return eating_datetime, nb_eaters, email

if __name__ == "__main__":
    # Args
    args = parse_arguments()
    eating_datetime, nb_eaters, email = clean_arguments(args)

    booker.book_rie(eating_datetime, nb_eaters, email)
