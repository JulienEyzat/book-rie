Command places at the RIE

# INSTALLATION

Install python3.

Install the dependencies

    pip3 install -r requirements.txt

# USAGE

    python3 book-rie.py [-h] [-d DATE] [-t TIME] [-p PERSONS] -e EMAIL

# OPTIONS

    -h, --help                      show this help message and exit.
    -d DATE, --date DATE            The date for the reservation.
                                    Format : "YYYY-mm-dd"
                                    Default : Today
    -t TIME, --time TIME            The time for the reservation
                                    Format : "HH-MM"
                                    Default : 12:15
    -p PERSONS, --persons PERSONS   Number of persons eating at the RIE.
                                    Default : 15
    -e EMAIL, --email EMAIL         The mail of the person receiving the reservation.
                                    Required.