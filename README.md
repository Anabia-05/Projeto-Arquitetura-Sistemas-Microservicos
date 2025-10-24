# Projeto: Microsserviço de Pacientes (API Flask + MongoDB)

Este projeto é um **microsserviço Python/Flask** responsável pelo gerenciamento de pacientes, utilizando **MongoDB** como banco de dados e **Docker Compose** para orquestração do ambiente.

---

## Visão Geral

O sistema é composto por uma **API RESTful** que expõe endpoints para operações CRUD sobre o recurso de pacientes, garantindo uma comunicação eficiente e persistência de dados no MongoDB.

Ele pode ser executado de forma isolada via Docker, sem necessidade de configurações manuais adicionais.

---

## Pré-requisitos

Para executar o sistema localmente, é necessário ter instalado:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Execução do Sistema

Para subir o ambiente completo (API + MongoDB), execute no diretório raiz do projeto — onde está localizado o arquivo `docker-compose.yml`:

```bash
docker-compose up --build
```

> O parâmetro `--build` garante que a imagem da API seja reconstruída com a versão mais recente do seu `server.py`.

---

## Serviços do Sistema

| Serviço | Tecnologia | Endereço de Acesso |
| :--- | :--- | :--- |
| **api** | Flask (Python 3.9) | [http://localhost:5000](http://localhost:5000) |
| **mongo** | MongoDB | Porta **27018** (Host) |

---

## Testando a API (Endpoints Implementados)

A API está configurada para o recurso **Pacientes (`/patients`)**, permitindo o ciclo completo de CRUD.  
Você pode testar via `curl` (recomendado: **Git Bash**).

---

### 1. Cadastrar um Novo Paciente (`POST /patients`)

Cria um novo registro de paciente:

```bash
curl localhost:5000/patients -H "Content-Type: application-json" -d '{"name":"teste", "contact": "9999-9999", "birth_date":"2020-01-01"}'
```

**Retorno esperado:**

```json
{
  "message": "Added patient!",
  "id": "um_id_unico_do_mongodb"
}
```

---

### 2. Buscar Todos os Pacientes (`GET /patients`)

Recupera a lista completa de pacientes:

```bash
curl http://localhost:5000/patients
```

---

### 3. Atualizar Dados de um Paciente (`PUT /patients/{id}`)

Atualiza campos de um paciente já cadastrado:

```bash
curl -X PUT http://localhost:5000/patients/{ID_DO_PACIENTE} -H "Content-Type: application/json" -d '{"contact": "1111-2222"}'
```

---

### 4. Deletar um Paciente (`DELETE /patients/{id}`)

Remove o paciente do banco de dados:

```bash
curl -X DELETE http://localhost:5000/patients/{ID_DO_PACIENTE}
```

---

## Próximos Passos no Desenvolvimento

Atualmente, o `server.py` implementa o CRUD básico para **Pacientes**.  
As próximas etapas do projeto incluem o desenvolvimento dos seguintes recursos:

| Módulo | Endpoint | Descrição |
| :--- | :--- | :--- |
| **Histórico Clínico e Condições** | `/conditions` | Registro de diagnósticos, doenças e condições médicas. |
| **Alergias** | `/allergies` | Armazenamento e consulta de alergias. |
| **Encontros/Atendimentos** | `/encounters` | Registro de consultas, atendimentos e interações clínicas. |

---

## Observações Finais

- O ambiente Docker isola todos os serviços, facilitando o deploy em diferentes máquinas.  
- As requisições são totalmente compatíveis com clientes REST como **Insomnia**, **Postman** ou **curl**.  
- O código foi estruturado para facilitar expansão futura (novas entidades, logs e autenticação).  
