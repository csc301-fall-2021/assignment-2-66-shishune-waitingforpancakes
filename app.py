# Imports
import datetime, csv, json, os, io, pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from dateutil.parser import ParserError, parse

# Configure app, API and database
app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET'])
def index():
    return 'By Grace and Eryka!'

# ENV = 'dev'

# if ENV == 'dev':
#     app.debug = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///database.db'
# else:
#     app.debug = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hxbliqhycjirgb:7a3f47c7cc57c32707ad2e4f26aaf11c2dac716d2e9a20ebab1f4e13c88efee4@ec2-107-20-127-127.compute-1.amazonaws.com:5432/de9htre82pv157'

# db = SQLAlchemy(app)

encoding = 'utf-8' 

TimeSeriesDB = []
DailyReportsDB = []

# Database tables
class TimeSeriesModel():
    combined_key = ""  
    province_state = ""
    country_region = ""
    date = None
    confirmed = None
    deaths = None
    recovered = None
    active = None

    def __init__(self, combined_key, date) -> None:
        self.combined_key = combined_key 
        self.date = date

    def __repr__(self):
        return f"TimeSeries(Province/State = {self.province_state}, \
            Country/Region = {self.country_region}, \
            Date = {self.date}, \
            Confirmed = {self.confirmed}, \
            Deaths = {self.deaths},\
            Recovered = {self.recovered}, \
            Active = {self.active})"

class DailyReportsModel():
    combined_key = str  
    province_state = str
    country_region = str
    date = None
    confirmed = int
    deaths = int
    recovered = int
    active = int

    def __init__(self, combined_key) -> None:
        self.combined_key = combined_key  


    def __repr__(self):
        return f"DailyReport(province/state = {self.province_state}, \
            country_region = {self.country_region}, \
            date = {self.date}, \
            confirmed = {self.confirmed}, deaths = {self.deaths},\
            recovered = {self.recovered}, active = {self.active})"

def find_key_date(key, date, db):
    i = 0
    for report in db:
        if report.combined_key == key and report.date == date:
            return report, i
        i += 1
    return None

def filter_key(key, db):
    query = []
    for report in db:
        if report.combined_key == key:
            query.add(report)
    return query

def filter_date(date, db):
    query = []
    for report in db:
        if report.date == date:
            query.add(report)
    return query

def filter_country(country, db):
    query = []
    for report in db:
        if report.country_region == country:
            query.add(report)
    return query


def filter_province(province, db):
    query = []
    for report in db:
        if report.province_state == province:
            query.add(report)
    return query

class TimeSeries(Resource):
    def post(self, time_series_type):
        # Convert CSV string to file-like object and parse through it using the headers
        csvfile = io.StringIO(request.data.decode("UTF8"), newline=None)
        reader = csv.DictReader(csvfile)
        
        # Put each row from the given csv file into our relation
        for row in reader:

            # Read the COVID report place
            try:
                province_state = row["Province/State"]
                country_region = row["Country/Region"]
            except:
                abort(400, message="File does not have named columns Province/State or Country/Region")
            
            # Read the COVID report dates
            for attribute in reader.fieldnames:
                if attribute not in ["Province/State", "Country/Region", "Lat", "Long"]:
                    
                    # Check required key values
                    if country_region is None:
                        abort(400, message="File does not have required field Country/Region")
                    try:
                        attribute_date = attribute.split('/')
                        attribute_month, attribute_day, attribute_year = int(attribute_date[0]), int(attribute_date[1]), int("20"+attribute_date[2])
                        datetime.date(attribute_year, attribute_month, attribute_day)
                    except:
                        abort(400, message="File includes an ill-named column or an improper date")

                    # Check whether we are creating a new resource or updating an existing resource
                    exists = find_key_date(province_state + country_region, attribute, TimeSeriesDB) 

                    if exists is None:     
                        report = TimeSeriesModel(province_state + country_region, attribute)
                        report.province_state = province_state
                        report.country_region = country_region
                        if time_series_type == "confirmed":
                            report.confirmed = row[attribute]
                            report.active = 0
                            TimeSeriesDB.append(report)
                        elif time_series_type == "deaths":
                            report.deaths = row[attribute]
                            report.active = 0
                            TimeSeriesDB.append(report)
                        elif time_series_type == "recovered":
                            report.recovered = row[attribute]
                            report.active = 0
                            TimeSeriesDB.append(report)
                        else:
                            abort(400, message="Incorrect Specified Endpoint...")
                    else:
                        report = exists[0]
                        index = exists[1]
                        if time_series_type == "confirmed":
                            report.confirmed = row[attribute]
                            TimeSeriesDB[index] = report
                        elif time_series_type == "deaths":
                            report.deaths = row[attribute]
                            TimeSeriesDB[index] = report
                        elif time_series_type == "recovered":
                            report.recovered = row[attribute]
                            TimeSeriesDB[index] = report
                        if report.confirmed is not None and \
                            report.deaths is not None and \
                            report.recovered is not None:
                            report.active = report.confirmed - report.deaths - report.recovered
                            TimeSeriesDB[index] = report

        return 201
    # except:
    #     abort(500, message="Could not add csv file content...")

