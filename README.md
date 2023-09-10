# Used Car Analysis Tool

This project is used to analize the price of paticular used cars so you know when to buy

This project has two parts a server and a scraper. The scraper scrapes used car data in
a cron job. This data is then written to a csv file. The server is a client written using
the bokeh framework to view the value of the car over time to get an idea of the trend.

## Cron setup

Add the following line to your cron tab
`* 15 * * * python3 <path>/<to>/car_value_analysis_tool/scraper/results_downloader.py > <path>/<to>/car_value_analysis_tool/logs/last_log.log`
