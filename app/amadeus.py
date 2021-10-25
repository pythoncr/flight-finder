import logging
from datetime import datetime, timedelta

import boto3
import requests

import utils

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s - %(message)s")
log = utils.config_logger(__name__, logging.DEBUG)
TOKEN_API_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHTS_OFFERS_API_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

client = boto3.client("ssm")
get_parameter = lambda k: client.get_parameter(Name=k, WithDecryption=True)["Parameter"]["Value"]
CONFIG = {
    "AMADEUS_ACCESS_TOKEN": get_parameter("AMADEUS_ACCESS_TOKEN"),
    "AMADEUS_CLIENT_ID": get_parameter("AMADEUS_CLIENT_ID"),
    "AMADEUS_CLIENT_SECRET": get_parameter("AMADEUS_CLIENT_SECRET"),
    "AMADEUS_TOKEN_EXPIRES_IN": get_parameter("AMADEUS_TOKEN_EXPIRES_IN"),
    "AMADEUS_TOKEN_ISSUED_DATE": get_parameter("AMADEUS_TOKEN_ISSUED_DATE"),
}


# We need to save this somewhere :)
token_entry = {
    "token_info": {
        "access_token": CONFIG["AMADEUS_ACCESS_TOKEN"],
        "expires_in": 1799,
        "state": "approved",
        "scope": "",
    },
    "issued_timestamp": CONFIG["AMADEUS_TOKEN_ISSUED_DATE"],
}


def is_token_expired() -> bool:
    log.info(token_entry)
    issued_date = CONFIG["AMADEUS_TOKEN_ISSUED_DATE"]
    access_token = CONFIG["AMADEUS_ACCESS_TOKEN"]
    token_expires_in = int(CONFIG["AMADEUS_TOKEN_EXPIRES_IN"])
    if access_token and issued_date:
        date_from_token = datetime.strptime(issued_date, "%Y-%m-%d %H:%M:%S.%f")
        log.info(f"Date from token {date_from_token}")
        past = datetime.now() - timedelta(seconds=token_expires_in)
        if past > date_from_token:
            return True
        else:
            return False
    # Default to True
    return True


def get_token() -> str:
    if is_token_expired():
        log.info("Token is expired, generating a new one")
        payload = {
            "grant_type": "client_credentials",
            "client_id": CONFIG["AMADEUS_CLIENT_ID"],
            "client_secret": CONFIG["AMADEUS_CLIENT_SECRET"],
        }

        log.info(f"Send to API: {payload}")
        result = requests.post(TOKEN_API_URL, data=payload)
        issued_timestamp = datetime.now()
        res = result.json()
        log.info(f"Response from API: {result.json()}")

        # TODO: Store token from result into DynamoDB? Secret? somewhere...
        # new_token_entry = {"token_info": res, "issued_timestamp": issued_timestamp}
        CONFIG["AMADEUS_ACCESS_TOKEN"] = res["access_token"]
        CONFIG["AMADEUS_TOKEN_ISSUED_DATE"] = str(issued_timestamp)
        log.info(CONFIG["AMADEUS_TOKEN_ISSUED_DATE"])
        # token_entry["issued_timestamp"] = issued_timestamp

        if res["access_token"]:
            return res["access_token"]
    else:
        # use the existing token
        log.info("Token is still valid, reusing")
        return CONFIG["AMADEUS_ACCESS_TOKEN"]


def get_travelers(adults, children):
    num_passengers = 1
    travelers = []
    for i in range(0, adults):
        travelers.append({"id": num_passengers, "travelerType": "ADULT"})
        num_passengers += 1
    for i in range(0, children):
        travelers.append({"id": num_passengers, "travelerType": "CHILD"})
        num_passengers += 1

    return travelers


def get_offers(origin, destination, adults, children, departure_date, arrival_date, currency, qty_offers):
    payload = {
        "currencyCode": currency,
        "originDestinations": [
            {
                "id": "1",
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDateTimeRange": {"date": departure_date},
            },
            {
                "id": "2",
                "originLocationCode": destination,
                "destinationLocationCode": origin,
                "departureDateTimeRange": {"date": arrival_date},
            },
        ],
        "travelers": get_travelers(adults, children),
        "sources": ["GDS"],
        "searchCriteria": {"maxFlightOffers": qty_offers},
    }

    auth_token = get_token()
    headers = {"Authorization": "Bearer " + auth_token}
    response = requests.post(FLIGHTS_OFFERS_API_URL, json=payload, headers=headers)
    result = parse_response(response.json())
    return result


