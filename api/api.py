from flask import Flask
from flask_restful import Api, Resource, reqparse
from datetime import date, datetime
import json
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)
api = Api(app)

class Data():

    def db(post_data):

        engine = create_engine("sqlite:///inventory.db", echo=False)
        sqlite_table = "inventory"
        sqlite_connection = engine.connect()
        df = pd.DataFrame(post_data,index=[0])
        df.to_sql(sqlite_table, sqlite_connection, if_exists="append")
        sqlite_connection.close() 
        
    def export_to_file(post_data):

        time = date.today().strftime("%Y-%m-%d")
        # CSV EXPORT
        df = pd.DataFrame(post_data,index=[0])
        df.to_csv(post_data["IP"] + "_" + time + ".csv", index=False)
        # JSON EXPORT
        with open(post_data["IP"] + "_" + time + ".json", "w") as jfile:
            json.dump(post_data, jfile)


class Inventory(Resource):

    def get(self):

        return {'message': "I'm Alive"}

    def post(self):
        # PARSER REQUEST
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("IP")
        parser.add_argument("OS")
        parser.add_argument("OS_Version")
        parser.add_argument("Processor")
        parser.add_argument("Users")
        parser.add_argument("Processes")
        args = parser.parse_args()
        # DATA PROCESSING
        post_data = {
            "Report_Date": datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
            "IP": args["IP"],
            "OS": args["OS"],
            "OS_Version": args["OS_Version"], 
            "Processor" : args["Processor"],
            "Users": args["Users"],
            "Processes" : args["Processes"]
        }

        Data.db(post_data)
        Data.export_to_file(post_data)

    
        return print("It's working great, please hire me :)"), 201


api.add_resource(Inventory, "/inventory")
if __name__ == '__main__':
    app.run(debug=True)