#  /app/home/views.py
import json
import requests
import re

from flask import request, jsonify, abort, url_for
from app.models import User, ShoppingList, ShoppingItems

from . import home
from . import home as home_blueprint

@home.route('/home/shoppinglists', methods=['POST', 'GET', 'DELETE'])
def shoppinglists():
    """ API that GET and POST shopping lists. """

    #Pagination arguments: Setting page to 1, then min_per_page to 20 and max_per_page to 100
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    limit = limit if limit <= 20 else 20

    #Token retrival
    auth_header = request.headers.get('Authorization', None)

    if not auth_header:
        response = jsonify({
            'message':
            'No token provided!'})
        response.status_code = 500
        return response
    else:
        token = auth_header.split(" ")
        access_token = token[1]
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                if request.method == "POST":
                    listname = str(request.data["listname"])
                    if not re.match(r"(?=^.{3,}$)^[A-Za-z0-9_-]+( +[A-Za-z0-9_-]+)*$", listname):
                        response = jsonify(
                            {'message':'listname should contain letters, digits and with a min length of 3'}
                        )
                        response.status_code = 400
                        return response
                    if not listname:
                        return {'mesaage': 'No input provided'}, 400
                    else:
                        list_exists = ShoppingList.query.filter_by(created_by=user_id).filter_by(listname=listname).first()
                        if list_exists:
                            return {
                                    'message':
                                    'shoppinglist with that name already exists.'
                                    }, 409        
                        else:
                            shoppinglist = ShoppingList(listname=listname, created_by=user_id)
                            shoppinglist.save()
                            response = jsonify({
                                'list_id': shoppinglist.list_id,
                                'listname': shoppinglist.listname,
                                'created_by': shoppinglist.created_by
                                })
                            return {'message':'shoppinglist with name {} successfully created'.format(
                                    shoppinglist.listname)}, 201

                elif request.method == "GET":
                    results = []
                    q = request.args.get('q')
                    if q:
                        shopping_lists = ShoppingList.query.filter_by(
                            created_by=user_id).filter(ShoppingList.listname.like('%{0}%'.format(q)))
                    else:
                        shopping_lists = ShoppingList.query.filter_by(created_by=user_id)
                    
                    if shopping_lists:
                        pagination = shopping_lists.paginate(page, per_page=limit, error_out=False)
                        shop_lists = pagination.items
                        if pagination.has_prev:
                            prev = url_for('home.shoppinglists', page=page-1, limit= limit, _external=True)
                        else:
                            prev = None
                        if pagination.has_next:
                            next = url_for('home.shoppinglists', page=page+1, limit=limit, _external=True)
                        else:
                            next = None
                        if shop_lists:
                            for shoppinglist in shop_lists:
                                obj = {
                                    'list_id': shoppinglist.list_id,
                                    'listname': shoppinglist.listname
                                    }
                                results.append(obj)
                            response = jsonify({
                                'shoppinglists': results,
                                'prev': prev,
                                'next': next,
                                'count': pagination.total
                                })
                            response.status_code = 200
                            return response
                        else:
                            return {'message':'No shopping lists to display'}, 404            
                else:
                    shopping_lists = ShoppingList.query.filter_by(created_by=user_id)
                    for item in shopping_lists:
                        item.delete()
                    response = jsonify({
                        'message':
                        'All shopping lists successfully deleted'})
                    response.status_code = 200
                    return response
            else:
                response = jsonify({'message':user_id})
                response.status_code = 401
                return response

@home.route('/home/shoppinglists/<list_id>', methods=['GET', 'PUT', 'DELETE'])
def shoppinglists_management(list_id):
    """ API that GET, PUT and DELETE a shopping list. """

    #Token retrival
    auth_header = request.headers.get('Authorization', None)

    if not auth_header:
        response = jsonify({
            'message':
            'No token provided!'})
        response.status_code = 500
        return response
    else:
        token = auth_header.split(" ")
        access_token = token[1]
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                shoppinglist = ShoppingList.query.filter_by(created_by=user_id).filter_by(list_id=list_id).first()
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
                        shopping_lists = ShoppingList.query.filter_by(created_by=user_id)
                        for item in shopping_lists:
                            if item.listname == listname:
                                return {'message':'There exists a shopping list with such a name'}, 409
                            else:
                                shoppinglist.listname = listname
                                shoppinglist.save()
                                response = jsonify({
                                    'list_id': shoppinglist.list_id,
                                    'listname': shoppinglist.listname
                                })
                                return {'message':'shoppinglist with id {} successfully edited. '.format(shoppinglist.list_id)}, 200
                    else:
                        shoppinglist.delete()
                        return {'message':'Shoppinglist with id {} successfully deleted'.format(shoppinglist.list_id)}, 200
                else:
                    return {'messsage': 'No shopping with that id'}, 404
            else:
                response = jsonify({'message':user_id})
                response.status_code = 401
                return response

