**Runs on python3 (Developed and tested on python Version 3.8.2).**

**Note:** All commands are run from `/GeminiCodeChallenge`

Script that when given a deviation price percent change returns all pairs with 
greater percent price change over last 24 hours via Gemini api. \
`https://docs.gemini.com/rest-api/#price-feed`

### Challenge:
Writing in a language of your choice (python3 or golang are recommended, but not required).
Implement a series of monitoring alerts using our public API - https://docs.gemini.com/rest-api.

Imagine that your script will be run periodically by a monitoring tool, being called directly,
generating alerts as output that will feed into an alerting mechanism (eg. Slack, PagerDuty, etc).
You do not need to implement this alert mechanism - just log the alert (written to stdout) and its
details per the spec below. Implementing the alert inputs as CLI args is nice to have, but not
required.

For each of the symbols (ie. currency pairs) that Gemini trades you must generate an alert for one (or more) of the following conditions -

**Price Deviation** - Generate an alert if the current price is more than one standard deviation from the 24hr average

**Price Change** - Generate an alert if the current price has changed in the past 24 hours by more than X% from the price at the start of the period

**Volume Deviation** - Generate an alert if the quantity of the most recent trade is more than X% of the total 24hr volume in the symbol

You only need to implement one of the above, but doing all three is fine, given time.
**Delivering a more correct**, but less complete answer is preferable - I'd rather you do a great job implementing one check and show off your skills 
and ability, than struggle to do all three.

**Output**

The alert should be a log line that highlights -

**Log level** - (ie. INFO for regular output. ERROR if the alert condition is met)

**timestamp**

**symbol**

**type of alert** (ie. price deviation, high volume, etc)


### Step1 - Installing reqs:
Install required python libraries \
`pip install -r requirements.txt`

### Step2 - Running the Script:
a) Run the script with a 0.10% price change. 
Will print pairs with price changes greater than 0.10%. \
`python api_alerts.py -d .10`

**Note:** If percent provided is too large and there are no price changes greater than or equal to it
then there will not be any output.

b) Do a dry run of the script \
`python api_alerts.py -d .15 --dry_run True`

c) View more info about the script \
`python3 api_alerts.py --help`

### Step3 - Running tests:
`python -m unittest` \
(Alternatively can use pytest and run that way for fancier testing) \
`python -m pytest` \
Code syntax testing: \
`pylint *`

### Future Features and improvements Roadmap:
1) Add volume deviation monitoring.
2) Add price standard deviation monitoring.
3) More error handling for things like invalid arguments being submitted.
4) Integration with slack, pagerduty for live alerts to relevant teams.
5) Containerize with docker, k8s for easy deployment and avoiding running locally.
6) Add to CI/CD pipeline in jenkins/travis/circle/other tool for continuous deployment of this application.
7) Add linting, and unittests to CI/CD pipeline.
8) Convert output to JSON format and store in AWS S3, then analyze trends with AWS Athena.
9) Address not fixed linting issues