# Automatically parses through the request being sent and ensures it matches the guidelines
time_series_args = reqparse.RequestParser()
time_series_args.add_argument("filetype", type=str, help="Return filetype.", required=True)
time_series_args.add_argument("province_state", type=str, action="append", help="Province/State of COVID Reports.")
time_series_args.add_argument("country_region", type=str, action="append", help="Country/Region of COVID Reports.")
time_series_args.add_argument("combined_key", type=str, action="append", help="Country/Region of COVID Reports.")
time_series_args.add_argument("start_date", type=str, help="Date of COVID Report.")
time_series_args.add_argument("end_date", type=str, help="Date of COVID Report.")
time_series_args.add_argument("confirmed", type=bool, help="Confirmed COVID Cases.")
time_series_args.add_argument("deaths", type=bool, help="Deaths from COVID.")
time_series_args.add_argument("active", type=bool, help="Active COVID Cases.")
time_series_args.add_argument("recovered", type=bool, help="Recovered from COVID.")

@app.route('/time_series/cases/', methods=['GET'])
def time_series_query():
    # Load user request arguments 
    args = time_series_args.parse_args()

    places = []
    if not args['combined_key'] and not args['province_state'] and  \
        not args['country_region']:
        try:
            places = TimeSeriesDB
        except:
            abort(404, message="No data found...")
        
    # Find queries with every combination of country/region and province/state
    # TODO I HAVE UNNESTED YOUR CODE!!! @GRACE
    if args['country_region'] is not None:
        for country in args['country_region']:
            places.extend(filter_country(country, TimeSeriesDB))

    if args['province_state'] is not None:
        for province in args['province_state']:
            places.extend(filter_province(province, TimeSeriesDB))

    # Find queries with combined_key
    if args['combined_key'] is not None:
        for key in args['combined_key']:
            places.extend(filter_key(key, TimeSeriesDB))
        
    result = places

    # Find queries in specified timespan
    if args['start_date'] is not None and args['end_date'] is not None:
        timespan = []
        try:
            start_string = args['start_date'].split('/')
            start_month, start_day, start_year = int(start_string[0]), int(start_string[1]), int("20"+start_string[2])
            end_string = args['end_date'].split('/')
            end_month, end_day, end_year = int(end_string[0]), int(end_string[1]), int("20"+end_string[2])
            start_date = datetime.date(start_year, start_month, start_day)
            end_date = datetime.date(end_year, end_month, end_day)
        except:
            abort(400, message="Dates formatted incorrectly or improper date")
        if start_date > end_date:
            abort(403, message="Cannot have a negative time span")
        for row in TimeSeriesDB:
            row_date = row.date.split('/')
            row_month, row_day, row_year = int(row_date[0]), int(row_date[1]), int("20"+row_date[2])
            if start_date <= datetime.date(row_year, row_month, row_day) and \
                datetime.date(row_year, row_month, row_day) <= end_date:
                timespan = set(timespan).union(set([row]))
        result = set(result).intersection(set(timespan))
    
    result = set(result)
    # Select specified columns
    select_calls = {}
    
    if args['confirmed']:
        select_calls['confirmed'] =  args['confirmed']
    if args['deaths']:
        select_calls['deaths'] =  args['deaths']
    if args['active']:
        select_calls['active'] =  args['active']
    if args['recovered']:
        select_calls['recovered'] =  args['recovered']

    # Export query results
    if args['filetype'] in ['csv', 'json']:
        try:
            return export_query(result, select_calls, "time_series_query_results", args['filetype']), 200
        except:
            abort(500, message="Could not export query results...")
    else:
        abort(400, message="Incorrect Specified File Type...")  

