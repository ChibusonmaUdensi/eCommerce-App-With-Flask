from website import create_app, db
from flask import Flask, jsonify
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/')
def index():
    return jsonify({"message": "Hello, this is my Flask app running on Vercel!"})

# This function allows Vercel to access your Flask app
def handler(request):
    return app(request.environ, request.start_response)