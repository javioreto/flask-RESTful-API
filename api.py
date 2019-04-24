#!flask/bin/python

from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path="")

if __name__ == '__main__':
    print("Hey! Starting server test")
    app.run()
