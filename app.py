from flask import *
import json
from mysql.connector import connect, Error
import collections
import numpy as np

# connect with local mysql database 
# password for ec2 is <blank> local is different
try:
    db_connection = connect(
        host= "localhost",
        user= "root",
        password= "",
        database="website")
    print(db_connection)
except Error as e:
    print(e)



app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True


# Backend

@app.errorhandler(500)
def internal_error(error):
	res = {'error': True, 
        'message': 'internal server error'}
	return json.dumps(res)



@app.route("/api/attractions")
def attraction_api_page():
	
	page_num = request.args.get("page", 0)
	page_num = int(page_num)
	offset_num = 12*page_num

	keyword = request.args.get("keyword")
	db_cursor = db_connection.cursor(buffered=True , dictionary=True) # extract value of specific column


	# check total page to decide next page number
	if keyword:
		pattern = "LIKE '%" + str(keyword) + "%'" 
		sql = "select count(id) from travel where name " + pattern
		db_cursor.execute(sql)
		total_rows = db_cursor.fetchall()[0]["count(id)"]		
	else:
		sql = "select count(id) from travel"
		db_cursor.execute(sql)
		total_rows = db_cursor.fetchall()[0]["count(id)"]


	if page_num>=(np.ceil(float(total_rows)/12)-1):
		next_page_num = None
	else:
		next_page_num =  page_num+1	


	if keyword:
		pattern = "LIKE '%" + str(keyword) + "%'" 
		if offset_num==0:
			sql = "select id, name, category, description, address, transport, mrt, latitude, longitude, images from travel where name " + pattern + " limit 12" 
		else:
			sql = "select id, name, category, description, address, transport, mrt, latitude, longitude, images from travel where name " + pattern + " limit " + str(offset_num) +" , 12"
	else:
		if offset_num==0:
			sql = "select id, name, category, description, address, transport, mrt, latitude, longitude, images from travel limit 12"
		else:
			sql = "select id, name, category, description, address, transport, mrt, latitude, longitude, images from travel limit " + str(offset_num) + " , 12"
		 
	db_cursor.execute(sql)

	
	res = db_cursor.fetchall()
	json_data = {"nextPage": next_page_num, "data":res}


	return render_template("attraction.html",result=json.dumps(json_data))



@app.route("/api/attraction/<attractionId>")
def attraction_api_page_id(attractionId):

	db_cursor = db_connection.cursor(buffered=True , dictionary=True) # extract value of specific column
	sql = "select id, name, category, description, address, transport, mrt, latitude, longitude, images from travel where id = " + str(attractionId)
	db_cursor.execute(sql)

	res = db_cursor.fetchall()

	if res:
		json_data = {"data":res}
		return render_template("attraction.html",result=json.dumps(json_data))
	else:
		res = {'error': True, 'message': '景點編號不正確'}
		return json.dumps(res),400





# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")




app.run(host="0.0.0.0",port=3000)

