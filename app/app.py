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


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(host='0.0.0.0', port=5030, debug= True)
