# flask-RESTful-API

# First steps
- Intall in your pc Python2.7, pip and Git.
- Then, clone this repository and execute install commands:

```
python -m virtualenv flask
source flask/bin/activate
pip install -r requirements.txt
```

# Execute API server
- Run **python ./api.py** to start the server.
- Default server host is **http://127.0.0.1:5000**.

# Endpoints
- Basic auth with user and password. By default: user-> **test** and password-> **1234**.
- **GET /todo/api/v1/cars** Get all cars list
- **POST /todo/api/v1/cars** Insert new car (requiered all values)
```
        {
            "name": "Volvo",
            "model": "CX40",
            "price": 33000
        }
```
- **GET /todo/api/v1/cars/{id}** Get car by id
- **PUT /todo/api/v1/cars/{id}** Update one car (you can update all or partial data)
```
        {
            "name": "Volvo",
            "model": "CX40",
            "price": 56000
        }
```
- **DELETE /todo/api/v1/cars/{id}** Delete one car
- **POST /todo/api/v1/cars/filter** Filter cars by price max or/and min.
```
        {
            "min": 1500,
            "max": 50000
        }
```
- IMPORTAN: Send body data using Content-Type **application/json**