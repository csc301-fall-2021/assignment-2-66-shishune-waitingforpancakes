[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=6228005&assignment_repo_type=AssignmentRepo)

Note: This program was mostly written with a live share so commits may be lacking but
equal coding was done.

Pair Programming
- In our first challenge, Eryka was confused on how to post a csv file. In this scenario, Eryka was driver while Grace was the navigator. Here, Eryka watched Grace code daily_reports_post.py 
- In our second challenge, Grace did not understand why her time series query function was not exporting correctly. Eryka, who had coded exporting to json and csv files, stepped in as the navigator while Grace drove.
- Pair programming was likable because we could bounce ideas off each other. Pair programming was not favourable on a time crunch because our sessions were long and it seems less productive for someone to just watch the other code.
- Pair programming was helpful in understanding eachother's code as well. This enabled understanding the implementation of certain features that the other would then have to do for the other file type. Grace completed the Time Series features and Eryka completed the Daily Report features. Understanding the problems that one person faced allowed for the other to avoid the same mistakes, as well thoroughly understand the logic of the implementation, pair programming forces us to work and solve problems together. 

Design
- We decided to have separate ~~database relations~~ lists and endpoints for data files in the Time Series format and files in the Daily Reports format (there are separate endpoints for querying as well). This reduces coupling in the code because the post and get methods of Time Series and Daily Reports do not query or store information in the same table. This will also make it easier if we want to alter the format of how Time Series or Daily Reports is stored or received in the future. Furthermore, there is high cohesion in our classes, the methods of Time Series only alter the Time Series relation and the methods of Daily Reports only alter the Daily Reports relation. 
- Note: Due to issues in deployment, we changed out database relations into lists. Instead of creating functions that were specific to either the Time Series or Daily Reports lists, we made functions that took in a list and used a key to filter. This allowed for cleaner coding, and reduced the need for code repetition. 

 API Documentation:
 - To send a request with a csv file directly to the API, the TA must...
    - Open the csv file for reading and pass it in as an argument for the data field of posting.
    - To access the Daily Reports endpoint use "https://covid-301-api.herokuapp.com/daily_reports/" as an argument for the url field of posting.
    - To access the Time Series endpoint use "https://covid-301-api.herokuapp.com/time_series/" plus either "confirmed", "deaths", "recovered" (for the different types of time series) as an argument for the url field of posting.
    - Ex. requests.post("https://covid-301-api.herokuapp.com/time_series/confirmed", 
        data=open(local_file_to_send, "r"))
 - We combine adding and updating in "plain idempotent post requests."
 - With regards to querying...
    - The /time_series/cases/ endpoint is used to query the Time Series relation.
    - The /daily_reports/cases/ endpoint is used to query the Daily Reports relation.
    - We allow a user to query multiple columns out of confirmed, deaths, recovered, and active, at specific timespans and countries.
    - For Time Series queries, the user must submit data through requests. 
        They:
        - must enter the type of file they want the results to be put into (either csv or json)
        - may specify True or False for confirmed, deaths, recovered, and active where True indicates that they want to see that column in the result and False indicates they do not. 
        - may specify one province_state, country_region, and combined_key as a string or a list of them. 
        - may specify both the start date and end date with a string formatted 'month/day/year' for looking a specific day or time period. It will not work if only one is given.
        Note that:
        - All dates, even column dates must be specified as a string formatted 'month/day/year'
        - If no or one date is missing, all dates will be considered.
        - If there are no Country/Region or combined keys specified then all countries/regions and provinces/states will be considered. For example, if data = {"filetype":"json"}.
        - We also assume that we include all queries where there is a certain Province/State and all queries where there is a certain Country/Region (ex. {"filetype":"csv", "province_state": "Ontario", "country_region":["Russia", "China"]} will include all queries from Russia, China, and countries with Ontario as a province). If one wants to query Province/State and Country/Region, then they must use a combined key which is a Province/State and Country/Region in this order with no spaces or characters in between. Ex. "OntarioCanada"
        - Names are case sensitive
    - For Daily Report queries, the user must submit data through requests. They:
        - must enter the type of file they want the results to be put into (either csv or json)
            - example: "filetype":"csv"
        - can enter how they would like to filter their results. The results that will be returned will satisfy any one of the filters. For example, if you inputted Canada for country_region and  East Flanders for province_state, results will include all rows that are from Canada and East Flanders.
        Filters can have multiple keys, as long as they are separated by a comma (','). For example, "Canada,Netherlands,France" will output results from Canada, the Netherlands and France. We advise against trailing spaces between commas. All of these filters are optional. If you enter no filters then the results will return the all rows in the database. 
            Filters:
            - "combined_key": For global daily reports, this is the province/state and country/region. For US daily reports, this is the city, the province/state and country/region. For example: "Kerala, India'. Note that each combined key must be put in single quotations. Therefore, for several combined key, it would look like this: "combined_key":"'Kerala, India','Luxembourg, Belgium'"
            - "province_state": This is the province or state of the daily report. 
            - "country_region": This is the country or region of the daily report. 
            - "date": This is the date of the daily report. The format is "yyyy/mm/dd", 
        - can specify what type of data they would like. These keys take in booleans, and where True will include the attribute in the result, and False will not. All of these attributes are optional.
            - "confirmed"
            - "recovered"
            - "deaths"
            - "active" 
        - Example data: 
            {"filetype":"csv",
            "combined_key":"'Kerala, India','Luxembourg, Belgium'", 
            "date":"2021-01-01", 
            "confirmed": True, 
            "active": False}


- Our test cases include...
    - Time Series:
        - POST:
            - Insert a file of each time series type: confirmed, deaths, or recovered
            - Missing column names (no Province/State column, no Country/Region column)
            - Incorrect column names (Long_ instead of Long, improper date, poorly formatted date)
            - Missing cell values (no keys (no country/region, no confirmed/deaths/recovered), no province/state)
        - GET:
            - Query all data for each of deaths, confirmed, recovered, and active
            - Query for one day
            - Query for multiple days
            - Query one combined_key
            - Query many combined_key
            - Query one country/region
            - Query many country/region
            - Query one province/state
            - Query many province/state
            - Query for json and csv format output
            - Query for one missing date time (either start_date or end_date)
            - Query with no countries/regions, provinces/states, combined_keys specified
            - Query with no time period specified
    - Daily Reports
        - POST:
            - Improperly formatted column headers
            - Missing column header 
            - Missing cell values (no keys, no dates, no country/province, no confirmed/deaths/active/recovered)
            - Poorly formatted date, illegal date
            - Properly formatted file
            - Update data for information already posted
        - GET:
            - Query all data for deaths, confirmed, recovered, and active
            - Query all data for one of each; deaths, confirmed, recovered, and active
            - Query all data with no count data
            - Query for one day
            - Query one combined_key
            - Query many combined_key
            - Query one country/region
            - Query many country/region
            - Query one province/state
            - Query many province/state
            - Query for json and csv format output
            - Query with no countries/regions, provinces/states, combined_keys or date specified

    
