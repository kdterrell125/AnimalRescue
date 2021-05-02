import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db_drop_and_create_all, Shelter, Animal
from auth.auth import requires_auth, AuthError


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    db_drop_and_create_all()

    CORS(app, resources={r"/*": {"origins": "*"}})

    # @app.after_request
    # def after_request(response):
    #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,
    #                           Authorization,true')
    #     response.headers.add('Access-Control-Allow-methods','GET, POST,
    #                           PATCH, DELETE, OPTIONS')
    #     return response

    @app.route('/')
    def health():
        return jsonify({
            'health': 'Running!'
        }), 200

    @app.route('/shelters', methods=['GET'])
    def get_shelters():
        shelters = Shelter.query.all()
        # formatted_shelters ={}
        # for shelter in shelters:
        #     formatted_shelters[shelter.id] = shelter.id
        formatted_shelters = [shelter.format() for shelter in shelters]

        return jsonify({
            'success': True,
            'shelters': formatted_shelters
        }), 200

    @app.route('/animals', methods=['GET'])
    def get_movies():
        animals = Animal.query.all()
        formatted_animals = [animal.format() for animal in animals]

        return jsonify({
            'success': True,
            'animals': formatted_animals
        }), 200

    @app.route('/shelters/<int:shelter_id>/animals', methods=['GET'])
    def get_specific_shelter_animals(shelter_id):
        shelter = Shelter.query.get(shelter_id)
        animals = Animal.query.filter(Animal.shelter_id == shelter_id).all()

        if len(animals) == 0:
            abort(404)

        formatted_animals = [animal.format() for animal in animals]
        formatted_shelters = shelter.format()

        return jsonify({
            'success': True,
            'animals': formatted_animals,
            'total_animals': len(animals),
            'shelters': formatted_shelters,
            'current_shelter': shelter_id
        }), 200

    @app.route('/shelters/<int:shelter_id>', methods=['DELETE'])
    @requires_auth('delete:shelters')
    def delete_shelter(payload, shelter_id):
        shelter = Shelter.query.get(shelter_id)

        if shelter is None:
            abort(400)

        shelter.delete()

        return jsonify({
            'success': True,
            'message': "Shelter deleted",
            'deleted': shelter_id
        }), 200

    @app.route('/animals/<int:animal_id>', methods=['DELETE'])
    @requires_auth('delete:animals')
    def delete_animal(payload, animal_id):
        animal = Animal.query.get(animal_id)

        if animal is None:
            abort(400)

        animal.delete()

        return jsonify({
            'success': True,
            'message': "Animal deleted",
            'deleted': animal_id
        }), 200

    @app.route('/shelters', methods=['POST'])
    @requires_auth('post:shelters')
    def post_shelter(payload):

        try:
            data = request.get_json()

            name = data.get('name')
            city = data.get('city')
            state = data.get('state')
            address = data.get('address')

            if ((name == '') or (city == '') or
                    (state == '') or (address =='')):
                abort(422)

            shelter = Shelter(
                name=name,
                city=city,
                state=state,
                address=address
            )
            shelter.insert()
        except BaseException as e:
            print(e)
            abort(422)

        formatted_shelters = [shelter.format()]

        return jsonify({
            'success': True,
            'shelters': formatted_shelters
        }), 200

    @app.route('/animals', methods=['POST'])
    @requires_auth('post:animals')
    def post_animal(payload):

        try:
            data = request.get_json()

            name = data.get('name')
            gender = data.get('gender')
            age = data.get('age')
            species = data.get('species')
            breed = data.get('breed')
            shelter_id = data.get('shelter_id')

            if ((name == '') or (species == '') or
                    (breed == '')):
                abort(422)

            animal = Animal(
                name=name,
                gender=gender,
                age=age,
                species=species,
                breed=breed,
                shelter_id=shelter_id
            )
            animal.insert()
        except BaseException as e:
            print(e)
            abort(422)

        formatted_animals = [animal.format()]

        return jsonify({
            'success': True,
            'animals': formatted_animals
        }), 200

    @app.route('/shelters/<int:shelter_id>', methods=['PATCH'])
    @requires_auth('patch:shelters')
    def update_shelter(payload, shelter_id):
        updated_shelter = Shelter.query.get(shelter_id)

        if updated_shelter is None:
            abort(404)

        try:
            data = request.get_json()

            update_name = data.get('name', None)
            update_city = data.get('city', None)
            update_state = data.get('state', None)
            update_address = data.get('address', None)

            if update_name:
                updated_shelter.name = update_name
            if update_city:
                updated_shelter.city = update_city
            if update_state:
                updated_shelter.state = update_state
            if update_address:
                updated_shelter.address = update_address

            updated_shelter.update()
        except BaseException as e:
            print(e)
            abort(422)

        formatted_shelters = [updated_shelter.format()]

        return jsonify({
            'success': True,
            'shelters': formatted_shelters
            }), 200

    @app.route('/animals/<int:animal_id>', methods=['PATCH'])
    @requires_auth('patch:animals')
    def update_animal(payload, animal_id):
        updated_animal = Animal.query.get(animal_id)

        if updated_animal is None:
            abort(404)

        try:
            data = request.get_json()

            update_name = data.get('name', None)
            update_gender = data.get('gender', None)
            update_age = data.get('age', None)
            update_species = data.get('species', None)
            update_breed = data.get('breed', None)
            update_shelter_id = data.get('shelter_id', None)

            if update_name:
                updated_animal.name = update_name
            if update_gender:
                updated_animal.gender = update_gender
            if update_age:
                updated_animal.age = update_age
            if update_species:
                updated_animal.species = update_species
            if update_breed:
                updated_animal.breed = update_breed
            if update_shelter_id:
                updated_animal.shelter_id = update_shelter_id

            updated_animal.update()
        except BaseException as e:
            print(e)
            abort(422)

        formatted_animals = [updated_animal.format()]

        return jsonify({
            'success': True,
            'animals': formatted_animals
        }), 200

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response
        
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
