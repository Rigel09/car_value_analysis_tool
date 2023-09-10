# Local Imports
#########################
from project_specs import VERSION, TOP_LEVEL_PROJECT_DIR

import argparse
import datetime as dtime
import json
import logging
import requests
from typing import Any, Dict

URL_FILE = TOP_LEVEL_PROJECT_DIR.joinpath("configs/url_config.txt")
DATA_FOLDER = TOP_LEVEL_PROJECT_DIR.joinpath("data")
LOG_FOLDER = TOP_LEVEL_PROJECT_DIR.joinpath("logs")
DESC = "Scrapes used car pricing data from the web"
PROG = "Car Value Analysis Tool"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=PROG, description=DESC)
    parser.add_argument(
        "--mode",
        action="store_true",
        help="Puts program in test mode. Used for debugging",
    )
    args = parser.parse_args()
    test_mode: bool = args.mode

    logger.info(f"{PROG} is starting up")

    if test_mode:
        logger.info("Test mode is enabled")

    if not DATA_FOLDER.exists():
        logger.info(f"Creating data folder [{DATA_FOLDER}]")
        DATA_FOLDER.mkdir(parents=True)

    if not LOG_FOLDER.exists():
        logger.info(f"Creating log folder [{LOG_FOLDER}]")
        LOG_FOLDER.mkdir(parents=True)

    if not URL_FILE.exists():
        raise FileExistsError(f"Error: {URL_FILE} doesn't exist")

    with URL_FILE.open("r") as config_file:
        for config in config_file:
            if not config:
                continue  # Testing for blank lines

            make, model, year, url = config.strip().split(";")

            print(f"URL:\n\t[{url}]")

            webpage = requests.get(url)

            contents = webpage.content.decode()
            index_front = contents.find('{"rangeLow')
            index_back = contents.find('PriceRange"}') + len('PriceRange"}')

            raw_car_value_data = contents[index_front:index_back]
            car_value_dict: Dict[str, Any] = json.loads(raw_car_value_data)

            print("This is the data I got:")
            print(f"\tRangelow: {car_value_dict['rangeLow']}")
            print(f"\tRangeHigh: {car_value_dict['rangeHigh']}")
            print(f"\tValue: {car_value_dict['configuredValue']}")
            print(f"\tBaseValue: {car_value_dict['baseValue']}")
            print(f"\tPriceType: {car_value_dict['priceType']}")

            data_file_name = f"{make}_{model}_{year}_values.csv"

            if test_mode:
                data_file_name = f"{make}_{model}_{year}_values_testing.csv"

            with DATA_FOLDER.joinpath(data_file_name).open("a+") as data_file:
                rlow = car_value_dict["rangeLow"]
                rhigh = car_value_dict["rangeHigh"]
                value = car_value_dict["configuredValue"]
                base_value = car_value_dict["baseValue"]
                pricing_type = car_value_dict["priceType"]
                date = dtime.datetime.now().strftime("%d-%m-%Y")
                data_file.write(
                    f"{date},{rlow},{rhigh},{value},{base_value},{pricing_type}\n"
                )
