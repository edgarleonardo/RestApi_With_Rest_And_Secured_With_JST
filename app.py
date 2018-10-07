from flask import Flask, jsonify, request, Response
import json
from settings import *
from bookModel import *
from settings import *
import jwt, datetime
from userModel import User
from functools import wraps

DEFAULT_PAGE_LIMIT = 3

app.config['SECRET_KEY'] = 'meow'

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid token'})
    return wrapper

@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])
    match = User.username_password_match(username, password)

    if (match):
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response("", 401, mimetype='application/json')

@app.route('/')
def hello_world():
    """End Point Primero 

    """
    return 'This is Edgar'

def validBooksObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

def validPutBooksObject(bookObject):
    if ("name" in bookObject and "price" in bookObject ):
        return True
    else:
        return False

#PATCH /books/9333004
#{
#    'name': 'new name'
#}
@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()
    if ("name" in request_data):
        Book.update_book_name(isbn, request_data["name"])
    if ("price" in request_data):
        Book.update_book_price(isbn, request_data["price"])    
    response = Response("", status=204)
    response.headers['Location'] = '/books/'+str(isbn)
    return response


#PUT /books/9333004
#{
#    'name': 'new name',
#    'price': 3.4
#}
@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
    request_data = request.get_json()

    if (not validPutBooksObject(request_data)):
        invalidBookObjectError = {
            "error": "The params sent are wrong",
            "helpString": "Data passed in similar to this {'name': 'bookname', "
        }
        response = Response(json.dumps(invalidBookObjectError), 400, mimetype='application/json')
        return response

    Book.replace_book(isbn, request_data["name"], request_data["price"])
    response = Response("", status=204)
    return response

# Post /books
#{
#    'name': 'Name',
#    'price': 1.11,
#    'isbn': 555
#}
@app.route('/books', methods=['POST'])
@token_required
def add_books():
    requestData = request.get_json()
    if (validBooksObject(requestData)):
        Book.add_book(requestData["name"],requestData["price"],requestData["isbn"])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/"+ str(requestData['isbn'])
        return response
    else:
        invalidBookObjectError = {
            "error": "The params sent are wrong",
            "helpString": "Data passed in similar to this {'name': 'bookname', "
        }
        response = Response(json.dumps(invalidBookObjectError), 400, mimetype='application/json')
        return response

#DELETE /books/9333004
@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    if (Book.delete_book(isbn)):
        response = Response("", status = 204)
        return response
    else:
        invalidBookObjectError = {
            "error": "The book ISNB provided was not found"
        }
        response = Response(json.dumps(invalidBookObjectError), status = 400, mimetype='application/json')
        return response

# Get /books/
@app.route('/books')
def get_books():
    """This end point returns all books 

    """
    return jsonify({'books': Book.get_all_books()})

# Get /books/89059890298930
@app.route('/books/<int:isbn>')
def get_single_books(isbn):
    """This end point returns a single books

    """
    return_value = Book.get_book(isbn)
    return jsonify(return_value)



app.run(port=5000)