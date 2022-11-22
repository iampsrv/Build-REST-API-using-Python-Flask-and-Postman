from flask import Flask, render_template, request, make_response, jsonify

app1 = Flask(__name__)


@app1.route('/')
def hello_world():
    return 'Hello World'


@app1.route('/pranjal')
def pranjal():
    return 'Hello Pranjal'


@app1.route('/html')
def get_html():
    return render_template("index.html")


@app1.route('/qs')
def get_qs():
    if request.args:
        req = request.args
        return " ".join(f"{k}:{v}" for k, v in req.items())

    return "No query"


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


@app1.route("/orders")
def get_order():
    response = make_response(jsonify(order), 200)
    return response


'''
Get order details using order id
'''


@app1.route("/orders/<orderid>")
def get_order_details(orderid):
    if orderid in order:
        response = make_response(jsonify(order[orderid]), 200)
        return response
    return "Order not found"


@app1.route("/orders/<orderid>/<items>")
def get_item_details(orderid, items):
    item = order[orderid].get(items)
    if item:
        response = make_response(jsonify(item), 200)
        return response
    return "Order not found"


@app1.route("/orders/<orderid>", methods=["POST"])
def post_order_details(orderid):  # create order
    req = request.get_json()
    if orderid in order:
        response = make_response(jsonify({"error": "Order ID already exists"}), 400)
        return response
    order.update({orderid: req})
    response = make_response(jsonify({"message": "New order created"}), 201)
    return response


@app1.route("/orders/<orderid>", methods=["PUT"])
def put_order_details(orderid):  # overwrite/create order
    req = request.get_json()
    if orderid in order:
        # order.update({orderid: req})
        order[orderid] = req
        response = make_response(jsonify({"message": "Order Updated"}), 200)
        return response
    order[orderid] = req
    response = make_response(jsonify({"message": "New order created"}), 201)
    return response


@app1.route("/orders/<orderid>", methods=["PATCH"])
def patch_order_details(orderid):  # add patches or update
    req = request.get_json()
    if orderid in order:
        for k, v in req.items():
            order[orderid][k] = v
        response = make_response(jsonify({"message": "Order Updated"}), 200)
        return response
    order[orderid] = req
    response = make_response(jsonify({"message": "New order created"}), 201)
    return response


@app1.route("/orders/<orderid>", methods=["DELETE"])
def delete_order_details(orderid):  # delete order
    if orderid in order:
        del order[orderid]
        response = make_response(jsonify({"message": "Order Deleted"}), 204)
        return response
    response = make_response(jsonify({"error": "Order ID already exists"}), 404)
    return response


@app1.route("/orders/<orderid>/<specs>", methods=["DELETE"])
def delete_order_spec_details(orderid, specs):  # delete order
    if orderid in order:
        if specs in order[orderid]:
            del order[orderid][specs]
            response = make_response(jsonify({"message": "Order Deleted"}), 204)
            return response
        response = make_response(jsonify({"error": "Specs not exists"}), 404)
        return response

    response = make_response(jsonify({"error": "Order ID not exists"}), 404)
    return response


if __name__ == '__main__':
    app1.run(debug=True)
