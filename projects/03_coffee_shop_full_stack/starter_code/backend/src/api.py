import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
def get_drinks_public(*args, **kwargs):
    try:
        drink = Drink.query.order_by(Drink.id).all()
        drinks = [d.short() for d in drink]

        if len(drinks) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'drinks': drinks
        })

    except AttributeError:
        abort(422)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(*args, **kwargs):
    try:
        drink = Drink.query.order_by(Drink.id).all()
        drinks = [d.long() for d in drink]

        if len(drinks) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'drinks': drinks
        })

    except AttributeError:
        abort(422)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(*args, **kwargs):
    try:
        body = request.get_json()
        new_title = body.get('title')
        new_recipe = body.get('recipe')

        drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        drink.insert()

        return jsonify({
            "success": True,
            "drinks": drink.long()
        })

    except AttributeError:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(*args, **kwargs):

    u_id = kwargs['drink_id']

    try:
        drink = Drink.query.filter(Drink.id == u_id).one_or_none()

        if drink is None:
            abort(404)

        body = request.get_json()

        drink.title = body.get('title', None)
        drink.recipe = json.dumps(body.get('recipe', None))
        drink.update()

        return jsonify({
            "success": True,
            "drinks": [drink.long()],
            "modified_drink_id": u_id
        })

    except AttributeError:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(*args, **kwargs):

    d_id = kwargs['drink_id']

    try:
        drink = Drink.query.filter(Drink.id == d_id).one_or_none()

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            "success": True,
            "delete": d_id
        })

    except AttributeError:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    })


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    })


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'forbidden'
    })


@app.errorhandler(AuthError)
def error_auth(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
