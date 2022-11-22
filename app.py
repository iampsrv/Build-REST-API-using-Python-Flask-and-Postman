from flask import Flask, make_response, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloEveryone(Resource):
    def get(self):
        return {'Hello': 'World'}


api.add_resource(HelloEveryone, '/')


###################################################

class HelloName(Resource):
    def get(self, name):
        return {'Hello': name}


api.add_resource(HelloName, '/<string:name>')
###################################################
order = {
    "order1": {
        "Size": "Small",
        "Toppings": "Cheese",
        "Crust": "Thin Crust"
    },
    "order2": {
        "Size": "Medium",
        "Toppings": "Tomato",
        "Crust": "Thick Crust"
    }
}


###################################################

class Orders(Resource):
    def get(self):
        return order


api.add_resource(Orders, '/orders')


###################################################

class OrdersID(Resource):
    def get(self, orderid):
        return order[orderid]

    def post(self, orderid):
        if orderid in order:
            response = make_response(jsonify({"Error": "Order ID already exists"}))
            return response
        req = request.get_json()
        order.update({orderid: req})
        response = make_response(jsonify({"Message": "New Order ID created"}))
        return response

    def put(self, orderid):
        req = request.get_json()
        if orderid in order:
            order[orderid] = req
            response = make_response(jsonify({"Message": "Order ID updated"}))
            return response
        order[orderid] = req
        response = make_response(jsonify({"Message": "New Order ID created"}))
        return response

    def patch(self, orderid):
        req = request.get_json()
        if orderid in order:
            for i, j in req.items():
                order[orderid][i] = j
            response = make_response(jsonify({"Message": "Order ID updated"}))
            return response
        order[orderid] = req
        response = make_response(jsonify({"Message": "New Order ID created"}))
        return response

    def delete(self, orderid):
        if orderid in order:
            del order[orderid]
            response = make_response(jsonify({}))
            return response
        response = make_response(jsonify({"Error": "Order ID not found"}))
        return response


api.add_resource(OrdersID, '/orders/<string:orderid>')


###################################################

class OrdersIDwithoptions(Resource):
    def get(self, orderid, options):
        return order[orderid][options]


api.add_resource(OrdersIDwithoptions, '/orders/<string:orderid>/<string:options>')
###################################################


if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask
# app = Flask(__name__)
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
# if __name__ == '__main__':
#     app.run()
