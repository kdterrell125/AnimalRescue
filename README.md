# Animal Rescue - Udacity Full Stack Web Development Capstone

Animal Rescue allows prospective adopters to go through shelters and available animals.  

This project was creaetd as a means to leverage all of the skills learned throughout Udacity's Full Stack Web Development course.

## Getting Started

### Installing Dependencies

Installation of Python3 and PIP are needed to use this project.

#### Python 3.7

Follow instructions to install the lastest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### PIP
Once you have your virtual environment setup and running, install dependencies by naviging to the `/UdacityCapstone` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

### Running the Server

#### Running the Server Locally

Open your terminal and navigate to the root directory.
To run the server, execute:

```
 export FLASK_APP=app
export FLASK_ENV=development
flask run 
```

## API Reference

This app is live hosted at: https://udacityanimalrescue.herokuapp.com/

### Authorization

Animal Rescue uses Auth0 (https://auth0.com/docs/) for role based authorization.  Three roles are responsible for maintaining the database:

    1. Domain Admin: Responsible maintaining all aspects of the database - adding/deleting    shelters and animals; updating both shelter and animal profiles
    ```
    email: kdterrell125@gmail.com
    password: kandisT125
    ```
    2. Shelter Manager: Responsible for updating shelter profiles and adding/deleting animals
    ```
    email: polarbearsrus@gmail.com
    password: kandisT125
    ```
    3. Animal Specialist: Responsible for updating animal profiles
    ```
    email: kdterrell@ucdavis.edu
    password: kandisT125
    ```
*** If tokens including in files are expired, please login to generate new ones.

### API Endpoints

#### GET /

* Returns "Greetings: Let's clear out the shelters!" if api is running properly
* curl https://udacityanimalrescue.herokuapp.com/
* curl http://127.0.0.1:5000/

```
{
    "Greetings": "Let's clear out the shelters!"
}
```

#### GET /shelters 

* Returns all shelters
* Does not require authorization
* curl https://udacityanimalrescue.herokuapp.com/shelters
* curl http://127.0.0.1:5000/shelters

```
{
  "shelters": [
    {
      "address": "300 L Street", 
      "city": "Antioch", 
      "id": 2, 
      "name": "Antioch Animal Services", 
      "phone": "925-779-6989", 
      "state": "CA"
    }, 
    {
      "address": "2253 Shafter Avenue", 
      "city": "San Francisco", 
      "id": 3, 
      "name": "Family Dog Rescue", 
      "phone": "", 
      "state": "CA"
    }, 
    {
      "address": "300 L Street", 
      "city": "Antioch", 
      "id": 1, 
      "name": "Antioch Animal Services", 
      "phone": null, 
      "state": "CA"
    }
  ], 
  "success": true, 
  "total_shelters": 3
}
```

#### GET /animals

* Returns all animals
* Does not require authorization
* curl https://udacityanimalrescue.herokuapp.com/animals
* curl http://127.0.0.1:5000/animals

```
{
  "animals": [
    {
      "age": 15, 
      "breed": "African Grey", 
      "gender": "male", 
      "id": 1, 
      "name": "Zik", 
      "shelter_id": 1, 
      "species": "bird"
    }, 
    {
      "age": 15, 
      "breed": "siamese", 
      "gender": "male", 
      "id": 2, 
      "name": "Zonk", 
      "shelter_id": 2, 
      "species": "cat"
    }, 
    {
      "age": 15, 
      "breed": "chihuahua", 
      "gender": "female", 
      "id": 3, 
      "name": "Mary Lou", 
      "shelter_id": 3, 
      "species": "dog"
    }, 
    {
      "age": 15, 
      "breed": "clydesdale", 
      "gender": "male", 
      "id": 4, 
      "name": "Dyno", 
      "shelter_id": 3, 
      "species": "horse"
    }
  ], 
  "success": true, 
  "total_animals": 4
}
```

#### GET /shelters/<int:shelter_id>/animals

* Returns all animals by specific shelter id
* Does not require authorization
* curl https://udacityanimalrescue.herokuapp.com/shelters/3/animals
* curl http://127.0.0.1:5000/shelters/3/animals

```
{
  "animals": [
    {
      "age": 15, 
      "breed": "chihuahua", 
      "gender": "female", 
      "id": 3, 
      "name": "Mary Lou", 
      "shelter_id": 3, 
      "species": "dog"
    }, 
    {
      "age": 15, 
      "breed": "clydesdale", 
      "gender": "male", 
      "id": 4, 
      "name": "Dyno", 
      "shelter_id": 3, 
      "species": "horse"
    }
  ], 
  "current_shelter": 3, 
  "shelters": {
    "address": "2253 Shafter Avenue", 
    "city": "San Francisco", 
    "id": 3, 
    "name": "Family Dog Rescue", 
    "phone": "", 
    "state": "CA"
  }, 
  "success": true, 
  "total_animals": 2
}
```

#### DELETE /shelters/<int:shelter_id>

* Deletes a specific shelter based upon the ID
* Role: Domain Admin
* Requires `delete:shelters`
* curl https://udacityanimalrescue.herokuapp.com/shelters/5 -X DELETE -H "Authorization: Bearer $domain_admin_token"
* curl http://121.0.0.1:5000/shelters/5 -X DELETE -H "Authorization: Bearer $domain_admin_token"

```
{
    "deleted":5,
    "message":"Shelter deleted",
    "success":true
}
```

#### DELETE /animals/<int:animal_id>

* Deletes a specific animal based upon the ID
* Role: Domain Admin or Shelter Manager
* Requires `delete:animals`
* curl https://udacityanimalrescue.herokuapp.com/animals/1 -X DELETE -H "Authorization: Bearer $shelter_manager_token"
* curl http://121.0.0.1:5000/animals/1 -X DELETE -H "Authorization: Bearer $shelter_manager_token"

```
{
    "deleted":1,
    "message":"Animal deleted",
    "success":true
}
```

#### POST /shelters

* Creates a new shelter
* Role: Domain Admin
* Requires `post:shelters`
* curl https://udacityanimalrescue.herokuapp.com/shelters -X POST -H "Authorization: Bearer $domain_admin_token" -H "Content-Type: application/json" -d '{"name": "Rocket Dog Rescue", "city": "Oakland", "state": "CA", "address": "3561 Foothil Boulevard", "phone": "415-756-8188"}'
* curl http://121.0.0.1:5000/shelters -X POST -H "Authorization: Bearer $domain_admin_token" -H "Content-Type: application/json" -d '{"name": "Rocket Dog Rescue", "city": "Oakland", "state": "CA", "address": "3561 Foothil Boulevard", "phone": "415-756-8188"}'

```
{
    "shelters":[
        {
        "address":"3561 Foothil Boulevard",
        "city":"Oakland","id":6,
        "name":"Rocket Dog Rescue",
        "phone":"415-756-8188",
        "state":"CA"
        }
    ],
    "success":true
}
```

#### POST /animals

* Creates a new animal
* Role Domain Admin or Shelter Manager
* Requires `post:animals`
* curl https://udacityanimalrescue.herokuapp.com/animals -X POST -H "Authorization: Bearer $shelter_manager_token" -H "Content-Type: application/json" -d '{"name": "Fab", "gender": "female", "age": 9, "species": "hamster", "breed": "chinese hamster", "shelter_id": 2}'
* curl http://121.0.0.1:5000/animals -X POST -H "Authorization: Bearer $shelter_manager_token" -H "Content-Type: application/json" -d '{"name": "Fab", "gender": "female", "age": 9, "species": "hamster", "breed": "chinese hamster", "shelter_id": 2}'

```
{
    "animals":[
        {
        "age":9,
        "breed":"chinese hamster",
        "gender":"female",
        "id":8,"name":"Fab",
        "shelter_id":2,
        "species":"hamster"
        }
    ],
    "success":true
}
```

#### PATCH /shelters/<int:shelter_id>

* Updates an existing shelter
* Role Domain Admin or Shelter Manager
* Requires `patch:shelters`
* curl https://udacityanimalrescue.herokuapp.com/shelters/1 -X PATCH -H "Authorization: Bearer $shelter_manager_token" -H "Content-Type: application/json" -d '{"phone": "925-779-6989"}'
* curl http://121.0.0.1:5000/shelters/1 -X PATCH -H "Authorization: Bearer $shelter_manager_token" -H "Content-Type: application/json" -d '{"phone": "925-779-6989"}'

```
{
    "shelters":[
        {
        "address":"300 L Street",
        "city":"Antioch",
        "id":1,
        "name":"Antioch Animal Services",
        "phone":"925-779-6989",
        "state":"CA"
        }
    ],
    "success":true
}
```

#### PATCH /animals/<int:animal_id>

* Updates an existing animal
* Role: Domain Admin or Animal Specialist
* Requires `patch:animals`
* curl https://udacityanimalrescue.herokuapp.com/animals/3 -X PATCH -H "Authorization: Bearer $animal_specialist_token" -H "Content-Type: application/json" -d '{"name": "Mary-Lou"}'
* curl http://121.0.0.1:5000/animals/3 -X PATCH - H "Authorization: Bearer $animal_specialist_token" -H "Content-Type: application/json" -d '{"name": "Mary-Lou"}'

```
{
    "animals":[
        {
        "age":15,
        "breed":"chihuahua",
        "gender":"female",
        "id":3,
        "name":"Mary-Lou",
        "shelter_id":3,
        "species":"dog"
        }
    ],
    "success":true
}
```

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    'success': False,
    'error': 400,
    'message': 'Bad request'
}
```

This API recognizes five error types:
* 400: Bad request
* 401: Unauthorized
* 404: Not found
* 422: Unprocessable entity
* 500: Internal server error

## Testing

To run the tests execute:

```
python test_app.py
```