# Defines how an object should be serialized
daily_resource_fields = {
    'combined_key': fields.String,
    'province_state': fields.String, 
    'country_region': fields.String,
    'date': fields.String,
    'confirmed': fields.Integer,
    'deaths': fields.Integer,
    'recovered': fields.Integer,
    'active': fields.Integer 
}

daily_csv_fieldnames = ("FIPS", "Admin2",  	"Province_State", "Country_Region", "Last_Update",\
 	"Lat", "Long_", "Confirmed", "Deaths", "Recovered", "Active", "Combined_Key", \
    "Incidence_Rate", "Case-Fatality_Ratio")

# app.config["CLIENT_CSV"] = "E:/AudiotoText/Flask_File_Downloads/filedownload/files/csv"

class DailyReports(Resource):

    @marshal_with(daily_resource_fields)
    def post(self):        
        print("received! thank you :)")
        csvfile = io.StringIO(request.data.decode("UTF8"), newline=None)
        # print(csvfile)
        print("decoding!")
        # skip header
        header = next(csvfile)
        if header != "FIPS,Admin2,Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,Combined_Key,Incident_Rate,Case_Fatality_Ratio\n":
            # return 400
            abort(400, message='File header is not formatted properly')  
        
        reader = csv.DictReader(csvfile, daily_csv_fieldnames)
        print("reader is reading")
        
        for row in reader:
            input_key = row["Combined_Key"]
            input_date = row["Last_Update"].split()[0].strip()
            formatted_date = parse(input_date).date()
            input_prov = row["Province_State"]
            input_country = row["Country_Region"]
            input_confirmed = row["Confirmed"]
            input_deaths = row["Deaths"]
            input_recovered = row["Recovered"]
            input_active = row["Active"]

            dailyReport = DailyReportsModel(combined_key = input_key)
            dailyReport.date = formatted_date
            dailyReport.province_state = input_prov
            dailyReport.country_region = input_country
            dailyReport.confirmed = input_confirmed
            dailyReport.deaths = input_deaths
            dailyReport.recovered = input_recovered
            dailyReport.active = input_active
            
            # you want to check if this report is in the database according to combined key and date
            # if it is not: 
            if attrNotNull(dailyReport):
                result = find_key_date(dailyReport.combined_key, dailyReport.date, DailyReportsDB)
                
                # print("result:", result)
                if result is None: 
                    DailyReportsDB.append(dailyReport)

                else:
                    # update!
                    result_report = result[0]
                    index = result[1]
                    print("Update:", result_report.combined_key, result_report.date)
                    
                    if result_report.confirmed != dailyReport.confirmed:
                        result_report.confirmed = dailyReport.confirmed  
                          
                    if result_report.deaths != dailyReport.deaths:
                         result_report.deaths = dailyReport.deaths

                    if result_report.recovered != dailyReport.recovered:
                        result_report.recovered = dailyReport.recovered

                    if result_report.active != dailyReport.active:
                        result_report.active = dailyReport.active

                    DailyReportsDB[index] = result_report

        return 200 # successful

    def delete(self):
        print("Goodbye Daily Reports!!!")
        DailyReportsDB = []


dailyreport_get_args = reqparse.RequestParser()
dailyreport_get_args.add_argument("filetype", type=str, help="Return filetype.", required=True)
dailyreport_get_args.add_argument("combined_key", type=str, help="City, Province/State and Country/Region of COVID Report.")
dailyreport_get_args.add_argument("province_state", type=str, help="Province/State of COVID Report.")
dailyreport_get_args.add_argument("country_region", type=str, help="Country/Region of COVID Report.")
dailyreport_get_args.add_argument("date", type=str, help="Date of COVID Report.")
dailyreport_get_args.add_argument("confirmed", type=bool, help="Confirmed COVID Cases.")
dailyreport_get_args.add_argument("deaths", type=bool, help="Deaths from COVID.")
dailyreport_get_args.add_argument("active", type=bool, help="Active COVID Cases.")
dailyreport_get_args.add_argument("recovered", type=bool, help="Recovered from COVID.")


