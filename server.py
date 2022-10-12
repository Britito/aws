from flask_app import app   #de la carpeta flask_app traemos de __ini__ la app = Flask
#importar nuestro controlador
from flask_app.controllers import users_controller
from flask_app.controllers import recipes_controller








#ejecutamos variable app
if __name__=="__main__":
    app.run(debug=True)
