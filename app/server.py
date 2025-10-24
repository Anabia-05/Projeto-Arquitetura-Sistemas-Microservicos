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
        
        nome = data.get('nome')
        cpf = data.get('cpf')
        data_nascimento = data.get('data_nascimento')
        contato = data.get('contato')
        cep = data.get('cep')
        endereco = data.get('endereco')
        nome_mae = data.get('nome_mae')
        conato_emergencia = data.get('conato_emergencia')
        tipo_sanguineo = data.get('tipo_sanguineo')

        

        if not nome:
            return jsonify({"erro": "nome é obrigatório"}), 400

        new_data = { "nome": nome, "cpf": cpf, "data_nascimento": data_nascimento , "contato": contato, "cep": cep,"endereco": endereco ,"nome_mae": nome_mae, "conato_emergencia": conato_emergencia, "tipo_sanguineo": tipo_sanguineo }
        user = collection.insert_one(new_data)

        return jsonify({"message": "Paciente Adicionado!", "id": str(user.inserted_id)})


class PatientById(Resource):
    def get(self, id):
        try:
            object_id = ObjectId(id)
        except Exception:
            return jsonify({"erro": "ID inválido!"})
        
        user = collection.find_one({"_id": object_id})
        user['_id'] = str(user['_id'])

        return jsonify(user)
    
    
    def put(self, id):
        # Campos que se espera atualizar em um Paciente
        nome = request.json.get('nome')
        data_nascimento = request.json.get('data_nascimento')
        contato = request.json.get('contato')
        cep = request.json.get('cep')
        endereco = request.json.get('endereco')
        nome_mae = request.json.get('nome_mae')
        cpf = request.json.get('cpf')
        conato_emergencia = request.json.get('conato_emergencia')
        tipo_sanguineo = request.json.get('tipo_sanguineo')

        
        # Cria o objeto de dados apenas com os campos fornecidos na requisição
        update_data = {}
        if nome:
            update_data['nome'] = nome
        if data_nascimento:
            update_data['data_nascimento'] = data_nascimento
        if contato:
            update_data['contato'] = contato
        if cep:
                update_data['cep'] = cep
        if cpf:
            update_data['cpf'] = cpf
        if conato_emergencia:
            update_data['conato_emergencia'] = conato_emergencia
        if tipo_sanguineo:
            update_data['tipo_sanguineo'] = tipo_sanguineo
        if endereco:
            update_data['endereco'] = endereco
        if nome_mae:
            update_data['nome_mae'] = nome_mae
            
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
            return jsonify({"erro": "ID inválido!"})
        
        user = collection.find_one({"_id": object_id})
        if user is None:
            return jsonify({"erro": "Paciente não encontrado!"}), 404

        collection.delete_one({"_id": object_id})

        return jsonify({"message": "Paciente deletado com sucesso!"})


api.add_resource(Patients, '/patients')
api.add_resource(PatientById, '/patients/<id>')

if __name__ == '__main__':
    app.run()