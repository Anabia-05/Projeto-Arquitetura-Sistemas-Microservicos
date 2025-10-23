from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson import ObjectId
import os 

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)

db = client['DBPython']
collection = db['pacients']

app = Flask(__name__)
api = Api(app)

class Patients(Resource):
    def get(self):
       users = list(collection.find())

       for user in users:
           user['_id'] = str(user['_id'])
         
       return jsonify(users)

   
    def post(self):
        # Use request.get_json(force=True) para garantir a decodificação
        data = request.get_json(force=True) 
        
        name = data.get('name')
        contact = data.get('contact')
        birth_date = data.get('birth_date')

        if not name:
            return jsonify({"erro": "Name is required"}), 400

        new_data = { "name": name, "contact": contact, "birth_date": birth_date }
        user = collection.insert_one(new_data)

        return jsonify({"message": "Added patient!", "id": str(user.inserted_id)})


class PatientById(Resource):
    def get(self, id):
        try:
            object_id = ObjectId(id)
        except Exception:
            return jsonify({"erro": "ID invalid"})
        
        user = collection.find_one({"_id": object_id})
        user['_id'] = str(user['_id'])

        return jsonify(user)
    
    
    def put(self, id):
        # Campos que se espera atualizar em um Paciente
        name = request.json.get('name')
        birth_date = request.json.get('birth_date')
        contact = request.json.get('contact')
        
        # Cria o objeto de dados apenas com os campos fornecidos na requisição
        update_data = {}
        if name:
            update_data['name'] = name
        if birth_date:
            update_data['birth_date'] = birth_date
        if contact:
            update_data['contact'] = contact
            
        try:
            object_id = ObjectId(id)
        except Exception:
            return jsonify({"erro": "ID inválido!"})

        # Atualiza a coleção de pacientes (assumindo que 'collection' foi redefinida)
        patient = collection.update_one({"_id": object_id}, {"$set": update_data})

        if patient.matched_count == 0:
            return jsonify({"erro": "Paciente não encontrado!"})

        return jsonify({"message": "Paciente atualizado com sucesso!"})

    def delete(self, id):

        try:
            object_id = ObjectId(id)
        except Exception:
            return jsonify({"erro": "ID invalid"})
        
        user = collection.find_one({"_id": object_id})
        if user is None:
            return jsonify({"erro": "User not found!"}), 404

        collection.delete_one({"_id": object_id})

        return jsonify({"message": "Delete user"})


api.add_resource(Patients, '/patients')
api.add_resource(PatientById, '/patients/<id>')

if __name__ == '__main__':
    app.run()