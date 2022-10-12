from operator import methodcaller
from pickle import TRUE
from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario_id = data['usuario_id']
        self.imagen = data['imagen']

        #LEFT JOIN
        self.first_name = data['first_name']

    @staticmethod
    def valida_receta(formulario):
        es_valido = True

        if len(formulario['name'])< 3:
            flash("El nombre de la receta debe tener al menos 3 caracteres","receta")
            es_valido = False

        if len(formulario['description'])< 3:
            flash("La descripción de la receta debe tener al menos 3 caracteres","receta")
            es_valido = False

        if len(formulario['instructions'])< 3:
            flash("Las instrucciones de la receta debe tener al menos 3 caracteres", "receta")
            es_valido = False

        if formulario['date_made'] == '':
            flash("ingrese una fecha","receta")
            es_valido = False

        return es_valido

    @classmethod
    def save(cls, formulario):
        #formulario = {name: "Albondigas", description: "Albondigas de carne", instructions: ".....", date_made:"0000-00-00", under_30: 0, user_id: 1}
        query = "INSERT INTO recetas (name, description, instructions, date_made, under_30, usuario_id, imagen) VALUES (%(name)s, %(description)s, %(instructions)s,%(date_made)s, %(under_30)s, %(usuario_id)s, %(imagen)s)"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        return result
    
    @classmethod
    def get_all(cls):
        query ="SELECT recetas.*, first_name FROM recetas LEFT JOIN usuarios ON usuarios.id = recetas.usuario_id;"
        results =connectToMySQL('esquema_recetas').query_db(query)
        recipes = []
            #recipes diccionario
        for recipe in results:
            recipes.append(cls(recipe)) # cls(recipe) creamos la instancia en base al diccioanrio y recipes.append agrefo esa instancia a la lista recipes
        return recipes
    
    @classmethod
    def get_by_id(cls, formulario):    #formualrio falso es un diccionario con el que recibo el id del diccioanrio
        query = "SELECT recetas.*, first_name FROM recetas LEFT JOIN usuarios ON usuarios.id = recetas.usuario_id WHERE recetas.id = %(id)s;"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        #result = [
        #    {id: 1, first_name: elena, last_name:de troya.....} -> POSICION 0
        #]
        recipes = cls(result[0]) #Creamos una instancia de Recipe y necesito el id en posision 0 de mi lista
        return recipes

    @classmethod
    def update(cls, formulario):
        query ="UPDATE recetas SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under_30=%(under_30)s  WHERE id=%(recipe_id)s"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        return result
    
    @classmethod
    def delete(cls, formulario):
        query ="DELETE FROM recetas WHERE id = %(id)s"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario)
        return result