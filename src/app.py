from flask import Flask, request,jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

#Creamos la aplicacion servidor de Flask
app = Flask(__name__)
#Creando la base de datos en MongoDb
app.config['MONGO_URI']='mongodb://localhost/fullstack'
#Creamos la conexion con la base de datos
mongo  = PyMongo(app)

#Parar no tener problemas con React ya que en su entorno de desarrollo
#React crea su propio servidor, y para no tener ningun conflito 
#Usamos Cors para que se comunique con el servidor de React
CORS(app)



#Creando la colecion de la base de datos
db = mongo.db.users

#Crear usuarios
@app.route('/users', methods=['POST'])
def createUser():
    #Insertamos el nuevo usuario ala BAse de datos
    #Guardamos al usuario en una Variable ID
    #Ya retorna la Base de datos retorna un ID por defecto
    id = db.insert({
        'nombre':request.json['nombre'],
        'correo':request.json['correo'],
        'password':request.json['password']
    })
    #Convertimos el ID en un Objetocon ObjectId()
    #Convertimos el id a un String con str()
    #Retornamos al Cliente el ID del nuevo usuario
    return jsonify(str(ObjectId(id)))
  

#Obteniendo usuarios
@app.route('/users', methods=['GET'])
def getUser():
    #Creamos un arreglo para los usuarios que viene de la base de datos
    users = []
    #recoremos ese objecto (usuarios) 
   #para obtener su valor
   
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'nombre':doc['nombre'],
            'correo':doc['correo'],
            'password':doc['password']
        })
        #retornamos el arreglo de usuarios
    return jsonify(users)



#Obtener un unico usuario
@app.route('/user/<id>', methods=['GET'])
#Recibimos como parametro un Unico usuario con un ID
def getUSer(id):
    #Creamos un variable para obtener el ID de ese usuario en especifico
    user = db.find_one({'_id': ObjectId(id)})
  #retornamos en un formato json los datos del usuario con ese ID unico 
    return jsonify({
            '_id': str(ObjectId(user['_id'])),
            'nombre':user['nombre'],
            'correo':user['correo'],
            'password':user['password']
        })
    
#Eliminar usuario
@app.route('/users/<id>', methods=['DELETE'])
#Recibimos como parametro a ese unico usuario que queremos eliminar 
def deleteUser(id):
    #Eliminamos al usuario atravez de ese ID unico 
    db.delete_one({'_id': ObjectId(id)})
    #Retornamos al cliente un mensaje
    return jsonify({
        'msg': 'Usuario eliminado correctamente'
    })
#Actualizar usuario
@app.route('/users/<id>', methods=['PUT'])
#Inidcamos atravez de ID que le pasamos 
#Que usuario queremos eliminar
#Si el id es correcto Actualizamos los valores del usuario
def updateUSer(id):
    db.update_one({'_id': ObjectId(id)},{'$set':{
        'nombre':request.json['nombre'],
        'correo':request.json['correo'],
        'password':request.json['password'],
    }})
    return jsonify({
        'msg': 'Usuario actualizado satisfactoriamente '
    })



#Iniciamos la app de del servidor 
if __name__ == "__main__":
    app.run(debug=True)

