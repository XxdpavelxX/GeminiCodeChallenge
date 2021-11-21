#! /usr/bin/env python3

'''
Unit tests for api_alerts.py
Can be run via:

python -m unittest
or
python -m pytest

'''
from io import StringIO
import logging
import unittest
from unittest import mock

from click.testing import CliRunner

from api_alerts import price_change_alert, log_price_alert

mock_gemini_response_increase = {'percentChange24h': '0.15','pair':'eth/usd','price':'4000 usd'}
mock_gemini_response_decrease = {'percentChange24h': '-0.15','pair':'eth/usd','price':'4000 usd'}

def mocked_requests_get(url): # pylint: disable=W0613
    '''
    Mock function for get requests
    :param url: {string} arbitrary string.
    :return: arbitrary mocked response dictionary object
    '''
    class MockResponse: # pylint: disable=R0903
        '''
        Mock class for get request testing
        '''
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            '''
            Returns a mocked get response request.
            '''
            return self.json_data
    return MockResponse({"key1": "value1", "key2": "value2", "key3": "value3"}, 200)

class TestAPIAlerts(unittest.TestCase):
    '''
    Class for setting up and running unittests for api_alerts.py script
    '''
    def setUp(self):
        # Need this because CLIRunner capturea and stores STDOUT between tests and causes failure.
        logging.getLogger("").handlers = []

    def test_price_change_alert_dry_run(self):
        '''
        Testing dry run capability for price_change_alert function in api_alerts.py
        '''
        runner = CliRunner()
        result = runner.invoke(price_change_alert, '-d .10 -r True'.split(), input='2')
        assert result.exit_code == 0
        self.assertIn(' - AlertingTool - INFO - Dry Run only\n', result.output)
        self.assertIn(' - AlertingTool - INFO - Would have called API and found'
                      ' price fluctations above: 0.1%.\n', result.output)

    @mock.patch('api_alerts.log_price_alert')
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_price_change_alert(self, mock_get, mock_log_price_alert): # pylint: disable=W0613,R0201
        '''
        Testing for price_change_alert function in api_alerts.py using mocked objects
        '''
        mock_log_price_alert.return_value = "pass"
        runner = CliRunner()
        runner.invoke(price_change_alert, '-d .10'.split(), input='1')
        assert mock_log_price_alert.called is True
        assert mock_log_price_alert.call_count == 3

    def test_log_price_alert_increase(self):
        '''
        Testing for log_price_alert function in api_alerts.py when there is
        a price increase percent higher than passed argument.
        '''
        log_stream = StringIO()
        logging.basicConfig(stream=log_stream, level=logging.ERROR)
        log_price_alert(mock_gemini_response_increase, 0.1)
        output = log_stream.getvalue()
        self.assertEqual('ERROR:root:PRICE CHANGE: Price for pair eth/usd has increased '
                         'by 0.15%. Current price is now 4000 usd\n', output)

    def test_log_price_alert_decrease(self):
        '''
        Testing for log_price_alert function in api_alerts.py when there is
        a price decrease percent higher than passed argument.
        '''
        log_stream = StringIO()
        logging.basicConfig(stream=log_stream, level=logging.ERROR)
        log_price_alert(mock_gemini_response_decrease, 0.1)
        output = log_stream.getvalue()
        self.assertEqual('ERROR:root:PRICE CHANGE: Price for pair eth/usd has decreased'
                         ' by -0.15%. Current price is now 4000 usd\n', output)

    def test_log_price_alert_none(self):
        '''
        Testing for log_price_alert function in api_alerts.py when there is
         o price increase or decrease percent higher than passed argument.
        '''
        log_stream = StringIO()
        logging.basicConfig(stream=log_stream, level=logging.ERROR)
        log_price_alert(mock_gemini_response_decrease, 0.2)
        output = log_stream.getvalue()
        self.assertEqual('', output)

if __name__ == '__main__':
    unittest.main()
