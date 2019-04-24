#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, Response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth


# Example data
cars = [
    {
        'id': 1,
        'name': u'Volvo',
        'model': u'CX40',
        'price': 33000
    },
    {
        'id': 2,
        'name': u'Volvo',
        'model': u'CX60',
        'price': 41000
    },
    {
        'id': 3,
        'name': u'Renault',
        'model': u'Clio',
        'price': 12000
    }
]

# Example data model
cars_model = {
    'id': fields.Integer,
    'name': fields.String,
    'model': fields.String,
    'price': fields.Integer
}


'''
Application starts here
'''
app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(user):
    # list of auth users and passwords
    users = {'test': '1234', 'test2':'abcd'}
    if user in users:
        return users[user]
    else:
        return None


@auth.error_handler
def unauthorized():
    # when no authorized access return 403
    return make_response(jsonify({'error': 'Access denied'}), 403)


class GetCarList(Resource):
    decorators = [auth.login_required]

    def get(self):
        # Get all cars list
        return {'cars': marshal(cars, cars_model)}


api.add_resource(GetCarList, '/todo/api/v1/cars', endpoint='cars')


if __name__ == '__main__':
    app.run()
