# Imports
import datetime, csv, json, os, io, pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# Configure app, API and database
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
db = SQLAlchemy(app)

encoding = 'utf-8' 

# Database tables
class TimeSeriesModel(db.Model):
    combined_key = db.Column(db.String(100), primary_key=True)  
    province_state = db.Column(db.String(100), nullable=True)
    country_region = db.Column(db.String(100))
    date = db.Column(db.String(100), primary_key=True)
    confirmed = db.Column(db.Integer, nullable=True)
    deaths = db.Column(db.Integer, nullable=True)
    recovered = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"TimeSeries(Province/State = {self.province_state}, \
            Country/Region = {self.country_region}, \
            Date = {self.date}, \
            Confirmed = {self.confirmed}, \
            Deaths = {self.deaths},\
            Recovered = {self.recovered}, \
            Active = {self.active})"

class DailyReportsModel(db.Model):
    combined_key = db.Column(db.String(100), primary_key=True)  
    # note: combined key should be province and country, 
    # so remove admin2[city] for daily reports..?
    province_state = db.Column(db.String(100))
    country_region = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), primary_key=True)
    confirmed = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    recovered = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"DailyReport(province/state = {self.province_state}, \
            country_region = {self.country_region}, \
            date = {self.date}, \
            confirmed = {self.confirmed}, deaths = {self.deaths},\
            recovered = {self.recovered}, active = {self.active})"

# Create the database (should be run once)
# db.create_all() 

class TimeSeries(Resource):
    def post(self, time_series_type):
        # Convert CSV string to file-like object and parse through it using the headers
        csvfile = io.StringIO(request.data.decode("UTF8"), newline=None)
        reader = csv.DictReader(csvfile)

        for row in reader:
            province_state = row["Province/State"]
            country_region = row["Country/Region"]
            for attribute in reader.fieldnames:
                if attribute not in ["Province/State", "Country/Region", "Lat", "Long"]:
                    if (province_state + country_region) is None or attribute is None:
                        abort(400, message="Type of report not specified...")
                    exists = TimeSeriesModel.query.filter_by(combined_key=province_state + country_region, date=attribute).first()
                    if exists is None:           
                        if time_series_type == "confirmed":
                            report = TimeSeriesModel(combined_key = province_state + country_region, \
                                                    province_state = province_state, \
                                                    country_region = country_region, \
                                                    date = attribute,\
                                                    confirmed = row[attribute], \
                                                    active = 0)
                            db.session.add(report)
                        elif time_series_type == "deaths":
                            report = TimeSeriesModel(combined_key = province_state + country_region, \
                                                    province_state = province_state, \
                                                    country_region = country_region, \
                                                    date = attribute,\
                                                    deaths = row[attribute], \
                                                    active = 0)
                            db.session.add(report)
                        elif time_series_type == "recovered":
                            report = TimeSeriesModel(combined_key = province_state + country_region, \
                                                    province_state = province_state, \
                                                    country_region = country_region, \
                                                    date = attribute,\
                                                    recovered = row[attribute], \
                                                    active = 0)
                            db.session.add(report)
                        else:
                            abort(400, message="Incorrect Endpoint...")
                    else:
                        if time_series_type == "confirmed":
                            exists.confirmed = row[attribute]
                        elif time_series_type == "deaths":
                            exists.deaths = row[attribute]
                        elif time_series_type == "recovered":
                            exists.recovered = row[attribute]
                        if exists.confirmed is not None and \
                            exists.deaths is not None and \
                            exists.recovered is not None:
                            exists.active = exists.confirmed - exists.deaths - exists.recovered

        try:
            db.session.commit()
            return 201 # successful
        except:
            abort(400, message="Report already made...")

    # def delete(self):
    #     db.session.query(TimeSeriesModel).delete() 
    #     db.session.commit()

# Automatically parses through the request being sent and ensures it matches the guidelines
time_series_args = reqparse.RequestParser()
time_series_args.add_argument("filetype", type=str, help="Return filetype.", required=True)
# time_series_args.add_argument("query_type", type=str, help="Query Type is Required.", required=True)
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
    try:
        places = []
        if not args['combined_key'] and not args['province_state'] and  \
        not args['country_region']:
            print("You asked for everything")
            places = TimeSeriesModel.query.all()
        
        # print("places",places)
        # Find queries with every combination of country/region and province/state
        if args['country_region'] is not None:
            for country in args['country_region']:
                if args['province_state'] is not None:
                    for province in args['province_state']:
                        places = set(places).union(set(TimeSeriesModel.query.filter_by(country_region=country, province_state=province).all()))
                places = set(places).union(set(TimeSeriesModel.query.filter_by(country_region=country).all()))

        # Find queries with combined_key
        if args['combined_key'] is not None:
            for key in args['combined_key']:
                places = set(places).union(set(TimeSeriesModel.query.filter_by(combined_key=key).all()))
        
        result = places
        # Find queries in specified timespan
        if args['start_date'] is not None and args['end_date'] is not None:
            timespan = []
            start_date = args['start_date'].split('/')
            start_month, start_day, start_year = int(start_date[0]), int(start_date[1]), int("20"+start_date[2])
            end_date = args['end_date'].split('/')
            end_month, end_day, end_year = int(end_date[0]), int(end_date[1]), int("20"+end_date[2])
            if datetime.date(start_year, start_month, start_day) > \
                datetime.date(end_year, end_month, end_day):
                abort(400, message="Bad date times")
            for row in TimeSeriesModel.query.all():
                row_date = row.date.split('/')
                row_month, row_day, row_year = int(row_date[0]), int(row_date[1]), int("20"+row_date[2])
                if datetime.date(start_year, start_month, start_day) <= \
                    datetime.date(row_year, row_month, row_day) and \
                    datetime.date(row_year, row_month, row_day) <= \
                    datetime.date(end_year, end_month, end_day):
                    timespan = set(timespan).union(set([row]))
            result = set(result).intersection(set(timespan))
        
        # Select columns
        final_result = {}
        i = 0
        for model in result:
            model_dict = {"province_state": model.province_state, \
                        "country_region": model.country_region, \
                        "combined_key": model.combined_key, \
                        "date": model.date}

            if args['confirmed']:
                model_dict["confirmed"] = model.confirmed
    
            if  args['deaths']:
                model_dict["deaths"] = model.deaths
                
            if args['recovered']:
                model_dict["recovered"] = model.recovered

            if args['active']:
                model_dict["active"] = model.deaths

            final_result[i] = model_dict
            i += 1

        if args['filetype'] in ['csv', 'json']:
            return export_query(final_result, "time_series_query_results", args['filetype'])
        else:
            abort(400, message="Incorrect File Type")
    except:
        abort(404, message="Could not find any data...") 
    

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

