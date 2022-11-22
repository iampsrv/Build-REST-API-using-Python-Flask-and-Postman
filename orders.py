from flask import Flask, render_template, request, make_response, jsonify

app = Flask(__name__)


@app.route('/')
def get_html():
    return render_template("make_your_own_pizza.html")


@app.route('/', methods=['POST', 'GET'])
def main():
    size = ['Small', 'Medium', 'Large', 'Xlarge']
    crust = ['Stuffed Crust', 'Cracker Crust', 'Flat Bread Crust', 'Thin Crust', 'Cheese Crust', 'Thick Crust']
    toppings = ['Cheese', 'Tomato', 'Mushroom', 'Capsicum', 'Onion', 'Paneer', 'Sweet Corn', 'Olives', 'Jalapeno','Pepperoni', 'Broccoli']
    if request.method == 'POST':
        input = request.form.get("input_text")
        selected_size = int(request.form.get("selected_size"))
        selected_crust = int(request.form.get("selected_crust"))
        selected_toppings = request.form.getlist("mytoppings")
        for i in range(0,len(selected_toppings)):
            selected_toppings[i]=int(selected_toppings[i])
        t=[]
        for i in selected_toppings:
            t.append(toppings[i-1])
        order={
            "name":input,
            "selected_size":size[selected_size],
            "selected_toppings":t,
            "selected_crust":crust[selected_crust]
        }
        return make_response(jsonify(order),200)
        #return render_template("make_your_own_pizza.html", input=input,selected_size=size[selected_size],selected_crust=crust[selected_crust],selected_toppings=t)


if __name__ == '__main__':
    app.run(debug=True)
