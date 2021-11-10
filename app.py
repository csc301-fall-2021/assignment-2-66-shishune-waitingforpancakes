# Imports
import csv,json, os, io, pandas as pd
from flask import Flask, jsonify, request, send_from_directory, Response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

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

# Automatically parses through the request being sent and ensures it matches the guidelines
# timeseries_args = reqparse.RequestParser()
# timeseries_args.add_argument("type", type=str, help="Type of Statistic is Required.", required=True)
# timeseries_args.add_argument("country_region", type=str, help="Country/Region of COVID Report.", required=True)
# timeseries_args.add_argument("date", type=str, help="Date of COVID Report.", required=True)
# timeseries_args.add_argument("time_series_type", type=str, help="Confirmed COVID Cases.", required=True)
# timeseries_args.add_argument("time_series_type_value", type=int, help="Deaths from COVID.", required=True)

# Defines how an object should be serialized
resource_fields = {
    'combined_key': fields.String,
    'province_state': fields.String, 
    'country_region': fields.String,
    'date': fields.String,
    'confirmed': fields.Integer,
    'deaths': fields.Integer,
    'recovered': fields.Integer,
    'active': fields.Integer 
}

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
                                                    confirmed = row[attribute])
                            db.session.add(report)
                        elif time_series_type == "deaths":
                            report = TimeSeriesModel(combined_key = province_state + country_region, \
                                                    province_state = province_state, \
                                                    country_region = country_region, \
                                                    date = attribute,\
                                                    deaths = row[attribute])
                            db.session.add(report)
                        elif time_series_type == "recovered":
                            report = TimeSeriesModel(combined_key = province_state + country_region, \
                                                    province_state = province_state, \
                                                    country_region = country_region, \
                                                    date = attribute,\
                                                    recovered = row[attribute])
                            db.session.add(report)
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
            return 200 # successful
        except:
            abort(400, message="Report already made...")

@app.route('/time_series/deaths/<int:id>', methods=['GET'])
def time_series_query_deaths(id):
    try:
        result = TimeSeriesModel.query.all()
        return result
    except:
        abort(404, message="Could not find any data...")

@app.route('/time_series/confirmed/<int:id>', methods=['GET'])
def time_series_query_confirmed(id):
    try:
        result = TimeSeriesModel.query.all()
        return result
    except:
        abort(404, message="Could not find any data...")

@app.route('/time_series/active/<int:id>', methods=['GET'])
def time_series_query_active(id):
    try:
        result = TimeSeriesModel.query.all()
        return result
    except:
        abort(404, message="Could not find any data...")

@app.route('/time_series/recovered/<int:id>', methods=['GET'])
def time_series_query_recovered(id):
    try:
        result = TimeSeriesModel.query.all()
        return result
    except:
        abort(404, message="Could not find any data...")

@app.route('/time_series/period/<int:id>', methods=['GET'])
def time_series_query_period(id):
    try:
        result = TimeSeriesModel.query.all()
        return result
    except:
        abort(404, message="Could not find any data...")

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

file_path = './tmp/'
UPLOAD_DIRECTORY = "tmp"

UPLOAD_FOLDER = file_path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# app.config["CLIENT_CSV"] = "E:/AudiotoText/Flask_File_Downloads/filedownload/files/csv"


