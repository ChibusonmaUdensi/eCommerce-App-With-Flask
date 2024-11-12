from website import create_app, db
from flask import Flask, jsonify
app = create_app()


@app.route('/')
def index():
    return jsonify({"message": "Hello, this is my Flask app running on Vercel!"})

def handler(request):
    return app(request.environ, request.start_response)
if __name__ == '__main__':
    app.run(debug=True)