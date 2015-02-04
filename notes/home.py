import requests
from flask import render_template
from notes import app
import os


@app.route("/")
def home():

    return render_template("home.html", username="")


@app.route("/<username>")
def list(username):

    github_user = os.environ.get('GITHUB_USER')
    github_pass = os.environ.get('GITHUB_PASS')
    url = "https://api.github.com/users/%s/gists" % username

    gists = requests.get(url, auth=(github_user, github_pass)).json()

    return render_template("list.html", username=username, gists=gists)


@app.route("/<username>/<id>")
def show(username, id):

    github_user = os.environ.get('GITHUB_USER')
    github_pass = os.environ.get('GITHUB_PASS')
    url = "https://api.github.com/gists/%s" % id

    gist = requests.get(url, auth=(github_user, github_pass)).json()

    return render_template("show.html", username=username, gist=gist)