sample_response = {
    "meta": {"count": 2},
    "data": [
        {
            "type": "flight-offer",
            "id": "1",
            "source": "GDS",
            "instantTicketingRequired": False,
            "nonHomogeneous": False,
            "oneWay": False,
            "lastTicketingDate": "2021-10-16",
            "numberOfBookableSeats": 9,
            "itineraries": [
                {
                    "duration": "PT2H45M",
                    "segments": [
                        {
                            "departure": {"iataCode": "SJO", "terminal": "M", "at": "2021-11-01T10:10:00"},
                            "arrival": {"iataCode": "MIA", "at": "2021-11-01T14:55:00"},
                            "carrierCode": "AV",
                            "number": "690",
                            "aircraft": {"code": "320"},
                            "duration": "PT2H45M",
                            "id": "1",
                            "numberOfStops": 0,
                            "blacklistedInEU": False,
                        }
                    ],
                },
                {
                    "duration": "PT3H3M",
                    "segments": [
                        {
                            "departure": {"iataCode": "MIA", "at": "2021-11-10T13:20:00"},
                            "arrival": {"iataCode": "SJO", "terminal": "M", "at": "2021-11-10T15:23:00"},
                            "carrierCode": "AV",
                            "number": "691",
                            "aircraft": {"code": "320"},
                            "duration": "PT3H3M",
                            "id": "2",
                            "numberOfStops": 0,
                            "blacklistedInEU": False,
                        }
                    ],
                },
            ],
            "price": {
                "currency": "USD",
                "total": "310.50",
                "base": "88.00",
                "fees": [{"amount": "0.00", "type": "SUPPLIER"}, {"amount": "0.00", "type": "TICKETING"}],
                "grandTotal": "310.50",
                "additionalServices": [{"amount": "70.00", "type": "CHECKED_BAGS"}],
            },
            "pricingOptions": {"fareType": ["PUBLISHED"], "includedCheckedBagsOnly": False},
            "validatingAirlineCodes": ["AV"],
            "travelerPricings": [
                {
                    "travelerId": "1",
                    "fareOption": "STANDARD",
                    "travelerType": "ADULT",
                    "price": {"currency": "USD", "total": "161.55", "base": "50.00"},
                    "fareDetailsBySegment": [
                        {
                            "segmentId": "1",
                            "cabin": "ECONOMY",
                            "fareBasis": "UMOB1BT9",
                            "brandedFare": "S",
                            "class": "U",
                            "includedCheckedBags": {"quantity": 0},
                        },
                        {
                            "segmentId": "2",
                            "cabin": "ECONOMY",
                            "fareBasis": "UMOB1BT9",
                            "brandedFare": "S",
                            "class": "U",
                            "includedCheckedBags": {"quantity": 0},
                        },
                    ],
                },
                {
                    "travelerId": "2",
                    "fareOption": "STANDARD",
                    "travelerType": "CHILD",
                    "price": {"currency": "USD", "total": "148.95", "base": "38.00"},
                    "fareDetailsBySegment": [
                        {
                            "segmentId": "1",
                            "cabin": "ECONOMY",
                            "fareBasis": "UMOB1BT9",
                            "brandedFare": "S",
                            "class": "U",
                        },
                        {
                            "segmentId": "2",
                            "cabin": "ECONOMY",
                            "fareBasis": "UMOB1BT9",
                            "brandedFare": "S",
                            "class": "U",
                        },
                    ],
                },
            ],
        },
        {
            "type": "flight-offer",
            "id": "2",
            "source": "GDS",
            "instantTicketingRequired": False,
            "nonHomogeneous": False,
            "oneWay": False,
            "lastTicketingDate": "2021-10-16",
            "numberOfBookableSeats": 9,
            "itineraries": [
                {
                    "duration": "PT2H45M",
                    "segments": [
                        {
                            "departure": {"iataCode": "SJO", "terminal": "M", "at": "2021-11-01T10:10:00"},
                            "arrival": {"iataCode": "MIA", "at": "2021-11-01T14:55:00"},
                            "carrierCode": "CM",
                            "number": "690",
                            "aircraft": {"code": "320"},
                            "duration": "PT2H45M",
                            "id": "1",
                            "numberOfStops": 0,
                            "blacklistedInEU": False,
                        }
                    ],
                },
                {
                    "duration": "PT8H5M",
                    "segments": [
                        {
                            "departure": {"iataCode": "MIA", "at": "2021-11-10T16:00:00"},
                            "arrival": {"iataCode": "SAL", "at": "2021-11-10T17:45:00"},
                            "carrierCode": "AV",
                            "number": "311",
                            "aircraft": {"code": "320"},
                            "duration": "PT2H45M",
                            "id": "3",
                            "numberOfStops": 0,
                            "blacklistedInEU": False,
                        },
                        {
                            "departure": {"iataCode": "SAL", "at": "2021-11-10T21:50:00"},
                            "arrival": {"iataCode": "SJO", "terminal": "M", "at": "2021-11-10T23:05:00"},
                            "carrierCode": "AV",
                            "number": "627",
                            "aircraft": {"code": "320"},
                            "duration": "PT1H15M",
                            "id": "4",
                            "numberOfStops": 0,
                            "blacklistedInEU": False,
                        },
                    ],
                },
            ],
            "price": {
                "currency": "USD",
                "total": "300.50",
                "base": "88.00",
                "fees": [{"amount": "0.00", "type": "SUPPLIER"}, {"amount": "0.00", "type": "TICKETING"}],
                "grandTotal": "290.50",
                "additionalServices": [{"amount": "70.00", "type": "CHECKED_BAGS"}],
            },
            "pricingOptions": {"fareType": ["PUBLISHED"], "includedCheckedBagsOnly": False},
            "validatingAirlineCodes": ["AV"],
            "travelerPricings": [
                {
                    "travelerId": "1",
                    "fareOption": "STANDARD",
                    "travelerType": "ADULT",
                    "price": {"currency": "USD", "total": "161.55", "base": "50.00"},
                    "fareDetailsBySegment": [
                        {
                            "segmentId": "1",
                            "cabin": "ECONOMY",
                            "fareBasis": "UMOB1BT9",
                            "brandedFare": "S",
                            "class": "U",
                            "includedCheckedBags": {"quantity": 0},
                        },
                        {
                            "segmentId": "3",
                            "cabin": "ECONOMY",
                            "fareBasis": "UMOB1BT9",
                            "class": "U",
                            "includedCheckedBags": {"quantity": 0},
                        },
                        {
                            "segmentId": "4",
                            "cabin": "ECONOMY",
                            "fareBasis": "UMOB1BT9",
                            "brandedFare": "S",
                            "class": "U",
                            "includedCheckedBags": {"quantity": 0},
                        },
                    ],
                },
                {
                    "travelerId": "2",
                    "fareOption": "STANDARD",
                    "travelerType": "CHILD",
                    "price": {"currency": "USD", "total": "148.95", "base": "38.00"},
                    "fareDetailsBySegment": [
                        {
                            "segmentId": "1",
                            "cabin": "ECONOMY",
                            "fareBasis": "UMOB1BT9",
                            "brandedFare": "S",
                            "class": "U",
                        },
                        {"segmentId": "3", "cabin": "ECONOMY", "fareBasis": "UMOB1BT9", "class": "U"},
                        {
                            "segmentId": "4",
                            "cabin": "ECONOMY",
                            "fareBasis": "UMOB1BT9",
                            "brandedFare": "S",
                            "class": "U",
                        },
                    ],
                },
            ],
        },
    ],
    "dictionaries": {
        "locations": {
            "MIA": {"cityCode": "MIA", "countryCode": "US"},
            "SJO": {"cityCode": "SJO", "countryCode": "CR"},
            "SAL": {"cityCode": "SAL", "countryCode": "SV"},
        },
        "aircraft": {"320": "AIRBUS A320"},
        "currencies": {"USD": "US DOLLAR"},
        "carriers": {"AV": "AVIANCA", "CM": "COPA AIRLINES"},
    },
}


