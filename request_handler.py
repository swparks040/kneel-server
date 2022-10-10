import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import (
    get_all_metals,
    get_single_metal,
    create_metal,
    delete_metal,
    update_metal,
)
from views import get_all_orders, get_single_order, create_order, delete_order
from views import get_all_sizes, get_single_size, create_size, delete_size, update_size
from views import (
    get_all_styles,
    get_single_style,
    create_style,
    delete_style,
    update_style,
)


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

    def do_GET(self):
        """Handles GET requests to the server"""
        # self._set_headers(200)
        response = {}  # Default response
        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            if id is not None:
                response = get_single_metal(id)
                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = {
                        "message": "That metal is not currently in stock for jewelry."
                    }
            else:
                response = get_all_metals()
        elif resource == "orders":
            if id is not None:
                response = get_single_order(id)
                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = {
                        "message": "That order was never placed, or was cancelled."
                    }
            else:
                response = get_all_orders()
        elif resource == "sizes":
            if id is not None:
                response = get_single_size(id)
                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = {"message": "That size is not available."}
            else:
                response = get_all_sizes()
        elif resource == "styles":
            if id is not None:
                response = get_single_style(id)
                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = {"message": "That style is not available."}
            else:
                response = get_all_styles()

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        # set server response
        self._set_headers(201)
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        # JSON to Python
        post_body = json.loads(post_body)
        # Parse URL
        (resource, id) = self.parse_url(self.path)
        # Initialize new items
        new_metal = None
        new_order = None
        new_size = None
        new_style = None
        # add new item to list
        if resource == "metals":
            if "metal" in post_body and "price" in post_body:
                self._set_headers(201)
                new_metal = create_metal(post_body)
            else:
                self._set_headers(400)
                new_metal = {
                    "message": f'{"metal is required" if "metal" not in post_body else ""} {"price is required" if "price" not in post_body else ""}'
                }
            self.wfile.write(json.dumps(new_metal).encode())
        if resource == "orders":
            if (
                "order" in post_body
                and "metalId" in post_body
                and "sizeId" in post_body
                and "styleId" in post_body
            ):
                self._set_headers(201)
                new_order = create_order(post_body)
            else:
                self._set_headers(400)
                new_order = {
                    "message": f'{"order is required" if "order" not in post_body else ""} {"metalId is required" if "metalId" not in post_body else ""} {"sizeId is required" if "sizeId" not in post_body else ""} {"styleId is required" if "styleId" not in post_body else ""}'
                }
            self.wfile.write(json.dumps(new_order).encode())
        if resource == "sizes":
            if "size" in post_body and "carats" in post_body and "price" in post_body:
                self._set_headers(201)
                new_size = create_size(post_body)
            else:
                self._set_headers(400)
                new_size = {
                    "message": f'{"size is required" if "size" not in post_body else ""} {"carats is required" if "carats" not in post_body else ""} {"price is required" if "price" not in post_body else ""}'
                }
            self.wfile.write(json.dumps(new_size).encode())
        if resource == "styles":
            if "style" in post_body and "price" in post_body:
                self._set_headers(201)
                new_style = create_style(post_body)
            else:
                self._set_headers(400)
                new_style = {
                    "message": f'{"style is required" if "style" not in post_body else ""} {"price is required" if "price" not in post_body else ""}'
                }
            self.wfile.write(json.dumps(new_style).encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        # self._set_headers(204)
        response = ""
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        # Delete a single metal from the list
        if resource == "metals":
            update_metal(id, post_body)
            self._set_headers(204)
        elif resource == "orders":
            response = {"message": "Unable to update order."}
            self._set_headers(405)
        elif resource == "sizes":
            update_size(id, post_body)
            self._set_headers(204)
        elif resource == "styles":
            update_style(id, post_body)
            self._set_headers(204)
        self.wfile.write(json.dumps(response).encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)
        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        # Delete a single metal from the list
        if resource == "metals":
            delete_metal(id)
        # Encode the new metal and send in response
        self.wfile.write("".encode())
        # Delete a single order from the list
        if resource == "orders":
            delete_order(id)
        # Encode the new order and send in response
        self.wfile.write("".encode())
        # Delete a single size from the list
        if resource == "sizes":
            delete_size(id)
        # Encode the new size and send in response
        self.wfile.write("".encode())
        # Delete a single style from the list
        if resource == "styles":
            delete_style(id)
        # Encode the new style and send in response
        self.wfile.write("".encode())


# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
