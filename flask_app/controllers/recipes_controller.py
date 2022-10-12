from gzip import READ
from flask import render_template, redirect, session, request, flash
from flask_app import app

from flask_app.models.users import User
from flask_app.models.recipes import Recipe

from werkzeug.utils import secure_filename
import os

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    return render_template('new_recipe.html', user=user)

@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')
    
    #Validación de Receta
    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')

    #validación subir imagen
    if 'imagen' not in request.files:
        flash('No seleccionó ninguna imagen', 'recetas')
        return redirect('/new/recipe')
    
    imagen =request.files['imagen']
    
    if imagen.filename == '':
        flash('Nombre de la imagen vacío', 'recetas')
        return redirect('/new/recipe')
    
    nombre_imagen = secure_filename(imagen.filename)

    #guardar imagen 
    imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen))
    #Guardamos la receta

    formulario = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "under_30": int(request.form['under_30']),
        "imagen": nombre_imagen,
        "usuario_id": int(request.form['usuario_id'])
    }



    Recipe.save(formulario)
    return redirect('/dashboard')


@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    #quermos la instancia de la receta quesse debe desplegar-en base del id que recibimos en URL
    formulario_receta = {"id": id}
    
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)

@app.route('/update/recipe', methods=['POST'])
def update_recipe(): 
    # veificar que haya iniciado session
    if 'user_id' not in session:
        return redirect('/')
    #verificar que todos los datos esten correctos, recibimos formulario que es request.form y lo validamos
    #guardar los cambios
    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe'+request.form['recipe_id']) # si hay error nos rdiriga a edit/recipe/1
    Recipe.update(request.form)
    #redireccionar a /dashboard
    return redirect('/dashboard')
    # request.form = {name: "Albondigas", description : "124", .......recipe_id: 1}

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    # verificar que haya inciado sesion
    if 'user_id' not in session:
        return redirect('/')

    #pendiente : borramos
    formulario = {"id": id}
    Recipe.delete(formulario)
    #redirigir a /dashboard
    return redirect('/dashboard')

@app.route('/view/recipe/<int:id>')
def view_recipe(id):
    # verificar que haya inciado sesion
    if 'user_id' not in session:
        return redirect('/')
    # SAber cual es el nombre del ususario que inicio sesion
    formulario ={"id": session['user_id']}
    user =User.get_by_id(formulario)
    formulario_receta ={"id":id}
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('/show_recipe.html', user=user, recipe=recipe)