@app.route('/daily_reports/cases/', methods=['GET'])
def query_daily_reports():

    args = dailyreport_get_args.parse_args() 
    
    result = []

    if not args['combined_key'] and not args['province_state'] and  \
        not args['country_region'] and not args['date']:
        print("You asked for everything")
        result = DailyReportsDB.copy()

    if args['combined_key']:
        for arg_key in args['combined_key'].split("'"):
            arg_key = arg_key.replace("\"", "").lstrip().rstrip()
            result.extend(filter_key(arg_key, DailyReportsDB))

    if args['province_state']:
        for arg_prov in args['province_state'].split(','):
            arg_prov = arg_prov.lstrip().rstrip()
            result.extend(filter_province(arg_prov, DailyReportsDB))

    if args['country_region']:
        for arg_country in args['country_region'].split(','):
            arg_country = arg_country.lstrip().rstrip()            
            result.extend(filter_country(arg_country, DailyReportsDB))
    
    if args['date']:
        for arg_date in args['date'].split(','):
            try:
                input_date = parse(arg_date).date()
            except ParserError: 
                abort(400,  message='Date invalid') # TODO 
            result.extend(filter_date(input_date, DailyReportsDB))
        

    select_calls = {}
    if args['confirmed']:
        select_calls['confirmed'] =  args['confirmed']
    if args['deaths']:
        select_calls['deaths'] =  args['deaths']
    if args['active']:
        select_calls['active'] =  args['active']
    if args['recovered']:
        select_calls['recovered'] =  args['recovered']

    file_name = 'daily_report_query_results'

    if args['filetype'] in ['csv', 'json']:
        return export_query(result, select_calls, file_name, args['filetype'])
    else:
        abort(400, message="Incorrect File Type")

def attrNotNull(dailyReport):
    if dailyReport.combined_key is None or \
        dailyReport.date is None or \
        dailyReport.country_region is None or \
        dailyReport.confirmed is None or \
        dailyReport.deaths is None or \
        dailyReport.recovered is None or \
        dailyReport.active is None:
        return False
    return True

file_path = "./tmp/"
UPLOAD_DIRECTORY = "tmp"
UPLOAD_FOLDER = UPLOAD_DIRECTORY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def export_query(result, select_calls, file_name, filetype):
    final_result = {}
    i = 0
    for model in result:
        model_dict = {"province_state": model.province_state, \
                    "country_region": model.country_region, \
                    "combined_key": model.combined_key, \
                    "date":model.date}

        if 'confirmed' in select_calls:
            model_dict["confirmed"] = model.confirmed
 
        if  'deaths' in select_calls:
            model_dict["deaths"] = model.deaths
            
        if 'recovered' in select_calls:
            model_dict["recovered"] = model.recovered

        if 'active' in select_calls:
            model_dict["active"] = model.deaths

        final_result[i] = model_dict
        i += 1
    
    data = final_result

    print("exporting")
    if filetype == "json":
        file_type = '.json'
        with open(file_path + file_name + file_type, 'w') as jsonfile:
            json.dump(data, jsonfile)
        # And then we write a final newline to the end of the file 
        # (this is just a best practice)
            jsonfile.write('\n')
        try:
            return send_from_directory(app.config["UPLOAD_FOLDER"], filename=file_name + file_type, as_attachment=True)
        except FileNotFoundError:
            abort(404, message="The file was not created")

    elif filetype == "csv":
        file_type = '.csv'
        dataframe = pd.DataFrame.from_dict(data, orient='index')
        # print(dataframe)
        csvdata = pd.DataFrame.to_csv(dataframe)
        # print(csvdata)
        
        # csvfile.save(file_location)
        with open(file_path + file_name + file_type, 'w') as csvfile:
            csvfile.write(csvdata)

        try:
            return send_from_directory(app.config["UPLOAD_FOLDER"], filename=file_name + file_type, as_attachment=True)

        except FileNotFoundError:
            abort(404, message="The file was not created")
    else:
        abort(404, message="File type not available. Must be csv or json")  

@app.route('/create/', methods=['POST'])
def create_db():
    TimeSeriesDB = []
    DailyReportsDB = []

@app.route('/delete/', methods=['DELETE'])
def delete_db():
    TimeSeriesDB = []
    DailyReportsDB = []

# Register resources
api.add_resource(TimeSeries, "/time_series/<string:time_series_type>")
api.add_resource(DailyReports, "/daily_reports/")

if __name__ == "__main__":
    # Only debug in an development environment (not a production environment)
    app.run()
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080) 