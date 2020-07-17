from flask import Flask
from photoshop import crop_photo
app = Flask(__name__)

@app.route('/test')
def hello_world():
    crop_photo("https://api.time.com/wp-content/uploads/2015/02/imsis270-064.jpg?w=800&quality=85")
    return 'Hello, World!'