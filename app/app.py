from typing import List, Dict
import mysql.connector
import simplejson as json
# import str as str
from flask import Flask, Response, request, redirect
from flask import render_template

app = Flask(__name__ , template_folder='templates')

from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_USER'] = 'afu2'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'heightWidth'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Height Width Data'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM hw_100')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cities=result)


@app.route('/view/<int:Index>', methods=['GET'])
def view(Index):
    cursor = mysql.get_db().cursor()
    # id = city_id.id
    # id = request.args.get('city_id')
    # id = request.form('city_id')
    cursor.execute('SELECT * FROM hw_100 WHERE `Index`= %s', Index)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<int:Index>', methods=['GET'])
def form_edit_get(Index):
    # return render_template('edit1.html', title='Edit Form', city= city_id)
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM hw_100 WHERE `Index`= %s', Index)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:Index>', methods=['POST'])
def form_update_post(Index):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Index'), request.form.get('Height_Inches'), request.form.get('Weight_Pounds'), Index)
    sql_update_query = """UPDATE hw_100 t SET t.Index = %s, t.Height_Inches = %s, t.Weight_Pounds = %s WHERE t.Index = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    cursor.close()
    return redirect("/", code=302)


@app.route('/hw/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='Height Width Form')


@app.route('/hw/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Index'), request.form.get('Height_Inches'), request.form.get('Weight_Pounds'))
    sql_insert_query = """INSERT INTO hw_100 (`Index`,`Height_Inches`,`Weight_Pounds`) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:Index>', methods=['POST'])
def form_delete_post(Index):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM hw_100 WHERE `Index` = %s """
    cursor.execute(sql_delete_query, Index)
    mysql.get_db().commit()
    return redirect("/", code=302)

# API
@app.route('/api/v1/hw', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM hw_100')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/hw/<int:Index>', methods=['GET'])
def api_retrieve(Index) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM hw_100 WHERE `Index`= %s', Index)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/hw/<int:Index>', methods=['PUT'])
def api_edit(Index) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Index'], content['Height_Inches'], content['Weight_Pounds'], Index)
    sql_update_query = """UPDATE hw_100 t SET t.Index = %s, t.Height_Inches = %s, t.Weight_Pounds = %s WHERE t.Index = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/hw', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Index'], content['Height_Inches'], content['Weight_Pounds'])
    sql_insert_query = """INSERT INTO hw_100 (`Index`,`Height_Inches`,`Weight_Pounds`) VALUES (%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/hw/<int:Index>', methods=['DELETE'])
def api_delete(Index) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM hw_100 WHERE `Index` = %s """
    cursor.execute(sql_delete_query, Index)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(host='0.0.0.0', port=5030, debug= True)
