from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'homeData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Samir'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM homes')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, homes=result)


@app.route('/view/<string:sell>', methods=['GET'])
def record_view(sell):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM homes WHERE Sell=%s', sell)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', home=result[0])


@app.route('/edit/<string:sell>', methods=['GET'])
def form_edit_get(sell):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM homes WHERE Sell=%s', sell)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', home=result[0])


@app.route('/edit/<string:sell>', methods=['POST'])
def form_update_post(sell):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Sell'), request.form.get('List'), request.form.get('Living'),
                 request.form.get('Rooms'), request.form.get('Beds'), request.form.get('Baths'),
                 request.form.get('Age'), request.form.get('Acres'), request.form.get('Taxes'), sell)
    sql_update_query = """UPDATE homes t SET t.Sell = %s, t.List = %s, t.Living = %s, t.Rooms = 
    %s, t.Beds = %s, t.Baths = %s, t.Age = %s, t.Acres = %s, t.Taxes = %s WHERE t.Sell = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/home/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Home Form')


@app.route('/home/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Sell'), request.form.get('List'), request.form.get('Living'),
                 request.form.get('Rooms'), request.form.get('Beds'), request.form.get('Baths'),
                 request.form.get('Age'), request.form.get('Acres'), request.form.get('Taxes'))
    sql_insert_query = """INSERT INTO homes (Sell,List,Living,Rooms,Beds,Baths,Age,Acres,Taxes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<string:sell>', methods=['POST'])
def form_delete_post(sell):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM homes WHERE Sell = %s """
    cursor.execute(sql_delete_query, sell)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM homes')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['GET'])
def api_retrieve(city_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM homes WHERE id=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['PUT'])
def api_edit(city_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/cities/<int:city_id>', methods=['DELETE'])
def api_delete(city_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
