#  /app/home/views.py
import json
import requests

from flask import request, jsonify, abort
from app.models import User, ShoppingList, ShoppingItems

from . import home
from . import home as home_blueprint

@home.route('/home/shoppinglists/', methods=['POST', 'GET'])
def shoppinglists():
    """ API that GET and POST shopping lists. """

    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")
    access_token = token[1]
    if access_token:
        user_id = User.decode_auth_token(access_token)
        if not isinstance(user_id, str):
            if request.method == "POST":
                listname = str(request.data["listname"])
                shoppinglist = ShoppingList.query.filter_by(listname=listname).first()
                if not shoppinglist:
                    shoppinglist = ShoppingList(listname=listname, created_by=user_id)
                    shoppinglist.save()
                    response = jsonify({
                        'list_id': shoppinglist.list_id,
                        'listname': shoppinglist.listname,
                        'created_by': shoppinglist.created_by
                        })
                    return {'message':'shoppinglist with name {}\
                                        successfully created'.format(shoppinglist.listname)}, 201
                else:
                    return {'message':
                            'shoppinglist with that name {} already exists.'
                            .format(shoppinglist.listname)}, 404
            else:
                results = []
                q = request.args.get('q')
                if q:
                    shopping_lists = ShoppingList.query.filter_by(
                        created_by=user_id).filter(ShoppingList.listname.like('%{0}%'.format(q)))
                else:
                    shopping_lists = ShoppingList.query.filter_by(created_by=user_id)
                for shoppinglist in shopping_lists:
                    obj = {
                        'list_id': shoppinglist.list_id,
                        'listname': shoppinglist.listname
                        }
                    results.append(obj)
                response = jsonify(results)
                response.status_code = 200
                return response
        else:
            response = jsonify({'message':user_id})
            response.status_code = 401
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
            return {'message':'Shoppinglist with id: {} successfully deleted'.format(shoppinglist.list_id)}, 200
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
                shoppingitem = ShoppingItems(
                    itemname=itemname,
                    quantity=quantity,
                    price=price,
                    item_for_list=list_id
                    )
                shoppingitem.save()
                response = jsonify({
                    'item_id' : shoppingitem.item_id,
                    'itemname' : shoppingitem.itemname,
                    'quantity' : shoppingitem.quantity,
                    'price' : shoppingitem.price,
                    'item_for_list': shoppingitem.item_for_list
                    })
                return {'message':'shoppingitem with itemname {} successfully created. '.format(shoppingitem.itemname)}, 201
            else:
                return {'message': 'shoppingitem with that name {}\
                                    already exists in this shopping list.'
                                    .format(shoppingitem.itemname)}, 404
        else: 
            results = []
            q = request.args.get('q')
            if q:
                shopping_items = ShoppingItems.query.filter_by(
                    item_for_list=list_id).filter(ShoppingItems.itemname.like('%{0}%'.format(q)))
            else:
                shopping_items = ShoppingItems.query.filter_by(item_for_list=list_id)

            for shoppingitem in shopping_items:
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
