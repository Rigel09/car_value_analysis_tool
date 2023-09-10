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
DESC = "Scrapes used car pricing data from the web\nVersion: {VERSION}"
PROG = "Car Value Analysis Tool"

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=PROG, description=DESC)
    parser.add_argument(
        "--mode",
        action="store_true",
        help="Puts program in test mode. Used for debugging",
    )
    args = parser.parse_args()
    test_mode: bool = args.mode

    logger.info(f"{PROG} Version: {VERSION} is starting up")

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

    logger.debug(f"Config file used is [{URL_FILE}]")

    with URL_FILE.open("r") as config_file:
        for config in config_file:
            if not config:
                continue  # Testing for blank lines

            make, model, year, url = config.strip().split(";")

            logger.debug(f"Make: {make}  model: {model}  year: {year}")
            logger.debug(f"URL:\n\t[{url}]")

            webpage = requests.get(url)

            contents = webpage.content.decode()
            index_front = contents.find('{"rangeLow')
            index_back = contents.find('PriceRange"}') + len('PriceRange"}')

            raw_car_value_data = contents[index_front:index_back]
            logger.debug(f"Raw contents: {raw_car_value_data}")
            car_value_dict: Dict[str, Any] = json.loads(raw_car_value_data)

            data_file_name = f"{make}_{model}_{year}_values.csv"

            if test_mode:
                data_file_name = f"{make}_{model}_{year}_values_testing.csv"

            data_file = DATA_FOLDER.joinpath(data_file_name)

            logger.info(f"Putting site contents in {data_file}")

            with data_file.open("a+") as data_file:
                rlow = car_value_dict["rangeLow"]
                rhigh = car_value_dict["rangeHigh"]
                value = car_value_dict["configuredValue"]
                base_value = car_value_dict["baseValue"]
                pricing_type = car_value_dict["priceType"]
                date = dtime.datetime.now().strftime("%d-%m-%Y")

                line = f"{date},{rlow},{rhigh},{value},{base_value},{pricing_type}\n"
                data_file.write(line)
                logger.debug(f"Wrote line [{line}]")