class DailyReports(Resource):
    # This decorator is used for the return
    # When we return, take these values and serialize with these fields
    # @marshal_with(daily_resource_fields)
    def get(self):

    # note: combined key should be province and country, 
    # so remove admin2[city] for daily reports..?
    # province_state = db.Column(db.String(100), nullable=False)
    # country_region = db.Column(db.String(100), nullable=False)
    # date = db.Column(db.String(100), primary_key=True)
    # confirmed = db.Column(db.Integer, nullable=False)
    # deaths = db.Column(db.Integer, nullable=False)
    # recovered = db.Column(db.Integer, nullable=False)
    # active = db.Column(db.Integer, nullable=False)
        args = dailyreport_get_args.parse_args() 
        result = DailyReportsModel.query.all()
        # print(result)
        data = {}
        i = 0
        for report in result:
            # if row is not None:
            if report is not None: 
                data[i] = {
                    'combined_key': report.combined_key,
                    'province_state': report.province_state,
                    'country_region': report.country_region,
                    'date': report.date,
                    'confirmed': report.confirmed,
                    'deaths': report.deaths,
                    'recovered': report.recovered,
                    'active': report.active
                }
                # print(data[i])
                i += 1


        filetype = args["filetype"]
        # for i in data:
        #     print(data[i])
        
        file_name = 'daily_report_query_results'
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

            return jsonfile
        elif filetype == "csv":
            file_type = '.csv'
            file_location = os.path.join(app.config['UPLOAD_FOLDER'], file_name + file_type)
            dataframe = pd.DataFrame.from_dict(data, orient='index')
            print(dataframe)
            csvdata = pd.DataFrame.to_csv(dataframe)
            print(csvdata)

            
            # csvfile.save(file_location)
            with open(file_path + file_name + file_type, 'w') as csvfile:
                csvfile.write(csvdata)
                # writer = csv.writer(csvfile) #, delimiter=' ')
                # writer.writerow(csvdata)
            # with open(file_path + file_name + file_type, 'w') as jsonfile:
            #     json.dump(data, jsonfile)
            # # And then we write a final newline to the end of the file 
            # # (this is just a best practice)
            #     jsonfile.write('\n')
            try:
                return send_from_directory(app.config["UPLOAD_FOLDER"], filename=file_name + file_type, as_attachment=True)

            except FileNotFoundError:
                abort(404, message="The file was not created")
        else:
            abort(404, message="File type not available. Must be csv or json") 
        # if args['combined_key']:
        #     print("you have asked for something!")
        #     result = DailyReportsModel.query.intersect(result, \
        #         DailyReportsModel.query.filter_by(combined_key=args['combined_key']).all())
        # name=args['combined_key']
        
        # Sketch solution
        if not result:
            abort(404, message="Could not find video with that ID...")
        return result



    @marshal_with(daily_resource_fields)
    def post(self):        
        print("received! thank you :)")
        # csvfile = request.data.decode(encoding)
        csvfile = io.StringIO(request.data.decode("UTF8"), newline=None)
        # print(csvfile)
        print("decoding!")
        # read_file = pd.read_csv (csvfile)
        # file_location = os.path.join(app.config['UPLOAD_FOLDER'], "upload")
        # read_file.to_csv(file_location, index=None)
        # `next` will simply skip over the header row in the csvfile
        next(csvfile)
        
        # # We use the csv library to create a 'reader' of the file
        # # This reader parses through the csvfile and the headers 
        # # and allow us to interact with it as a Python object
        reader = csv.DictReader(csvfile, daily_csv_fieldnames)
        print("reader is reading")
        # # Now we use the reader to iterate over all the rows of the CSV
        # # (except for the header) and then keep the values we want 

        # b'hello'.decode(encoding)
        for row in reader:
            # We also restructure the data so that it exists as 
            # a set of date keys with the value as a dictionary of
            # different data elements from the CSV.
            dailyReport = DailyReportsModel(combined_key = row["Combined_Key"],
                date = row["Last_Update"],
                province_state = row["Province_State"],
                country_region = row["Country_Region"],
                confirmed = row["Confirmed"],
                deaths = row["Deaths"],
                recovered = row["Recovered"],
                active = row["Active"])
            
            # you want to check if this report is in the database according to combined key and date
            # if it is not: 
            if attrNotNull(dailyReport):
                result = DailyReportsModel.query.filter_by(combined_key=row["Combined_Key"],\
                    date = row["Last_Update"]).first()
                # print("result:", result)
                if result is None: 
                    try: 
                        # print("We are adding the daily report!")
                        db.session.add(dailyReport)
                        # print(dailyReport)
                    except sqlite3.connector.IntegrityError:
                        return 'This already exists!- Integrity Error'
                    except orm_exc.FlushError:
                        return 'This already exists!- Conflict'
                        
                # else:
                #     print(dailyReport, "is already in here!")
            # if it is:
            # update the database for new information 
            # maybe call a separate function? so it can return? 
            # will that stop running this method as well?
        db.session.commit()
        return 200 # successful

    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        
        # NOTE:check/correct date formatting  

        # Sketch way to handle putting videos that already exist, probably want to use try and except instead
        if result:
            abort(409, message="Video ID taken...")

        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        
        # Temporarily add video to database
        db.session.add(video)

        # Permanently added videos to the databasee
        db.session.commit()

        # We can specify status codes in the return. Ex. 201
        return video, 201
    
        

    # Standard for updating, although there's also an update method?
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        
        db.session.commit()

        return result

    def delete(self):
        print("Goodbye everyone!!!")
        db.drop_all()

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

# @app.route('/clear', methods=['DELETE'])
# def clear():
    


# Register resources
api.add_resource(TimeSeries, "/time_series/<string:time_series_type>")
api.add_resource(DailyReports, "/daily_reports/")

if __name__ == "__main__":
    # Only debug in an development environment (not a production environment)
    app.run(debug=True) 