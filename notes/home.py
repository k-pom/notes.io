import requests
from flask import render_template
from notes import app
import os

def get_gists_for_user(username, page=0):

    items_per_page = 10
    github_user = os.environ.get('GITHUB_USER')
    github_pass = os.environ.get('GITHUB_PASS')
    url = "https://api.github.com/users/%s/gists" % username

    gists = requests.get(url, auth=(github_user, github_pass)).json()
    gists = [g for g in gists if g['description'] != "description" and g['files'][g['files'].keys()[0]]['language'] == "Markdown"]

    start = page*items_per_page

    if start+items_per_page > len(gists):
        gists.append(None)

    return gists[start:start+items_per_page]

@app.route("/")
def home():
    return render_template("home.html", username="")


@app.route("/<username>/page/<page>")
@app.route("/<username>")
def list(username, page=0):
    page = int(page)
    gists = get_gists_for_user(username, int(page))
    return render_template("list.html",
                           page=page,
                           username=username,
                           gists=gists)

@app.route("/<username>/<id>")
def show(username, id):

    github_user = os.environ.get('GITHUB_USER')
    github_pass = os.environ.get('GITHUB_PASS')
    url = "https://api.github.com/gists/%s" % id

    gist = requests.get(url, auth=(github_user, github_pass)).json()

    return render_template("show.html", username=username, gist=gist)
