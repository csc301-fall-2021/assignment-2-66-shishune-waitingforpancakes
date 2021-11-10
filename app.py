# Imports
from flask import Flask, jsonify, request, send_from_directory
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
import csv
import json
import os
import urllib.request
from werkzeug.utils import secure_filename
import pandas as pd

# Configure app, API and database
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
db = SQLAlchemy(app)

class TimeSeriesModel(db.Model):
    province_state = db.Column(db.String(100), primary_key=True)
    country_region = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    confirmed = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    recovered = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"TimeSeries(Province/State = {province_state}, \
            Country/Region = {country_region}, \
            Date = {date}, \
            Confirmed = {confirmed}, \
            Deaths = {deaths},\
            Recovered = {recovered}, \
            Active = {active})"

class DailyReportsModel(db.Model):
    combined_key = db.Column(db.String(100), primary_key=True)  
    # note: combined key should be province and country, 
    # so remove admin2[city] for daily reports..?
    province_state = db.Column(db.String(100), nullable=False)
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
db.create_all() 

# Automatically parses through the request being sent and ensures it matches the guidelines
# timeseries_args = reqparse.RequestParser()
# timeseries_args.add_argument("province_state", type=str, help="Province/State of COVID Report.", required=True)
# timeseries_args.add_argument("country_region", type=str, help="Country/Region of COVID Report.", required=True)
# timeseries_args.add_argument("date", type=str, help="Date of COVID Report.", required=True)
# timeseries_args.add_argument("time_series_type", type=str, help="Confirmed COVID Cases.", required=True)
# timeseries_args.add_argument("time_series_type_value", type=int, help="Deaths from COVID.", required=True)


# dailyreport_args = reqparse.RequestParser()
# dailyreport_args.add_argument("province_state", type=str, help="Province/State of COVID Report.", required=True)
# dailyreport_args.add_argument("country_region", type=str, help="Country/Region of COVID Report.", required=True)
# dailyreport_args.add_argument("date", type=str, help="Date of COVID Report.", required=True)
# dailyreport_args.add_argument("confirmed", type=str, help="Confirmed COVID Cases.", required=True)
# dailyreport_args.add_argument("deaths", type=int, help="Deaths from COVID.", required=True)
# dailyreport_args.add_argument("active", type=str, help="Active COVID Cases.", required=True)
# dailyreport_args.add_argument("recovered", type=int, help="Recovered from COVID.", required=True)

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
    @marshal_with(resource_fields)
    def get(self, combined_key):
        try:
            result = CovidReportsModel.filter_by(id=combined_key).first()
            return result
        except:
            abort(404, message="Could not find report...")
    
    def post(self, type):
        post_data = request.data 
        with open(file, 'r') as csvfile:
            # `next` will simply skip over the header row in the csvfile
            next(csvfile)
            # We use the csv library to create a 'reader' of the file
            # This reader parses through the csvfile and the headers 
            # and allow us to interact with it as a Python object
            reader = csv.DictReader(csvfile, daily_csv_fieldnames)

            # Now we use the reader to iterate over all the rows of the CSV
            # (except for the header) and then keep the values we want 
            for row in post_data: 
                province_state = post_data.get('Province/State')
                country_region = post_data.get('Country/Region')

                report = TimeSeriesModel(province_state=province_state, \
                                        country_region=country_region)
            
                try:
                    db.session.add(report)
                except:
                    abort(409, message="Report already made...")
        try:
            db.session.commit()
            return report, 201
        except:
            abort(409, message="Report already made...")

    @marshal_with(resource_fields)
    def patch(self, video_id):
        return "result"

    def delete(self, video_id):
        return "", 204

dailyreport_args = reqparse.RequestParser()
dailyreport_args.add_argument("combined_key", type=str, help="City, Province/State and Country/Region of COVID Report.", required=True)
dailyreport_args.add_argument("province_state", type=str, help="Province/State of COVID Report.", required=True)
dailyreport_args.add_argument("country_region", type=str, help="Country/Region of COVID Report.", required=True)
dailyreport_args.add_argument("date", type=str, help="Date of COVID Report.", required=True)
dailyreport_args.add_argument("confirmed", type=str, help="Confirmed COVID Cases.", required=True)
dailyreport_args.add_argument("deaths", type=int, help="Deaths from COVID.", required=True)
dailyreport_args.add_argument("active", type=str, help="Active COVID Cases.", required=True)
dailyreport_args.add_argument("recovered", type=int, help="Recovered from COVID.", required=True)

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


UPLOAD_DIRECTORY = "tmp/files"

UPLOAD_FOLDER = 'tmp/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

encoding = 'utf-8' 

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

class DailyReports(Resource):
    # This decorator is used for the return
    # When we return, take these values and serialize with these fields
    @marshal_with(daily_resource_fields)
    def get(self, video_id):
        result = DailyReportsModel.query.filter_by(id=video_id).first()

        # Sketch solution
        if not result:
            abort(404, message="Could not find video with that ID...")
        return result



    @marshal_with(daily_resource_fields)
    def post(self):
        # print(request.data)
        # if 'daily_reports' not in request.files:
        #     print("no files")
        #     resp = jsonify({'message' : 'No file part in the request'})
        #     resp.status_code = 400
        #     return resp

        # files = request.files.getlist('daily_reports')
        # files = request.files # .getlist('daily_reports')
        # print("files:",files)
        # for file in files:
        #     print('file:', file)
        #     # filename = secure_filename(file.filename)
        #     file_location = os.path.join(app.config['UPLOAD_FOLDER'], "upload")
        #     file.save(file_location)
   
        # # file = request.files
        #     with open(file_location, 'r') as csvfile:
        #  csvfile = request.data
        print("received! thank you :)")
        csvfile = request.data.decode(encoding)
        print(csvfile)
        print("decoding!")
        # `next` will simply skip over the header row in the csvfile
        # next(csvfile)
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
                country_region = row["Combined_Key"],
                confirmed = row["Confirmed"],
                deaths = row["Deaths"],
                recovered = row["Recovered"],
                active = row["Active"])
            
            # you want to check if this report is in the database according to combined key and date
            # if it is not: 
            if attrNotNull(dailyReport):
                print(dailyReport)
                result = DailyReportsModel.query.filter_by(combined_key=row["Combined_Key"],\
                    date = row["Combined_Key"]).first()
                if not result: 
                    try: 
                        db.session.add(dailyReport)
                        print(dailyReport)
                    except sqlite3.connector.IntegrityError as err:
                        return 'This already exists!'
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

    def delete(self, video_id):
        return "", 204

def attrNotNull(dailyReport):
    if dailyReport.combined_key is None or \
        dailyReport.date is None or \
        dailyReport.province_state is None or dailyReport.country_region is None or \
        dailyReport.confirmed is None or \
        dailyReport.deaths is None or \
        dailyReport.recovered is None or \
        dailyReport.active is None:
        return False
    return True



# Register resources
api.add_resource(TimeSeries, "/time_series/")
api.add_resource(DailyReports, "/daily_reports/")

if __name__ == "__main__":
    # Only debug in an development environment (not a production environment)
    app.run(debug=True) 