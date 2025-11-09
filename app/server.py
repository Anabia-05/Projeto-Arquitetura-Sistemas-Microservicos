from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os
import re
import boto3
import logging
from botocore.exceptions import ClientError
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
 
AWS_REGION = "us-east-2"
S3_BUCKET_NAME = "arquitetura-sistemas"
s3_client = boto3.client('s3', region_name=AWS_REGION)
 
logging.basicConfig(level=logging.INFO)
 
def upload_file_to_s3(file, bucket_name, object_name=None):
    if object_name is None:
        object_name = secure_filename(file.filename)
 
    try:
        s3_client.upload_fileobj(file, bucket_name, object_name)
    except ClientError:
        logging.error("Erro ao fazer upload do arquivo!")
        return None
    return object_name
 
 
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)
db = client['DBPython']
collection = db['pacients']
 
try:
    collection.create_index([("_id", 1)], unique=True)
    print("Índice de unicidade no _id (CPF) criado com sucesso.")
except Exception as e:
    print(f"Erro ao criar índice: {e}")
 
 
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
        if not nome or not cpf:
            return {"erro": "Nome e CPF são obrigatórios"}, 400
 
        cpf_pattern = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
        if not cpf_pattern.match(cpf):
            return {"erro": "O CPF deve estar no formato 000.000.000-00."}, 400
 
        new_data = {
            "_id": cpf,
            "nome": nome,
            "data_nascimento": data.get('data_nascimento'),
            "contato": data.get('contato'),
            "cep": data.get('cep'),
            "endereco": data.get('endereco'),
            "nome_mae": data.get('nome_mae'),
            "contato_emergencia": data.get('contato_emergencia'),
            "tipo_sanguineo": data.get('tipo_sanguineo'),
            "historico": {
                "ocorrencias": []
            }
        }
       
        try:
            user = collection.insert_one(new_data)
            return jsonify({"message": "Paciente Adicionado!", "id": user.inserted_id})
        except DuplicateKeyError:
            return {"erro": f"CPF {cpf} já está cadastrado!"}, 409
 
 
class PatientById(Resource):
    def get(self, id):
        user = collection.find_one({"_id": id})
        if not user:
            return {"erro": "Paciente não encontrado!"}, 404
        user['_id'] = str(user['_id'])
        return jsonify(user)
   
    def delete(self, id):
        user = collection.find_one({"_id": id})
        if user is None:
            return {"erro": "Paciente não encontrado!"}, 404
 
        collection.delete_one({"_id": id})
        return jsonify({"message": "Paciente deletado com sucesso!"})
 
 
class FileUpload(Resource):
    def get(self, id):
        user = collection.find_one({"_id": id})
        if user is None:
            return {"erro": "Paciente não encontrado!"}, 404
        
        files = user.get("files", [])
        return {"files": files}, 200
        
    def post(self, id):
        user = collection.find_one({"_id": id})
        if not user:
            return {"erro": "Paciente não encontrado!"}, 404
       
        if 'file' not in request.files:
            return {"erro": "Nenhum arquivo fornecido!"}, 400
       
        file = request.files['file']
        if file.filename == '':
            return {"erro": "Nome do arquivo vazio!"}, 400
 
        unique_filename = f"{id}_{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        s3_key = upload_file_to_s3(file, S3_BUCKET_NAME, unique_filename)
        if s3_key is None:
            return {"erro": "Falha ao fazer upload do arquivo."}, 500
       
        file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
        collection.update_one({"_id": id}, {"$push": {"files": file_url}})
        return {"message": "Arquivo enviado com sucesso!", "file_url": file_url}, 200
 
 
class HistoricoGeral(Resource):
    def get(self, id):
        paciente = collection.find_one({"_id": id}, {"historico.ocorrencias": 1})
        if not paciente:
            return {"erro": "Paciente não encontrado!"}, 404
       
        ocorrencias = paciente.get("historico", {}).get("ocorrencias", [])
        return jsonify({"ocorrencias": ocorrencias})
 
    def post(self, id):
        data = request.get_json()
        if not data:
            return {"erro": "JSON inválido ou ausente."}, 400
 
        ocorrencia = data.get("ocorrencia")            
        urgencia = data.get("urgencia", "leve").lower()
       
        # Gera a data/hora atual no formato brasileiro (dd/mm/aaaa HH:MM:SS)
        data_insercao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
 
        if not ocorrencia:
            return {"erro": "O campo 'ocorrencia' (doença/atendimento) é obrigatório."}, 400
 
        if urgencia not in ["leve", "moderada", "alta"]:
             return {"erro": "O campo 'urgencia' deve ser 'leve', 'moderada' ou 'alta'."}, 400
 
        novo_registro = {
            "_id": str(uuid.uuid4()),
            "data_ocorrencia": data_insercao,  # Usando a data/hora da inserção
            "ocorrencia": ocorrencia,
            "urgencia": urgencia
        }
       
        collection.update_one({"_id": id}, {"$push": {"historico.ocorrencias": novo_registro}})
       
        return jsonify({"message": "Ocorrencia registrada!", "ocorrencia": novo_registro})
 
    def delete(self, id):
        data = request.get_json()
        ocorrencia_id = data.get("_id")
 
        if not ocorrencia_id:
            return {"erro": "O campo '_id' da ocorrencia é obrigatório para remoção."}, 400
 
        result = collection.update_one(
            {"_id": id},
            {"$pull": {"historico.ocorrencias": {"_id": ocorrencia_id}}}
        )
 
        if result.modified_count == 0:
            return {"erro": "Ocorrência não encontrada ou paciente inexistente."}, 404
 
        return jsonify({"message": "Ocorrência removida com sucesso!"})
 
 
api.add_resource(Patients, '/patients')
api.add_resource(PatientById, '/patients/<id>')
api.add_resource(FileUpload, '/patients/<id>/upload')
api.add_resource(HistoricoGeral, '/patients/<id>/historico')
 
 
@app.route('/')
def index():
    return "Bem-vindo à API de Pacientes! Rotas: /patients, /patients/<id>, /patients/<id>/upload e /patients/<id>/historico."
 
 
if __name__ == '__main__':
    app.run()