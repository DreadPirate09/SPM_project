from flask import Flask, request
import requests
import json
import csv

app = Flask(__name__)

nume = "john"
password = "john"

@app.route("/login", methods=["GET","POST"])
def login():

	checkFlag = 0

	db = open('db.csv')
	header = []
	csvreader = csv.reader(db)
	header = next(csvreader)


	json_data = request.get_json()
	dict_data = json.loads(json.dumps(json_data))

	print(dict_data)
	for row in csvreader:
		print(list(row)[0],list(row)[1])
		if list(row)[0] == dict_data['name'] and list(row)[1] == dict_data['password']:
			print('neh')
			checkFlag = 1
		print(dict_data['name'])
		print(dict_data['password'])

	if checkFlag == 1:
		response = {
			"raspuns":"access granted"
		}
	else:
		response = {
			"raspuns":"wrong password"
		}

	return json.dumps(response)

@app.route("/register", methods=["GET","POST"])
def register():

	json_data = request.get_json()
	dict_data = json.loads(json.dumps(json_data))
	try:
		db = open('db.csv','a')
		row = str(dict_data['email'])+","+str(dict_data['password'])+"\n"
		db.write(row)
		print('nume si parola adaugate')
		db.close()
		response = 'user adaugat'
		return json.dumps(response)
	except Exception as e:
		print('a aparut o eroare',e)
		response = str(e)
		return json.dumps(response)


if __name__ == "__main__":
    app.debug = True
    app.run()