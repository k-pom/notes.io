from flask import Flask
from datetime import datetime
import os
import requests

app = Flask("notes.io")
app.secret_key = os.environ.get('SECRET_KEY')

import notes.home

@app.template_filter('datetimeformat')
def datetimeformat(value, format="%b %d, %Y"):
    return value.strftime(format)
