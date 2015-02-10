import requests
from flask import render_template
from notes import app
from datetime import datetime
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

    # TODO: Cache this
    def parsed(self, limit=False):

        if 'content' not in self.first_file:
            markdown = requests.get(self.first_file['raw_url']).text
        else:
            markdown = self.first_file['content']

        if limit:
            markdown = markdown[0:(limit+markdown[limit:].index('\n\n')+1)]

        html = requests.post(
            "https://api.github.com/markdown/raw",
            markdown,
            headers={"Content-Type": "text/x-markdown"},
            auth=(github_user, github_pass)
        )

        return html.text

    @property
    def number_comments(self):
        return self.gist['comments']

    @property
    def comments(self):
        # TODO: Cache
        comments = requests.get(self.gist['comments_url'], auth=(github_user, github_pass)).json()
        return [Comment(c) for c in comments]

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
    """
        Return all valid gists for a user
    """

    url = "https://api.github.com/users/%s/gists" % username

    all_gists = [Gist(g) for g in requests.get(url, auth=(github_user, github_pass)).json()]

    return [g for g in all_gists if g.is_valid()]


def get_gist(id):

    url = "https://api.github.com/gists/%s" % id
    gist = Gist(requests.get(url, auth=(github_user, github_pass)).json())

    if gist.is_valid():


        return gist

    print "WAS'T VALID"
    return None

#
# def get_parsed_gist(id):
# gist['files'][gist['files'].keys()[0]]['raw_url']
#     gist = get_gist(id)
#     # Check
#     markdown = requests.get(raw_url).text
#
#     if limit:
#         markdown = markdown[0:(limit+markdown[limit:].index('\n\n')+1)]
#
#     github_user = os.environ.get('GITHUB_USER')
#     github_pass = os.environ.get('GITHUB_PASS')
#     html = requests.post(
#         "https://api.github.com/markdown/raw",
#         markdown,
#         headers={"Content-Type": "text/x-markdown"},
#         auth=(github_user, github_pass))
#
#     return html.text
