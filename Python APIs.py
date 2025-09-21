from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse

# In-memory database
books_db = []

# Helper function to find a book by ID
def find_book(book_id):
    for book in books_db:
        if book["id"] == book_id:
            return book
    return None

class BookHandler(BaseHTTPRequestHandler):

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _read_request_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(content_length).decode('utf-8')

    # GET requests
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip("/").split("/")

        # GET all books
        if len(path_parts) == 1 and path_parts[0] == "books":
            self._set_headers()
            self.wfile.write(json.dumps(books_db).encode())
        
        # GET a book by ID
        elif len(path_parts) == 2 and path_parts[0] == "books":
            try:
                book_id = int(path_parts[1])
                book = find_book(book_id)
                if book:
                    self._set_headers()
                    self.wfile.write(json.dumps(book).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Book not found"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid book ID"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    # POST requests
    def do_POST(self):
        if self.path == "/books":
            try:
                data = json.loads(self._read_request_body())
                if find_book(data["id"]):
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": "Book with this ID already exists"}).encode())
                    return
                books_db.append({
                    "id": data["id"],
                    "book_name": data["book_name"],
                    "author": data["author"],
                    "publisher": data["publisher"]
                })
                self._set_headers(201)
                self.wfile.write(json.dumps(data).encode())
            except Exception as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    # PUT requests
    def do_PUT(self):
        path_parts = self.path.strip("/").split("/")
        if len(path_parts) == 2 and path_parts[0] == "books":
            try:
                book_id = int(path_parts[1])
                book = find_book(book_id)
                if not book:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Book not found"}).encode())
                    return
                data = json.loads(self._read_request_body())
                book["book_name"] = data.get("book_name", book["book_name"])
                book["author"] = data.get("author", book["author"])
                book["publisher"] = data.get("publisher", book["publisher"])
                self._set_headers()
                self.wfile.write(json.dumps(book).encode())
            except Exception as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    # DELETE requests
    def do_DELETE(self):
        path_parts = self.path.strip("/").split("/")
        if len(path_parts) == 2 and path_parts[0] == "books":
            try:
                book_id = int(path_parts[1])
                global books_db
                if not find_book(book_id):
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Book not found"}).encode())
                    return
                books_db = [b for b in books_db if b["id"] != book_id]
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Book deleted successfully"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid ID"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

# Run the server
def run(server_class=HTTPServer, handler_class=BookHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
