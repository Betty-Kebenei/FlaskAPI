from flask import request, jsonify, abort
from app.models import ShoppingList, ShoppingItems
from app import create_app

app = create_app(config_name="development")


@app.route('/shoppinglists/', methods=['POST', 'GET'])
def shoppinglists():
    if request.method == "POST":
        listname = str(request.data.get('listname'))
        if listname:
            shoppinglist = ShoppingList(listname=listname)
            shoppinglist.save()
            response = jsonify({
                'list_id': shoppinglist.list_id,
                'listname': shoppinglist.listname
                })
            response.status_code = 201
            return response
    else:
        shoppinglists = ShoppingList.get_all()
        results = []
        for shoppinglist in shoppinglists:
            obj = {
                'list_id': shoppinglist.list_id,
                'listname': shoppinglist.listname
                }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

@app.route('/shoppingitems/', methods=['POST', 'GET'])
def shoppingitems():
    if request.method == "POST":
        itemname = str(request.data.get('itemname'))
        quantity = int(request.data.get('quantity'))
        price = int(request.data.get('price'))
        if itemname:
            shoppingitem = ShoppingItems(itemname=itemname, quantity=quantity, price=price)
            shoppingitem.save()
            response = jsonify({
                'item_id' : shoppingitem.item_id,
                'itemname' : shoppingitem.itemname,
                'quantity' : shoppingitem.quantity,
                'price' : shoppingitem.price 
                })
            response.status_code = 201
            return response
    else:
        shoppingitems = ShoppingItems.get_all()
        results = []
        for shoppingitem in shoppingitems:
            obj = {
                'item_id' : shoppingitem.item_id,
                'itemname' : shoppingitem.itemname,
                'quantity' : shoppingitem.quantity,
                'price' : shoppingitem.price
                }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response