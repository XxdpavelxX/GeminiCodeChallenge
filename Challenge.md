### Challenge Prompt:
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