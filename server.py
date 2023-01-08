from flask import Flask, request
import requests
import json
import csv

app = Flask(__name__)

nume = "john"
password = "john"


def get_friends_names(user):
	file = open(user+'.csv','r')
	names = list()
	nr = 0
	csvreader = csv.reader(file)
	for lines in csvreader:
		names.append(lines[1])
	file.close()

	return names

def get_coordinates_by_names(names):
	coordinates = list()
	vals = list()
	lastName = None
	lastC1 = None
	lastC2 = None
	for i in range(len(names)):
		file = open('coordinates.csv','r')
		csvreader = csv.reader(file)
		for lines in csvreader:
			if lines[0] == names[i] :
				lastName = lines[0]
				lastC1 = lines[1]
				lastC2 = lines[2]
		coordinates.append([str(lastName),str(lastC1),str(lastC2)])
	return coordinates


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

@app.route("/addFriend", methods=["GET","POST"])
def addFriend():

	json_data = request.get_json()
	dict_data = json.loads(json.dumps(json_data))
	response = ''
	try:
		coord = open('coordinates.csv','r')
		csvreader = csv.reader(coord)
		print('before fore')
		for lines in csvreader:
			print(lines)
			if len(lines) and lines[3] == dict_data['code'] :
				db = open(dict_data['user']+'.csv','a')
				db.write(str(dict_data['code'])+","+str(lines[0])+'\n')
				db.close()
				response = 'userul cu numele '+lines[0]+' a fost adaugat'
		coord.close()

		print('after for')
		if len(response):
			print('response')
			return json.dumps(response)
		else:
			return json.dumps('Nu am gasit nici o persoana cu codul introdus')
	except Exception as e:
		print('a aparut o eroare',e)
		response = str(e)
		return json.dumps(response)

@app.route("/postCoordinates", methods=["GET","POST"])
def postCoordinates():

	json_data = request.get_json()
	dict_data = json.loads(json.dumps(json_data))

	try:
		db = open('coordinates.csv','a')
		csvreader2 = csv.reader(db)
		row = str(dict_data['name'])+","+str(dict_data['coordinates'])+","+str(dict_data['uniqueCode'])+"\n"
		db.write(row)

		print('nume si coordonates adaugate')
		db.close()
		response = 'success'
		return json.dumps(response)
	except Exception as e:
		print('error',e)
		response = str(e)
		return json.dumps(response)

@app.route("/getAllFriendsCoordinates", methods=["GET","POST"])
def getAllFriendsCoordinates():
	json_data = request.get_json()
	dict_data = json.loads(json.dumps(json_data))

	response = get_coordinates_by_names(get_friends_names(dict_data['user']))
	print(response)
	return json.dumps(response)


if __name__ == "__main__":
    app.debug = True
    app.run()