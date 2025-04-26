# ATC Scrapy Spider
A simple Scrapy spider for the WHO ATC Index.

## Description
This project uses Scrapy, a Python scraping framework, to scrape all ATC from the WHO ATC Index.

The output is a `.csv` file in the `output` folder.

Enabling proxies, `AUTOTHROTTLE_ENABLED`, `USER_AGENT` and/or `BOT_NAME` among other changes in `settings.py` may help to avoid being blocked, but note that the ATC codes are also available online as `.csv`, `.json` or `.xlsx`.

## Getting Started
* Clone this repository
* `cd` into the cloned repository
* Setup a virtual environment with `venv` or `conda` and activate it
* Run `pip install -r requirements.txt`
* Run one of the following commands:
    * Run `scrapy crawl atc`
        * Will get all ATC codes
        * No `tqdm` progress bar
    * Run `scrapy crawl atc -a progress_logging=true`
        * Will get all ATC codes
        * Will shoow a `tqdm` progress bar
    * Run `scrapy crawl atc -a progress_logging=true -a level=1`
        * Will get all ATC codes up to the specified level, as shown in this example:
            * 1: A01
            * 2: A01A
            * 3: A01AA
            * 4: A01AA01
        * Will shoow a `tqdm` progress bar

## License
This project is licensed under the MIT License - see the LICENSE.md file for details