def get_carrier_from_code(dictionaries, code):
    carriers = dictionaries.get("carriers", None)
    if carriers and code in carriers:
        return carriers.get(code)


def get_pricing_details(price_data):
    if "grandTotal" in price_data and "currency" in price_data:
        return price_data["grandTotal"] + " " + price_data["currency"]
    else:
        return 0


def get_itineraries(itineraries, dictionaries):
    result = dict()
    result["routes"] = []
    itin = dict()
    itin["routes"] = []
    for itinerary in itineraries:
        segments = itinerary.get("segments", None)
        routes = []

        if segments:
            for segment in segments:
                trip = dict()
                route = dict()
                departure = segment["departure"]
                route["duration"] = segment["duration"]
                arrival = segment["arrival"]
                route["departure"] = departure["iataCode"]
                route["arrival"] = arrival["iataCode"]
                route["timeStampDeparture"] = departure["at"]
                route["timeStampArrival"] = arrival["at"]
                route["airline"] = get_carrier_from_code(dictionaries=dictionaries, code=segment["carrierCode"])
                routes.append(route)
                trip["path"] = routes
                trip["fullDuration"] = itinerary["duration"]

        result["routes"].append(trip)

    return result


def parse_response(response_json):
    result = dict()
    result["offers"] = []
    data = response_json.get("data", None)
    dictionaries = response_json.get("dictionaries", None)
    if not len(data):
        return None
    else:
        for offer in data:
            new_offer = dict()
            price_data = offer.get("price", None)
            itineraries = offer.get("itineraries", None)
            price_details = get_pricing_details(price_data)
            new_offer["price"] = price_details
            itinerary_details = get_itineraries(itineraries, dictionaries)
            new_offer["itinerary"] = itinerary_details
            result["offers"].append(new_offer)

        return result

    return None
