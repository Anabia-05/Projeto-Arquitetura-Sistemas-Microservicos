from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError 
import os 
import re 


mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)

db = client['DBPython']
collection = db['pacients']

try:
    collection.create_index([("_id", 1)], unique=True)
    print("Indice de unicidade no _id (CPF) criado com sucesso.")
except Exception as e:
    print(f"Erro ao criar indice: {e}")

app = Flask(__name__)
api = Api(app)

class Patients(Resource):
    def get(self):
       users = list(collection.find())

       for user in users:
           user['_id'] = str(user['_id'])
         
       return jsonify(users)

    def post(self):
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
        
        if not nome or not cpf:
            return {"erro": "Nome e CPF são obrigatórios"}, 400

        cpf_pattern = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
        
        if not cpf_pattern.match(cpf):
            return {"erro": "O CPF deve estar no formato 000.000.000-00."}, 400

        new_data = { 
            "_id": cpf, 
            "nome": nome, 
            "data_nascimento": data_nascimento, 
            "contato": contato, 
            "cep": cep,
            "endereco": endereco, 
            "nome_mae": nome_mae, 
            "conato_emergencia": conato_emergencia, 
            "tipo_sanguineo": tipo_sanguineo 
        }
        
        try:
            user = collection.insert_one(new_data)
            return jsonify({"message": "Paciente Adicionado!", "id": user.inserted_id})
        except DuplicateKeyError:
            return {"erro": f"CPF {cpf} ja esta cadastrado!"}, 409
        except Exception as e:
            return {"erro": f"Erro interno: {str(e)}"}, 500


class PatientById(Resource):
    def get(self, id):
        
        user = collection.find_one({"_id": id})
        
        if user is None:
            return {"erro": "Paciente não encontrado!"}, 404

        user['_id'] = str(user['_id'])

        return jsonify(user)
    
    
    def put(self, id):
        data = request.get_json(force=True)
        nome = data.get('nome')
        data_nascimento = data.get('data_nascimento')
        contato = data.get('contato')
        cep = data.get('cep')
        endereco = data.get('endereco')
        nome_mae = data.get('nome_mae')
        conato_emergencia = data.get('conato_emergencia')
        tipo_sanguineo = data.get('tipo_sanguineo')
        
        if data.get('cpf'):
             return {"erro": "Não é permitido alterar o campo 'cpf' (ID primário) usando esta rota."}, 403


        update_data = {}
        if nome:
            update_data['nome'] = nome
        if data_nascimento:
            update_data['data_nascimento'] = data_nascimento
        if contato:
            update_data['contato'] = contato
        if cep:
            update_data['cep'] = cep
        if conato_emergencia:
            update_data['conato_emergencia'] = conato_emergencia
        if tipo_sanguineo:
            update_data['tipo_sanguineo'] = tipo_sanguineo
        if endereco:
            update_data['endereco'] = endereco
        if nome_mae:
            update_data['nome_mae'] = nome_mae
            
        if not update_data:
            return {"erro": "Nenhum campo para atualização foi fornecido."}, 400


        patient = collection.update_one({"_id": id}, {"$set": update_data})

        if patient.matched_count == 0:
            return {"erro": "Paciente não encontrado!"}, 404

        return jsonify({"message": "Paciente atualizado com sucesso!"})

    def delete(self, id):

        user = collection.find_one({"_id": id})
        if user is None:
            return {"erro": "Paciente não encontrado!"}, 404

        collection.delete_one({"_id": id})

        return jsonify({"message": "Paciente deletado com sucesso!"})


api.add_resource(Patients, '/patients')
api.add_resource(PatientById, '/patients/<id>')

if __name__ == '__main__':
    app.run()