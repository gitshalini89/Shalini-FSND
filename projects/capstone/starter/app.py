import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import setup_db, Actors, Movies
from auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(*args, **kwargs):
    try:
        actor = Actors.query.order_by(Actors.id).all()
        actors = [d.format() for d in actor]

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': actors
        })

    except AttributeError:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actors')
def get_actors_by_id(*args, **kwargs):

    u_id = kwargs['actor_id']

    try:
        actors = Actors.query.filter(Actors.id == u_id).one_or_none()
        
        if actors is None:
            abort(404)

        return jsonify({
            'success': True,
            'actors': actors
        })

    except AttributeError:
        abort(422)


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(*args, **kwargs):
    try:
        movie = Movies.query.order_by(Movies.id).all()
        movies = [d.format() for d in movie]

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': movies
        })

    except AttributeError:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['GET'])
@requires_auth('get:movies')
def get_movies_by_id(*args, **kwargs):

    u_id = kwargs['movie_id']

    try:
        movies = Movies.query.filter(Movies.id == u_id).one_or_none()

        if movies is None:
            abort(404)

        return jsonify({
            'success': True,
            'movies': movies
        })

    except AttributeError:
        abort(422)


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actors(*args, **kwargs):
    try:
        body = request.get_json()
        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')

        actors = Actors(name=new_name, age=new_age, gender=new_gender)
        actors.insert()

        return jsonify({
            "success": True,
            "message": "Actor Successfully Added!",
            "actors": actors.format()
        })

    except AttributeError:
        abort(422)


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movies(*args, **kwargs):
    try:
        body = request.get_json()
        new_title = body.get('title')
        new_releasedate = body.get('releasedate')

        movies = Movies(title=new_title, releasedate=new_releasedate)
        movies.insert()

        return jsonify({
            "success": True,
            "message": "Movie Successfully Added!",
            "movies": movies.format()
        })

    except AttributeError:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actors(*args, **kwargs):

    u_id = kwargs['actor_id']

    try:
        actors = Actors.query.filter(Actors.id == u_id).one_or_none()

        if actors is None:
            abort(404)

        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if new_name is not None:
            actors.name = new_name

        if new_age is not None:
            actors.age = new_age

        if new_gender is not None:
            actors.gender = new_gender

        actors.update()

        return jsonify({
            "success": True,
            "message": "Actor details successfully updated!",
            "actors": [actors.format()],
            "modified_actor_id": u_id
        })

    except AttributeError:
        abort(422)


@app.route('/movies/<int:movies_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movies(*args, **kwargs):

    u_id = kwargs['movies_id']

    try:
        movies = Movies.query.filter(Movies.id == u_id).one_or_none()

        if movies is None:
            abort(404)

        body = request.get_json()

        new_title = body.get('title', None)
        new_releasedate = body.get('releasedate', None)

        if new_title is not None:
            movies.title = new_title

        if new_releasedate is not None:
            movies.releasedate = new_releasedate

        movies.update()

        return jsonify({
            "success": True,
            "message": "Movie successfully updated!",
            "movies": [movies.format()],
            "modified_movie_id": u_id
        })

    except AttributeError:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(*args, **kwargs):

    d_id = kwargs['actor_id']

    try:
        actors = Actors.query.filter(Actors.id == d_id).one_or_none()

        if actors is None:
            abort(404)

        actors.delete()

        return jsonify({
            "success": True,
            "message": "Actor successfully deleted!",
            "deleted_actor_id": d_id
        })

    except AttributeError:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(*args, **kwargs):

    d_id = kwargs['movie_id']

    try:
        movies = Movies.query.filter(Movies.id == d_id).one_or_none()

        if movies is None:
            abort(404)

        movies.delete()

        return jsonify({
            "success": True,
            "message": "Movie successfully deleted!",
            "deleted_movie_id": d_id
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


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
