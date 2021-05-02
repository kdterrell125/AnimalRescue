import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all, Shelter, Animal
from auth.auth import requires_auth, AuthError
from dotenv import load_dotenv
load_dotenv('.env')

domain_admin_token = os.environ.get('domain_admin_token')
shelter_manager_token = os.environ.get('shelter_manager_token')
animal_specialist_token = os.environ.get('animal_specialist_token')


class AnimalRescueTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = 'postgresql://postgres:kandis@localhost:5432/'
        'capstone'
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

            self.new_shelter_success = {
                'name': 'Humane Society of the Bay',
                'city': 'Vallejo',
                'state': 'California',
                'address': '400 Sacramento Street'
            }
            self.new_shelter_failure = {
                'name': '',
                'city': 'Sacramento',
                'state': 'California',
                'address': '900 Lincoln Avenue'
            }
            self.new_animal_success = {
                'name': 'Sadie',
                'gender': 'female',
                'age': 6,
                'species': 'cat',
                'breed': 'siamese',
                'shelter_id': 6
            }
            self.new_animal_failure = {
                'name': 'Alabaster',
                'gender': '',
                'age': 8,
                'species': '',
                'breed': 'german shepherd',
                'shelter_id': 7
            }
            self.patch_shelter = {
                'name': 'Hopalong Rescue'
            }
            self.patch_animal = {
                'species': 'horse'
            }

    def tearDown(self):
        pass

    # Test Shelters

    def test_get_shelters_success(self):
        res = self.client().get('/shelters')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['shelters'])

    # Test Animals

    def test_get_animals_success(self):
        res = self.client().get('/animals')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animals'])

    # Test Get Animals By Specific Shelter

    def test_get_specific_shelter_animals_success(self):
        res = self.client().get('/shelters/6/animals')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animals'])
        self.assertTrue(len(data['animals']))
        self.assertTrue(data['shelters'])

    def test_get_specific_shelter_animals_failure(self):
        res = self.client().get('/shelters/15/animals')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    # Test Create New Shelter

    def test_create_new_shelter_success(self):
        res = self.client().post(
                                '/shelters',
                                headers={'Authorization':
                                         "Bearer {}".format
                                         (domain_admin_token)},
                                json=self.new_shelter_success
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['shelters'])

    def test_create_new_shelter_failure(self):
        res = self.client().post(
                                '/shelters',
                                headers={'Authorization':
                                         "Bearer {}".format
                                         (domain_admin_token)},
                                json=self.new_shelter_failure
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    # Test Create New Animal

    def test_create_new_animal_success(self):
        res = self.client().post(
                                '/animals',
                                headers={'Authorization':
                                         "Bearer {}".format
                                         (shelter_manager_token)},
                                json=self.new_animal_success
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animals'])

    def test_create_new_animal_failure(self):
        res = self.client().post(
                                '/animals',
                                headers={'Authorization':
                                         "Bearer {}".format
                                         (shelter_manager_token)},
                                json=self.new_animal_failure
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    # Test Delete Shelter

    def test_delete_shelter_success(self):
        res = self.client().delete(
                                  '/shelters/9',
                                  headers={'Authorization':
                                           "Bearer {}".format
                                           (domain_admin_token)}
                                    )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_shelter_failure(self):
        res = self.client().delete(
                                  '/shelters/17',
                                  headers={'Authorization':
                                           "Bearer {}".format
                                           (domain_admin_token)}
                                    )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Bad request')

    # Test Delete Animal

    def test_delete_animal_success(self):
        res = self.client().delete(
                                  '/animals/12',
                                  headers={'Authorization':
                                           "Bearer {}".format
                                           (shelter_manager_token)}
                                    )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_shelter_failure(self):
        res = self.client().delete(
                                  '/animals/17',
                                  headers={'Authorization':
                                           "Bearer {}".format
                                           (shelter_manager_token)}
                                    )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Bad request')

    # Test Patch Shelter

    def test_patch_shelter_success(self):
        res = self.client().patch(
                                 '/shelters/1',
                                 headers={'Authorization':
                                          "Bearer {}".format
                                          (shelter_manager_token)},
                                 json=self.patch_shelter
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['shelters'])

    def test_patch_shelter_failure(self):
        res = self.client().patch(
                                 '/shelters/1',
                                 headers={'Authorization':
                                          "Bearer {}".format
                                          (animal_specialist_token)},
                                 json=self.patch_shelter
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test Patch Animal

    def test_patch_animal_success(self):
        res = self.client().patch(
                                 '/animals/8',
                                 headers={'Authorization':
                                          "Bearer {}".format
                                          (animal_specialist_token)},
                                 json=self.patch_animal
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['animals'])

    def test_patch_animal_failure(self):
        res = self.client().patch(
                                 '/animals/8',
                                 headers={'Authorization':
                                          "Bearer {}".format
                                          (shelter_manager_token)},
                                 json=self.patch_animal
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

if __name__ == "__main__":
    unittest.main()
