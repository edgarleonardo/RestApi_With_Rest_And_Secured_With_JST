from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)
print(__name__)

books = [
        {
            'name': 'LOTR',
            'price': 8.33,
            'isbn': 29039890298930
        },
        {
            'name': 'The Hobbit',
            'price': 6.33,
            'isbn': 89059890298930
        },
        {
            'name': 'Game Of Thrones',
            'price': 2.33,
            'isbn': 49039890298930
        },
        {
            'name': 'Song Of Ice And Fire',
            'price': 1.33,
            'isbn': 333
        }
]

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
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if ("name" in request_data):
        updated_book["name"] = request_data["name"]
    if ("price" in request_data):
        updated_book["price"] = request_data["price"]
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = '/books/'+str(isbn)
    return response


#PUT /books/9333004
#{
#    'name': 'new name',
#    'price': 3.4
#}
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()

    if (not validPutBooksObject(request_data)):
        invalidBookObjectError = {
            "error": "The params sent are wrong",
            "helpString": "Data passed in similar to this {'name': 'bookname', "
        }
        response = Response(json.dumps(invalidBookObjectError), 400, mimetype='application/json')
        return response

    new_data = {
            "name": request_data["name"],
            "price":request_data["price"],
            "isbn":isbn
    }
    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_data
        i = 1
    response = Response("", status=204)
    return response

# Post /books
#{
#    'name': 'Name',
#    'price': 1.11,
#    'isbn': 555
#}
@app.route('/books', methods=['POST'])
def add_books():
    requestData = request.get_json()
    if (validBooksObject(requestData)):
        new_data = {
            "name": requestData["name"],
            "price":requestData["price"],
            "isbn":requestData["isbn"]
        }
        books.insert(0, new_data)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/"+ str(new_data['isbn'])
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
def delete_book(isbn):
    i = 0
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status = 204)
            return response
        i += 1
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
    return jsonify({'books': books})

# Get /books/89059890298930
@app.route('/books/<int:isbn>')
def get_single_books(isbn):
    """This end point returns a single books

    """
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"],
                'isbn': book["isbn"],
            }
    return jsonify(return_value)



app.run(port=5000)