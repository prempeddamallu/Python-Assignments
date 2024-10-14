from flask import Flask, jsonify, request

app = Flask(__name__)

def get_greeting_name():
    return request.args.get('name', 'World')

@app.route('/api/greet', methods=['GET'])
def greet():
    name = get_greeting_name()
    return jsonify(message=f'Hello, {name}!')
