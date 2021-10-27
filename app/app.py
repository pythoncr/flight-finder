import logging
from time import perf_counter

import amadeus
import telegram
import utils

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s - %(message)s")
log = utils.config_logger(__name__, logging.DEBUG)


def handle_response(status_code, body, start_time, context):
    passed_time = round((perf_counter() - start_time) * 1000, 2)
    raw_response = {
        "StatusCode": status_code,
        "Body": body,
        "ElapsedMilliseconds": passed_time,
        "AWSRequestId": context.aws_request_id,
    }
    return raw_response


def handler(event, context):
    start_time = perf_counter()
    # TODO: figure it out how EventBridge sends this value
    origin = "SJO"
    destination = "MIA"
    adults = 2
    children = 0
    departure_date = "2021-11-01"
    arrival_date = "2021-11-15"
    res = amadeus.get_offers(
        origin=origin,
        destination=destination,
        adults=adults,
        children=children,
        departure_date=departure_date,
        arrival_date=arrival_date,
        currency="USD",
        qty_offers=1,
    )

    if res:
        # # Check if there is any error
        # for res in result:
        #     if "error" in res:
        #         body_result = {
        #             "error": res["error"]
        #         }
        #         return handle_response(400, body_result, start_time, context)
        body_result = {
            "WasCompleted": True,
            # "EntriesCreated": len(result),
            "FlightEntries": res,
        }
        telegram.send_message(res, origin, destination, adults, children, departure_date, arrival_date)
        return handle_response(200, body_result, start_time, context)
    else:
        body_result = {"error": "no results"}
        handle_response(400, body_result, start_time, context)
