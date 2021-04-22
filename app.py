from flask import *
import json
from mysql.connector import connect, Error
import collections

# connect with local mysql database 
try:
    db_connection = connect(
        host= "localhost",
        user= "root",
        password= "Chloe951753@",
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
	res = {'error': True, 'message': 'internal server error'}
	return json.dumps(res)



@app.route("/api/attractions")
def attraction_page():
	
	page_num = request.args.get("page", 0)
	page_num = int(page_num)
	item_min = 1+12*page_num
	item_max = 12+12*page_num

	keyword = request.args.get("keyword")
	db_cursor = db_connection.cursor(buffered=True , dictionary=True) # extract value of specific column
 

	json_data = {}
	if keyword:
		pattern = "LIKE '%" + str(keyword) + "%'" 
		sql = "select id, name, category, description, address, transport, mrt, latitude, longitude, images from travel where name " + pattern + " and id between " + str(item_min) + " and " + str(item_max) + " order by id"
		db_cursor.execute(sql)
	else:
		sql = "select id, name, category, description, address, transport, mrt, latitude, longitude, images from travel where id between %s and %s order by id"
		db_cursor.execute(sql,(item_min,item_max))

	res = db_cursor.fetchall()
	json_data = {"nextPage": page_num+1, "data":res}

	return render_template("attraction.html",result=json.dumps(json_data))








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

app.run(port=3000)