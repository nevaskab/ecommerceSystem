from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)

file_path = 'products.json'

with open(file_path, 'r') as file:
    products = json.load(file)

#product route    
@app.route('/search/products', methods = ['GET'])
def get_products():
    return jsonify(products)

#ID route
@app.route('/search/products/<int:prod_id>', methods = ['GET'])
def get_product(prod_id):
    product = next((p for p in products if p['id'] == prod_id), None)
    if product is None:
        abort(404)
    return jsonify(product)

#add product
@app.route('/search/products', methods = ['POST'])
def add_product():
    if not request.json or not 'name' in request.json:
        abort(400)
    new_product = {
        'id': products[-1]['id'] + 1 if products else 1,
        'name': request.json['name'],
        'description': request.json.get('description', ""),
        'price': request.json.get('price', 0.0),
    }
    products.append(new_product)
    save_products()
    return jsonify(new_product), 201

#update product
@app.route('/search/products/<int:prod_id>', methods = ['PUT'])
def update_product(prod_id):
    product = next((p for p in products if p['id'] == prod_id), None)
    if product is None:
        abort(404)
    if not request.json:
        abort(400)
    product['name'] = request.json.get('name', product['name'])
    product['description'] = request.json.get('description', product['description'])
    product['price'] = request.json.get('price', product['price'])
    save_products()
    return jsonify(product)
    
#delete product
@app.route('/search/products/<int:prod_id>', methods = ['DELETE'])
def delete_product(prod_id):
    product = next((p for p in products if p['id'] == prod_id), None)
    if product is None:
        abort(404)    
    products.remove(product)
    save_products()
    return jsonify({'result': True})

#save prod on json file
def save_products():
    with open(file_path, 'w') as file:
        json.dump(products, file, indent = 4)

if __name__ == '__main__':
    app.run(debug=True)