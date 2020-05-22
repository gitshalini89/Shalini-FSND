import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app

from database.models import setup_db, Actors, Movies
from auth import AuthError, requires_auth

class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".\
            format('udacity:admin@localhost:5433', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'lithika',
            'age': 10,
            'gender': 'female'
        }

        self.new_movie = {
            'title': 'Frozen II',
            'releasedate': '12-06-2019'
        }

        self.update_actor = {
            'name': 'Sam'
        }

        self.udpate_movie = {
            'title': 'Cars'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_actors(self):

        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):

        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_actors_by_id(self):

        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_movies_by_id(self):

        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_get_actors_by_id(self):

        res = self.client().get('/actors/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')

    def test_404_get_movies_by_id(self):

        res = self.client().get('/movies/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')

    def test_delete_actors(self):

        res = self.client().delete('/actors/5')
        data = json.loads(res.data)

        actors = Actors.query.filter(Actors.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actors, None)

    def test_422_delete_actors_not_exist(self):

        res = self.client().delete('/actors/;;;')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

    def test_create_actors(self):

        res = self.client().post('/actors', json=self.new_actors)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_create_actors_not_allowed(self):

        res = self.client().post('/actors/100', json=self.new_actors)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'method not allowed')

    def test_delete_movies(self):

        res = self.client().delete('/movies/5')
        data = json.loads(res.data)

        movies = Movies.query.filter(Movies.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movies, None)

    def test_422_delete_movies_not_exist(self):

        res = self.client().delete('/movies/;;;')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

    def test_create_movies(self):

        res = self.client().post('/movies', json=self.new_movies)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_create_movies_not_allowed(self):

        res = self.client().post('/movies/100', json=self.new_movies)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'method not allowed')

    def test_update_actors(self):

        res = self.client().patch('/actors/1', json=self.update_actors)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_update_actors(self):

        res = self.client().patch('/actors/100', json=self.update_actors)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')

    def test_update_movies(self):

        res = self.client().patch('/movies/1', json=self.update_movies)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_update_movies(self):

        res = self.client().patch('/movies/100', json=self.update_movies)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')


if __name__ == "__main__":
    unittest.main()
