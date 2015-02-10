import requests
from flask import render_template
from notes import app
from notes.lib import github
import os


@app.route("/")
def home():
    return render_template("home.html", username="")


@app.route("/<username>/page/<page>")
@app.route("/<username>")
def list(username, page=0):

    items_per_page = 10

    gists = github.get_gists(username)

    start = page*items_per_page

    if start+items_per_page > len(gists):
        gists.append(None)

    gists = gists[start:start+items_per_page]

    return render_template("list.html",
                           page=page,
                           username=username,
                           gists=gists)


@app.route("/<username>/<id>")
def show(username, id):
    return render_template("show.html",
                           username=username,
                           gist=github.get_gist(id))
