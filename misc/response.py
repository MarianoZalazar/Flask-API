from flask import Response, json

def get_json(dictionary, status_code):
    return Response(response = json.dumps(dictionary), status = status_code, mimetype = "application/json")