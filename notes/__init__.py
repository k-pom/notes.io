from flask import Flask
from datetime import datetime
from markdown import markdown
import os
import requests

app = Flask("notes.io")
app.secret_key = os.environ.get('SECRET_KEY')

import notes.home


@app.template_filter('datetimeformat')
def datetimeformat(value, in_format="%Y-%m-%dT%H:%M:%SZ", out_format="%B %d, %Y"):
    return (datetime.strptime(value, in_format)).strftime(out_format)

@app.template_filter('get_as_markdown')
def datetimeformat(raw_url):

    markdown = requests.get(raw_url).text

    github_user = os.environ.get('GITHUB_USER')
    github_pass = os.environ.get('GITHUB_PASS')
    html = requests.post(
        "https://api.github.com/markdown/raw",
        markdown,
        headers={"Content-Type": "text/x-markdown"},
        auth=(github_user, github_pass))

    return html.text
