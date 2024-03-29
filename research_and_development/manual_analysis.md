# Clinical Trial Monitor - Stock Indicator

## URL Parameter

~~~url
https://classic.clinicaltrials.gov/api/query/study_fields?expr=Incannex+Health+Care&fields=BriefTitle%2CBriefSummary%2CStartDate%2CCompletionDate&min_rnk=1&max_rnk=1000&fmt=json
~~~

### Output Format

There are three formats for the output:
- JSON
- XML
- CSV

### Search Expression

The search expression is the search term used to find studies. It can be the name of the study, **company name**, trial ID, etc. In this program we will use the company name as the search expression. For example:

- Search Expression: Incannex Health Care
  - Not case sensitive

### Fields Used for Essential Information

Fields | Description
------ | -----------
BriefTitle | Short description of the study 
BriefSummary | Short description of the study and tests to be performed
CompletionDate | Estimated time of completion
StudyFirstPostDate | Initial posting to clinicaltrials.gov
StartDate | Start of trial
CompletionDate | End of trial
OverAllStatus | [Active, Recruiting, Not Yet Recruiting, Completed]
NStudiesFound | If this value is `0` then there are no clinical trials available
Rank | Each study gets their own rank

## Pharmaceutical Company List

When creating a list of pharmaceutical companies it is necessary to remove: *inc*, *pty ltd*, etc... For example:
- Incannex Healthcare Inc must be renamed to Incannex Healthcare for the search expession to find the trial data

## Resources

### Stock List Web Applications

- [NASDAQ List (csv)](https://topforeignstocks.com/wp-content/uploads/2024/01/Complete-List-of-Biotech-Stocks-Listed-on-NASDAQ-Jan-1-24.csv)

### Clinical Trial Data

- [clinicaltrials API information](https://classic.clinicaltrials.gov/api/gui)
- [clinicaltrials API field list](https://classic.clinicaltrials.gov/api/info/study_fields_list)
- [clinicaltrials API query](https://classic.clinicaltrials.gov/api/gui/demo/simple_study_fields)

### Stock API

- [yfinance](https://github.com/ranaroussi/yfinance)
- [yfinance PyPI](https://pypi.org/project/yfinance/)

## Start Dates

Date Field | Description
---------- | -----------
StartDate | When the study will commence
EndDate | When the study will conclude
StudyFirstPostDate | The estimated date that the trial was made available
StudyFirstSubmitDate | When the study was submitted
StudyFirstSubmitQCDate | When the study passed the Quality Control review
ResultsFirstPostDate | When the results were posted
ResultsFirstSubmitDate | When the results were submitted
ResultsFirstSubmitQCDate | When the results where first verified

## TODO

1. Only take trials from the same year to reduce chance of trends affecting the data
2. Investigate negative data, what year was it?

## Results

Start Date Field | Percentage Difference
---------------- | ---------------------
StudyFirstPostDate | -0.03508451847407963
StudyFirstSubmitDate | 
ResultsFirstPostDate | -0.0262478534630795351