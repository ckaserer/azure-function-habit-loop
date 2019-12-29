import os
import sys
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pyodbc
import time

# Initialize Flask
app = Flask(__name__)

# Setup Flask Restful framework
api = Api(app)

# Create connection to Azure SQL
conn = pyodbc.connect(os.environ['WWIF'])

class Queryable(Resource):
    def executeQueryJson(self, myquery):
        result = {}        
        cursor = conn.cursor()  
        try:
            cursor.execute(f"{myquery}")
            columns = [column[0] for column in cursor.description]
            result = []
            for row in cursor.fetchall():
                result.append(dict(zip(columns, row)))
            cursor.commit()    
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:    
            cursor.close()
        return result

# Habit Class
class Habit(Queryable):
    def get(self, habit):   
        result = self.executeQueryJson(f"SELECT ID,habit,occured FROM habits WHERE CONVERT(VARCHAR, habit) = '{habit}' ORDER BY occured DESC")   
        return result, 200

    def post(self, habit):   
        return self.get(habit)
    
    def put(self, habit):
        result = self.executeQueryJson(f"INSERT INTO habits(habit,occured) OUTPUT INSERTED.id,INSERTED.habit,INSERTED.occured VALUES ('{habit}', '{int(time.time())}')")
        return result, 201
    
# # Create API routes
api.add_resource(Habit, '/habit', '/habit/<habit>')
