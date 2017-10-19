#  /app/home/views.py
from . import home
from . import home as home_blueprint
from flask import request, jsonify, abort
from app.models import ShoppingList, ShoppingItems

@home.route('/home/shoppinglists/', methods=['POST', 'GET'])
def shoppinglists():
    """ API that GET and POST shopping lists. """

    if request.method == "POST":
        listname = str(request.data.get('listname'))
        shoppinglist = ShoppingList.query.filter_by(listname=listname).first()
        if not shoppinglist:
            if listname:
                shoppinglist = ShoppingList(listname=listname)
                shoppinglist.save()
                response = jsonify({
                    'list_id': shoppinglist.list_id,
                    'listname': shoppinglist.listname
                    })
                return {'message':'shoppinglist with name {}\
                                    successfully created'.format(shoppinglist.listname)}, 201
        else:
            return {'message': 'shoppinglist with that name {} already exists.'.format(shoppinglist.listname)}, 404
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

@home.route('/home/shoppinglists/<list_id>', methods=['GET', 'PUT', 'DELETE'])
def shoppinglists_management(list_id):
    """ API that GET, PUT and DELETE a shopping list. """

    shoppinglist = ShoppingList.query.filter_by(list_id=list_id).first()
    if shoppinglist:
        if request.method == "GET":
            response = jsonify({
                'list_id': shoppinglist.list_id,
                'listname': shoppinglist.listname
            })
            response.status_code = 200
            return response
        elif request.method == "PUT":
            listname = str(request.data.get('listname'))
            shoppinglist.listname = listname
            shoppinglist.save()
            response = jsonify({
                'list_id': shoppinglist.list_id,
                'listname': shoppinglist.listname
            })
            return {'message':'shoppinglist with id {} successfully edited. '.format(shoppinglist.list_id)}, 200
        else:
            shoppinglist.delete()
            return {'message':'{} shoppinglist successfully deleted'.format(shoppinglist.listname)}, 200
    else:
        abort(404)

@home.route('/home/shoppinglists/<list_id>/shoppingitems/', methods=['POST', 'GET'])
def shoppingitems(list_id):
    """ API that GET and POST items from/to a shopping list. """

    shoppinglist = ShoppingList.query.filter_by(list_id=list_id).first()
    if shoppinglist:
        if request.method == "POST":
            itemname = str(request.data.get('itemname'))
            quantity = int(request.data.get('quantity'))
            price = int(request.data.get('price'))
            shoppingitem = ShoppingItems.query.filter_by(itemname=itemname).first()
            if not shoppingitem:
                if itemname:
                    shoppingitem = ShoppingItems(
                        itemname=itemname,
                        quantity=quantity,
                        price=price)
                    shoppingitem.save()
                    response = jsonify({
                        'item_id' : shoppingitem.item_id,
                        'itemname' : shoppingitem.itemname,
                        'quantity' : shoppingitem.quantity,
                        'price' : shoppingitem.price
                        })
                    return {'message':'shoppingitem with itemname {} successfully created. '.format(shoppingitem.itemname)}, 201
            else:
                return {'message': 'shoppingitem with that name {}\
                                    already exists in this shopping list.'
                                    .format(shoppingitem.itemname)}, 404
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
    else:
        abort(404)

@home.route('/home/shoppinglists/<list_id>/shoppingitems/<item_id>', methods=['GET', 'PUT', 'DELETE'])
def shoppingitems_management(list_id, item_id):
    """ API that GET, PUT and DELETE items from/to a shopping list. """

    shoppinglist = ShoppingList.query.filter_by(list_id=list_id).first()
    if shoppinglist:
        shoppingitem = ShoppingItems.query.filter_by(item_id=item_id).first()
        if shoppingitem:
            if request.method == 'GET':
                response = jsonify({
                    'item_id': shoppingitem.item_id,
                    'itemname': shoppingitem.itemname,
                    'quantity': shoppingitem.quantity,
                    'price': shoppingitem.price
                })
                response.status_code = 200
                return response
            elif request.method == 'PUT':
                itemname = str(request.data.get('itemname'))
                quantity = int(request.data.get('quantity'))
                price = int(request.data.get('price'))
                shoppingitem.itemname = itemname
                shoppingitem.quantity = quantity
                shoppingitem.price = price
                shoppingitem.save()
                response = jsonify({
                    'item_id' : shoppingitem.item_id,
                    'itemname' : shoppingitem.itemname,
                    'quantity' : shoppingitem.quantity,
                    'price' : shoppingitem.price
                })
                return {'message':'shoppingitem with id {} successfully edited. '.format(shoppingitem.item_id)}, 200
            else:
                shoppingitem.delete()
                return {'message':'shoppingitem with id {} successfully deleted'.format(shoppingitem.item_id)}, 200
        else:
            abort(404)  
    else:
        abort(404)