@home.route('/home/shoppinglists/<list_id>/shoppingitems', methods=['POST', 'GET', 'DELETE'])
def shoppingitems(list_id):
    """ API that GET and POST items from/to a shopping list. """

    #Pagination arguments: Setting page to 1, then min_per_page to 20 and max_per_page to 100
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    limit = limit if limit <= 20 else 20

    #Token retrival
    auth_header = request.headers.get('Authorization', None)

    if not auth_header:
        response = jsonify({
            'message':
            'No token provided!'})
        response.status_code = 500
        return response
    else:
        token = auth_header.split(" ")
        access_token = token[1]
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):

                #Get list to work on by id
                shoppinglist = ShoppingList.query.filter_by(list_id=list_id).first()
                if shoppinglist:
                    if request.method == "POST":
                        itemname = request.data.get('itemname')
                        quantity = request.data.get('quantity')
                        price = request.data.get('price')
                        
                        if itemname and quantity and price:
                            if not re.match(r"(?=^.{3,}$)^[A-Za-z0-9_-]+( +[A-Za-z0-9_-]+)*$", itemname):
                                response = jsonify({
                                                'message':
                                                'itemname should contain letters, digits and with a min length of 3'
                                                })
                                response.status_code = 400
                                return response
                            if not re.match(r"(?=^.{1,}$)^[A-Za-z0-9_-]+( +[A-Za-z0-9_-]+)*$", quantity):
                                response = jsonify({
                                                'message':
                                                'Quantity should contain letters, digits and spaces'
                                                })
                                response.status_code = 400
                                return response
                            if not re.match(r"^[0-9.]+$", price):
                                response = jsonify({
                                                'message':
                                                'price should number with or without decimals'
                                                })
                                response.status_code = 400
                                return response

                            item = ShoppingItems.query.filter_by(item_for_list=list_id).filter_by(itemname=itemname).first()
                            if item:
                                return {
                                        'message':
                                        'shoppingitem with that name already exists.'
                                        }, 409 
                            else:
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
                                return {
                                        'message':
                                        'shoppingitem with itemname {} successfully created. '
                                        .format(shoppingitem.itemname)}, 201
                        else:
                            if not itemname:
                                return {'mesaage': 'No itemname provided'}, 400 
                            elif not quantity:
                                return {'mesaage': 'If there is no quantity to provided, key in 0'}, 400 
                            else:
                                return {'mesaage': 'If there is no price to provided, key in 0'}, 400 
                                
                    elif request.method == "GET": 
                        results = []
                        q = request.args.get('q')
                        if q:
                            shopping_items = ShoppingItems.query.filter_by(
                                item_for_list=list_id).filter(ShoppingItems.itemname.like('%{0}%'.format(q)))
                        else:
                            shopping_items = ShoppingItems.query.filter_by(item_for_list=list_id)

                        if shopping_items:
                            pagination = shopping_items.paginate(page, per_page=limit, error_out=False)
                            shop_items = pagination.items
                            if pagination.has_prev:
                                prev = url_for('home.shoppingitems', list_id=list_id, page=page-1, limit= limit, _external=True)
                            else:
                                prev = None
                            if pagination.has_next:
                                next = url_for('home.shoppingitems', list_id=list_id, page=page+1, limit=limit, _external=True)
                            else:
                                next = None

                            for shoppingitem in shop_items:
                                obj = {
                                    'item_id' : shoppingitem.item_id,
                                    'itemname' : shoppingitem.itemname,
                                    'quantity' : shoppingitem.quantity,
                                    'price' : shoppingitem.price
                                    }
                                results.append(obj)
                            response = jsonify({
                                    'shoppingitems': results,
                                    'prev': prev,
                                    'next': next,
                                    'count': pagination.total
                                    })
                            response.status_code = 200
                            return response
                        else:
                            return {'message':'No items to display'}, 404
                    else:
                        shopping_items = ShoppingItems.query.filter_by(item_for_list=list_id)
                        for item in shopping_items:
                            item.delete()
                        response = jsonify({
                            'message':
                            'All shopping items successfully deleted'})
                        response.status_code = 200
                        return response
                else:
                    response = jsonify({
                            'message':
                            'There is no shopping list with that id to add items to'})
                    response.status_code = 404
                    return response
            else:
                response = jsonify({'message':user_id})
                response.status_code = 401
                return response

@home.route('/home/shoppinglists/<list_id>/shoppingitems/<item_id>', methods=['GET', 'PUT', 'DELETE'])
def shoppingitems_management(list_id, item_id):
    """ API that GET, PUT and DELETE items from/to a shopping list. """

    #Token retrival
    auth_header = request.headers.get('Authorization', None)

    if not auth_header:
        response = jsonify({
            'message':
            'No token provided!'})
        response.status_code = 500
        return response
    else:
        token = auth_header.split(" ")
        access_token = token[1]
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                shoppinglist = ShoppingList.query.filter_by(created_by=user_id).filter_by(list_id=list_id).first()
                if shoppinglist:
                    shoppingitem = ShoppingItems.query.filter_by(item_for_list=list_id).filter_by(item_id=item_id).first()
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
                            itemname = request.data.get('itemname')
                            quantity = request.data.get('quantity')
                            price = request.data.get('price')
                            item = ShoppingItems.query.filter_by(item_for_list=list_id).filter_by(itemname=itemname).first()
                            if item:
                                return {
                                        'message':
                                        'shoppingitem with that name already exists.'
                                        }, 409 
                            else:
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
                                return {
                                        'message':
                                        'shoppingitem with id {} successfully edited. '
                                        .format(shoppingitem.item_id)}, 200
                        else:
                            shoppingitem.delete()
                            return {'message':'shoppingitem with id {} successfully deleted'.format(shoppingitem.item_id)}, 200
                    else:
                        return {'message':'Item with that id does not exist'}, 404  
                else:
                    abort(404)
            else:
                response = jsonify({'message':user_id})
                response.status_code = 401
                return response