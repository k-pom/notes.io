import requests
from flask import render_template
from notes import app
from notes.lib.cache import cached_http_get, cache_until_changed
from datetime import datetime
import json
import os

github_user = os.environ.get('GITHUB_USER')
github_pass = os.environ.get('GITHUB_PASS')



class Comment():

    def __init__(self, comment):
        self.comment = comment

    @property
    def user(self):
        return self.comment['user']

    @property
    def body(self):
        return self.comment['body']

    @property
    def created_at(self):
        return datetime.strptime(self.comment['created_at'], "%Y-%m-%dT%H:%M:%SZ")


class Gist():

    def __init__(self, gist):
        self.gist = gist

    def auth(self):
        return (github_user, github_pass)

    def parsed(self, limit=False):

        def fetch():

            markdown = requests.get(self.first_file['raw_url']).text

            if limit:
                markdown = markdown[0:(limit+markdown[limit:].index('\n\n')+1)]

            html = requests.post(
                "https://api.github.com/markdown/raw",
                markdown,
                headers={"Content-Type": "text/x-markdown"},
                auth=(github_user, github_pass)
            )
            return html.text

        key = "%s-%s" % (self.first_file['raw_url'], limit)
        return cache_until_changed(key, self.gist['updated_at'], fetch)

    @property
    def number_comments(self):
        return self.gist['comments']

    @property
    def comments(self):
        return [Comment(c) for c in cached_http_get(self.gist['comments_url'], 300)]

    @property
    def owner(self):
        return self.gist['owner']

    @property
    def id(self):
        return self.gist['id']

    @property
    def description(self):
        return self.gist['description']

    @property
    def created_at(self):
        return datetime.strptime(self.gist['created_at'], "%Y-%m-%dT%H:%M:%SZ")

    @property
    def first_file(self):
        return self.gist['files'][self.gist['files'].keys()[0]]

    def is_valid(self):
        if not isinstance(self.gist, dict):
            return False

        return (
            self.description != ""
            and self.first_file['language'] == "Markdown"
        )

def get_gists(username):

    url = "https://api.github.com/users/%s/gists" % username
    all_gists = [Gist(g) for g in cached_http_get(url, 300)]
    return [g for g in all_gists if g.is_valid()]


def get_gist(id):
    url = "https://api.github.com/gists/%s" % id
    gist = Gist(cached_http_get(url, 300))

    if gist.is_valid():
        return gist

    return None
