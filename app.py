#!/usr/bin/env python3

from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
import os
import configparser


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'db.conf'))

hostname = config.get('default', 'hostname')
username = config.get('default', 'username')
password = config.get('default', 'password')
database = config.get('default', 'database')


mysql = MySQL()
app = Flask(__name__)


app.config['MYSQL_DATABASE_USER'] = username
app.config['MYSQL_DATABASE_PASSWORD'] = password
app.config['MYSQL_DATABASE_DB'] = database
app.config['MYSQL_DATABASE_HOST'] = hostname


mysql.init_app(app)

api = Api(app)


@app.route('/director', methods=['GET', 'POST'])
def director():

    _name = request.values.get('name')
    # print(_name)
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT primary_title, directors, release_year, title_type, genres, rating, imdb_id FROM Film_Titles WHERE directors = %s""", [_name])
        data = cursor.fetchall()

        if data:
            return render_template('search.html', result_data=data)
        else:
            return render_template('search.html')

    except Exception as e:
        return render_template('500.html')

    return render_template('search.html')


@app.route("/search", methods=['GET', 'POST'])
def search():

    if request.method == 'POST':
        search_string = '%' + request.form['title'] + '%'

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT primary_title, directors, release_year, title_type, genres, rating, imdb_id FROM Film_Titles WHERE original_title LIKE %s OR directors LIKE %s""", [search_string, search_string])
            data = cursor.fetchall()

            if data:
                return render_template('search.html', result_data=data)
            else:
                return render_template('search.html')

        except Exception as e:
            return render_template('500.html')

    return render_template('search.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)
