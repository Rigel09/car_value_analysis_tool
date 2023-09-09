from typing import Any, Dict
import requests
from pathlib import Path
import json
import datetime as dtime

URL_FILE = Path("configs/url_config.txt")
DATA_FOLDER = Path("data")


if __name__ == "__main__":
    print(f"This script will go and download data for all urls in {URL_FILE}")

    print("Opening file")
    if not URL_FILE.exists():
        raise FileExistsError(f"Error: {URL_FILE} doesn't exist")

    with URL_FILE.open("r") as config_file:
        for config in config_file:
            if not config:
                continue  # Testing for blank lines

            make, model, year, url = config.strip().split(";")

            print(f"URL:\n\t[{url}]")

            webpage = requests.get(url)

            print("Webpage")
            # print(webpage.content)

            contents = webpage.content.decode()
            # print(contents)
            # print("\n\nHere")
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

            with DATA_FOLDER.joinpath(f"{make}_{model}_{year}_values.csv").open(
                "a"
            ) as data_file:
                rlow = car_value_dict["rangeLow"]
                rhigh = car_value_dict["rangeHigh"]
                value = car_value_dict["configuredValue"]
                base_value = car_value_dict["baseValue"]
                pricing_type = car_value_dict["priceType"]
                date = dtime.datetime.now().strftime("%d-%m-%Y")
                data_file.write(
                    f"{date},{rlow},{rhigh},{value},{base_value},{pricing_type}\n"
                )
