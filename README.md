# clinical-trial-monitor
Clinical trial stock price movement indicator

## Description

Currently the clinical trial backtester fetches price data based on the clinical trial start date and then calculates the average price difference as a percent.

Future implementations will fetch clinical trial data once a day and then alert via rss feed or discord to the ticker associated with the clinical trial data. However this is dependent on whether the backtesting data shows a significant positive price differential.

## Usage

1. Setup python virtual environment 

~~~bash
python3 -m venv .venv
~~~

2. Install requirements

~~~bash
pip install -r requirements.txt
~~~

3. Run the program

~~~bash
python3 clinical_trial_backtester.py
~~~

## Process

1. Extract companies from list of publicly listed companies
2. Send query to clinicaltrials API using company name
3. Analyse JSON data for trials that are about to start
4. Companies that are about to commence trials will get sent to discord server for manual analysis
5. ???
6. profit!
