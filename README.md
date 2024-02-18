# clinical-trial-monitor
Clinical trial stock price movement indicator 

## Usage

1. Setup python virtual environment 

~~~bash
python3 -m venv .venv
~~~

2. Install requirements

~~~bash
pip install -r requirements.txt
~~~

3. Set Nasdaq API key in local environmental variables

~~~bash
export NASDAQ_DATA_LINK_API_KEY=<YOUR_API_KEY>
~~~

4. Run the program

~~~bash
python3 extract_names.py
~~~

## Process

1. Extract companies from list of publicly listed companies
2. Send query to clinicaltrials API using company name
3. Analyse JSON data for trials that are about to start
4. Companies that are about to commence trials will get sent to discord server for manual analysis
5. ???
6. profit!
