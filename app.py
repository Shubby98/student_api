from flask import *
from pymongo import MongoClient
from bson import json_util as json


MONGODB_URI = "mongodb://test:test123@ds147011.mlab.com:47011/student_db"
client = MongoClient(MONGODB_URI)
db = client.get_database("student_db")
student_record = db.student_records

app = Flask(__name__)


#welcome page
@app.route('/')
def index():
	return "Welcome to student Records API" 

@app.route('/students/', methods=['GET','POST'])
def student_list():
	if request.method == 'GET':
		data = list(student_record.find({}))
		return json.dumps(data)
	else:
		try:
			data = dict(request.form)
			data['roll_no'] = int(data['roll_no'])

			#check if record already exists
			if student_record.count_documents({'roll_no': data['roll_no']}):
					return json.dumps({'error': 'this record already exists! '})
			
			#create new record in DB
			student_record.insert_one(data)
			return json.dumps({'result' : 'Successfully added the record'})
		except Exception as e:
			return json.dumps({'error' : str(e)})
			


@app.route('/students/<int:roll_no>/' , methods= ['GET' , 'PATCH' , 'DELETE'])
def student_details(roll_no):
	if student_record.count_documents({'roll_no': roll_no}) is 0:
		return json.dumps({'error' : 'No record found'})

	if(request.method == 'GET'):
		record = student_record.find_one({'roll_no' : roll_no})
		return json.dumps(record)

	elif request.method == 'PATCH':
		record = student_record.find_one({'roll_no' : roll_no})
		record.update(dict(request.form))
		student_record.update({'roll_no' : roll_no}, {'$set' : record })
		return json.dumps({'result' : 'Successfully updated the record'})

	else:
		student_record.delete_one({'roll_no' : roll_no})
		return json.dumps({'result' : 'Successfully deleted the record'})

@app.route('/codeforces')
def codeforces():
	return "Welcome to codeforces " 




if __name__ == '__main__':
	app.run(port = 7000 ,debug = True,use_reloader = True) 