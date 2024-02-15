# Clinical Trial Monitor - Stock Indicator

## URL Parameter

~~~url
https://classic.clinicaltrials.gov/api/query/study_fields?expr=Incannex+Health+Care&fields=BriefTitle%2CBriefSummary%2CStartDate%2CCompletionDate&min_rnk=1&max_rnk=&fmt=json
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
StartDate | Start of trial

## Pharmaceutical Company List

When creating a list of pharmaceutical companies it is necessary to remove: *inc*, *pty ltd*, etc... For example:
- Incannex Healthcare Inc must be renamed to Incannex Healthcare for the search expession to find the trial data