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
    records = event["payload"]
    res = amadeus.get_offers(
        origin="SJO",
        destination="MIA",
        adults=2,
        children=0,
        departure_date="2021-11-01",
        arrival_date="2021-11-15",
        currency="USD",
        qty_offers=10,
    )
    try:
        result = None

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
            telegram.send_message(body_result)
            return handle_response(200, body_result, start_time, context)

    except Exception as error:
        body_result = {"error": error}
        handle_response(400, body_result, start_time, context)
