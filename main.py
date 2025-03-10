from os import urandom, environ as ENV
from time import sleep

from dotenv import load_dotenv
from requests import get, post
from flask import Flask, redirect, request, session, render_template


load_dotenv
app = Flask(__name__)
app.secret_key = urandom(20)


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
    print(res)
    if res.status_code != 200:
        return "Bad request", 400
    session["access_token"] = res.json()["access_token"]
    return redirect("/welcome")


@app.route("/welcome")
def welcome():
    res = get("https://www.strava.com/api/v3/activities", headers={"Authorization": f'Bearer {session["access_token"]}'})
    return res.json()
