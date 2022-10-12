from  flask import Flask
app = Flask(__name__)   #iniciar la app
app.secret_key = "shuper secreto"
app.config['UPLOAD_FOLDER'] = 'flask_app/static/img'
