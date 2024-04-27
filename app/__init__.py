from flask import Flask, request, redirect, url_for

app = Flask(__name__)
app.config.from_object('app.config.Config')

from app import views