#!flask/bin/python

from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource, fields, marshal
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
    return make_response(jsonify({'Error': 'Access denied'}), 403)


class GetCarList(Resource):
    decorators = [auth.login_required]

    def get(self):
        # Get all cars list
        return {'cars': marshal(cars, cars_model)}

    def post(self):
        # Insert new car
        # Check the next id
        args = request.json
        if 'name' in args and 'model' in args and 'price' in args:
            new_id = 0
            for i in range(len(cars)):
                if cars[i]['id'] > new_id:
                    new_id = cars[i]['id']
            # New Id to use
            new_id += 1

            # Parse JSON and create new car
            new_car = {
                'id': new_id,
                'name': args['name'],
                'model': args['model'],
                'price': args['price']
            }
            cars.append(new_car)
            return {'cars': marshal(new_car, cars_model)}
        else:
            return make_response(jsonify({'Error': 'Name, model and price are requiered.'}), 400)

class GetCarById(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        # Get car by id
        for i in range(len(cars)):
            if cars[i]['id'] == id:
                return {'car': marshal(cars[i], cars_model)}
        return make_response(jsonify({'Error': 'Not found'}), 404)

    def delete(self, id):
        # Delete car by id
        for i in range(len(cars)):
            if cars[i]['id'] == id:
                cars.remove(cars[i])
                return make_response(jsonify({'Result': True}), 201)
        return make_response(jsonify({'Error': 'Not found'}), 404)

    def put(self, id):
        # Update car by id
        args = request.json
        for i in range(len(cars)):
            if cars[i]['id'] == id:
                cars[i]['name'] = args['name'] if 'name' in args else cars[i]['name']
                cars[i]['model'] = args['model'] if 'model' in args else cars[i]['model']
                cars[i]['price'] = args['price'] if 'price' in args else cars[i]['price']
                return {'cars': marshal(cars[i], cars_model)}
        return make_response(jsonify({'Error': 'Not found'}), 404)

class FilterCars(Resource):
    decorators = [auth.login_required]

    def post(self):
        # Filter Cars by min and max price
        result = []
        args = request.json
        min = args['min'] if 'min' in args else 0
        max = args['max'] if 'max' in args else 9999999999
    
        for i in range(len(cars)):
            if cars[i]['price'] >= min and cars[i]['price'] <= max:
                result.append(cars[i])

        if len(result) > 0:
            return {'cars': marshal(result, cars_model)}
        else:
            return make_response(jsonify({'Error': 'No content'}), 204)

api.add_resource(GetCarList, '/todo/api/v1/cars', endpoint='cars')
api.add_resource(GetCarById, '/todo/api/v1/cars/<int:id>', endpoint='car')
api.add_resource(FilterCars, '/todo/api/v1/cars/filter', endpoint='filter')

if __name__ == '__main__':
    app.run()
