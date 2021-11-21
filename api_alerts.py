#! /usr/bin/env python3
'''
Given a price change percentage returns all pairs with
greater percent price changes over last 24 hours found via Gemini api

Sample Run:
python3 api_alerts.py -d .10

Sample Dry Run:
python3 api_alerts.py -d .15 --dry_run True
'''

# pylint: disable=W1203
import logging

import click
import requests

# Note: Some of the "percentChange24" numbers displayed by API
# seem wrong to me (too low) especially for USD pairs.

@click.command()
@click.option('-d', '--deviation', required=True, type=click.FLOAT,
              help='Minimum percent price change of pairs over 24hrs to display.')
@click.option('-r', '--dry_run', default=False, help='Run script without making requests')
@click.option('-l', '--log_level', type=click.STRING, default='INFO',
              help='Sets the log level of the script. Defaults to INFO.')
def price_change_alert(deviation, log_level, dry_run):
    '''
    Makes an API request to gemini that gets all price pairs and percent change in 24hrs.
    Then sends alert to STDOUT if change is more than passed deviation.

    :param deviation: {float object}: Min percent change in price for pairs over 24hours to show.\n
    :param log_level: {bool object}: Min level of logs you want visible in STDOUT. Can ignore.\n
    :param dry_run: {bool object}: True/False. Whether you want to call the API or trigger dry run.
    :return:
    '''
    # Docs https://docs.gemini.com/rest-api/#price-feed
    # Can alternatively use sandbox api if preferred.

    # Added log_level parameter for visibility of INFO level logs in STDOUT
    logging.basicConfig(format='%(asctime)s - AlertingTool - %(levelname)s - %(message)s',
                        level=str(log_level.upper()))

    # Converted to lower string for error handling in case of typos.
    if str(dry_run).lower() == "false":
        base_url = 'https://api.gemini.com/v1'
        response = requests.get(base_url + '/pricefeed')
        pair_prices = response.json()
        for pair_price in pair_prices:
            log_price_alert(pair_price, deviation)
    else:
        logging.info('Dry Run only')
        logging.info(f'Would have called API and found price fluctations above: {deviation}%.')

def log_price_alert(pair_price, deviation):
    '''
    Verifies if pair price change over 24hrs is greater than passed deviation
    percent and sends an alert to STDOUT if it is. Differentiates
    between price increase and price decrease in the alert

    :param pair_price: {dictionary object}: Contains pair symbol, current price,
    and percent change in price over 24hours
    :param deviation: {float object}: Min percent change in price for pairs over 24hours to display.
    :return:
    '''
    # Can use abs() if we don't care whether price increased or decreased for alert.
    price_change = float(pair_price['percentChange24h'])
    symbol = pair_price['pair']
    current_price = pair_price['price']
    if price_change >= abs(deviation):
        logging.error(f'PRICE CHANGE: Price for pair {symbol} has increased by {price_change}%.'
                      f' Current price is now {current_price}')
    elif price_change <= -abs(deviation):
        logging.error(f'PRICE CHANGE: Price for pair {symbol} has decreased by {price_change}%.'
                      f' Current price is now {current_price}')
    else:
        # Log something else? INFO level log output can go here.
        pass

if __name__ == '__main__':
    price_change_alert() # pylint: disable=E1120
