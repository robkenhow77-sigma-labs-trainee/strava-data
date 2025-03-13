from os import urandom, environ as ENV
from time import sleep
from datetime import datetime
import json

from dotenv import load_dotenv
from requests import get, post
from flask import Flask, redirect, request, session, render_template

from functions import make_pace_graph, make_elevation_graph

load_dotenv
app = Flask(__name__)
app.secret_key = urandom(20)


def make_activities_table(data: dict):
    """Makes the table for the main page"""
    html = ""
    for row in data:
        date_time = datetime.fromisoformat(row["start_date"])
        date_time = datetime.strftime(date_time, "%d/%m/%Y, %H:%M")
        html += f"""
            <tr>
                <td>{date_time}</td>
                <td>
                    <a href = "/activities/{row["id"]}">{row["sport_type"]}<a/>
                </td>
                <td>{row["elapsed_time"]}</td>
                <td>{row["kudos_count"]}</td>
            </tr>
            """
    return html




@app.route("/")
def hello_world():
    return render_template('welcome_page.html')


@app.route("/callback")
def callback():
    sleep(1)
    code = request.args.get("code")
    session["code"] = code
    POST = f"https://www.strava.com/oauth/token?client_id={ENV["CLIENT_ID"]}&client_secret={ENV["CLIENT_SECRET"]}&code={code}&grant_type=authorization_code"
    res = post(POST)
    if res.status_code != 200:
        return "Bad request", 400
    session["access_token"] = res.json()["access_token"]
    return redirect("/main")


@app.route("/main")
def welcome():
    """API call to get strava information"""
    res = get("https://www.strava.com/api/v3/activities", headers={"Authorization": f'Bearer {session["access_token"]}'})
    data = res.json()
    table_html = make_activities_table(data)
    """Adding a variable to a template"""
    return render_template('main_page.html', table_data=table_html)


@app.route("/activities/<int:id>")
def activity(id):
    res = get(f"https://www.strava.com/api/v3//activities/{id}", headers={"Authorization": f'Bearer {session["access_token"]}'})
    data = res.json()
    pace_graph = make_pace_graph(data)
    elevation_graph = make_elevation_graph(data)
    polyline_str = data["map"]["summary_polyline"]
    return render_template('activity.html',  API_KEY=ENV["API_KEY"], polyline=json.dumps(polyline_str), pace_graph=pace_graph, elevation_graph=elevation_graph)

