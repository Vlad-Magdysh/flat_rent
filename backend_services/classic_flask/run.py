from app import flask_app
import routes
_ = routes

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port='8000', debug=True)