file_path = "./tmp/"
UPLOAD_DIRECTORY = "tmp"
UPLOAD_FOLDER = UPLOAD_DIRECTORY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

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
        if header != "FIPS,Admin2,Province_State,Country_Region,Last_Update,Lat,Long_,\
            Confirmed,Deaths,Recovered,Active,Combined_Key,Incident_Rate,Case_Fatality_Ratio":
            # return 400
            abort(400, message='File is not formatted properly')  
        
        reader = csv.DictReader(csvfile, daily_csv_fieldnames)
        print("reader is reading")
        
        for row in reader:
            input_key = row["Combined_Key"]
            input_date = row["Last_Update"].split()[0].strip()
            input_prov = row["Province_State"]
            input_country = row["Country_Region"]
            input_confirmed = row["Confirmed"]
            input_deaths = row["Deaths"]
            input_recovered = row["Recovered"]
            input_active = row["Active"]

            dailyReport = DailyReportsModel(combined_key = input_key,
                date = input_date,
                province_state = input_prov,
                country_region = input_country,
                confirmed = input_confirmed,
                deaths = input_deaths,
                recovered = input_recovered,
                active = input_active)
            
            # you want to check if this report is in the database according to combined key and date
            # if it is not: 
            if attrNotNull(dailyReport):
                result = DailyReportsModel.query.filter_by(combined_key=dailyReport.combined_key,\
                    date = dailyReport.date).first()
                # print("result:", result)
                if result is None: 
                    try: 
                        # print("We are adding the daily report!")
                        db.session.add(dailyReport)
                        # print(dailyReport)
                    except sqlite3.connector.IntegrityError:
                        return 'This already exists!- Integrity Error'
                    except orm_exc.FlushError:
                        return 'This already exists!- Conflict Error'
                else:
                    # update!
                    print("Update:", result.combined_key, result.date)
                    
                    if result.confirmed != dailyReport.confirmed:
                        result.confirmed = dailyReport.confirmed  
                          
                    if result.deaths != dailyReport.deaths:
                         result.deaths = dailyReport.deaths

                    if result.recovered != dailyReport.recovered:
                        result.recovered = dailyReport.recovered

                    if result.active != dailyReport.active:
                        result.active = dailyReport.active

        db.session.commit()
        return 200 # successful

    def delete(self):
        print("Goodbye Daily Reports!!!")
        db.session.query(DailyReportsModel).delete() 
        db.session.commit()


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
        result = DailyReportsModel.query.all()

    if args['combined_key']:
        for arg_key in args['combined_key'].split(','):
            arg_key = arg_key.lstrip().rstrip()
            result = set(result).union(DailyReportsModel.query.filter_by(combined_key=arg_key).all())

    if args['province_state']:
        for arg_prov in args['province_state'].split(','):
            arg_prov = arg_prov.lstrip().rstrip()
            result = set(result).union(DailyReportsModel.query.filter_by(province_state=arg_prov))

    if args['country_region']:
        for arg_country in args['country_region'].split(','):
            arg_country = arg_country.lstrip().rstrip()
            print(arg_country)
            
            result = set(result).union(DailyReportsModel.query.filter_by(country_region=arg_country).all())
    
    if args['date']:
        for arg_date in args['date'].split(','):
            arg_date = arg_date.lstrip().rstrip()
            result = set(result).union(DailyReportsModel.query.filter_by(date=arg_date).all())
    
    final_result = {}
    i = 0
    for model in result:
        model_dict = {"province_state": model.province_state, \
                                "country_region": model.country_region, \
                                "combined_key": model.combined_key, \
                                "date":model.date}

        if args['confirmed']:
            model_dict["confirmed"] = model.confirmed
 
        if  args['deaths']:
            model_dict["deaths"] = model.deaths
            
        if args['recovered']:
            model_dict["recovered"] = model.recovered

        if args['active']:
            model_dict["active"] = model.deaths

        final_result[i] = model_dict
        i += 1

    file_name = 'daily_report_query_results'

    if args['filetype'] in ['csv', 'json']:
        return export_query(final_result, file_name, args['filetype'])
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

def export_query(result, file_name, filetype):
    data = result
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
    db.create_all()

@app.route('/delete/', methods=['DELETE'])
def delete_db():
    db.drop_all()

# Register resources
api.add_resource(TimeSeries, "/time_series/<string:time_series_type>")
api.add_resource(DailyReports, "/daily_reports/")

if __name__ == "__main__":
    # Only debug in an development environment (not a production environment)
    app.run(debug=True) 