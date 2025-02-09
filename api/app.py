from website import create_app, db
from flask import Flask, jsonify, render_template
from flask_cors import CORS
app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}}) 


@app.route('/')
def index():
    return jsonify({"message": "Hello, this is my Flask app running on Vercel!"})

def handler(request):
    return app(request.environ, request.start_response)
if __name__ == '__main__':
    app.run(debug=True)


