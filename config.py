import os

# Get the absolute path of the current directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-1234'

    # SQLite database URI
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    # Disable modification tracking to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OpenWeatherMap API key (replace with your free key)
    WEATHER_API_KEY = 'a74355d84a26835c9dd0ea47cb9b62d3'
