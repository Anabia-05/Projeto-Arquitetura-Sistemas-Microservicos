# Projeto: Microsserviço de Pacientes (API Flask + MongoDB)

Este projeto é um **microsserviço Python/Flask** responsável pelo gerenciamento de pacientes, utilizando **MongoDB** como banco de dados e **Docker Compose** para orquestração do ambiente.

---

## Visão Geral

O sistema é composto por uma **API RESTful** que expõe endpoints para operações CRUD sobre o recurso de pacientes, garantindo uma comunicação eficiente e persistência de dados no MongoDB.  
Ele pode ser executado de forma isolada via **Docker**, sem necessidade de configurações manuais adicionais.

---

## Pré-requisitos

Para executar o sistema localmente, é necessário ter instalado:

- **Docker**
- **Docker Compose**

---

## Execução do Sistema

Para subir o ambiente completo (**API + MongoDB**), execute no diretório raiz do projeto — onde está localizado o arquivo `docker-compose.yml`:

```bash
docker-compose up --build
```

> O parâmetro `--build` garante que a imagem da API seja reconstruída com a versão mais recente do seu `server.py`.

---

## Serviços do Sistema

| Serviço | Tecnologia         | Endereço de Acesso              |
|----------|--------------------|--------------------------------|
| api      | Flask (Python 3.9) | http://18.216.190.52:5000          |
| mongo    | MongoDB            | Porta 27018 (Host)             |

---

## Testando a API (Endpoints Implementados)

A API está configurada para o recurso **Pacientes (`/patients`)** e recursos aninhados, permitindo o ciclo completo de gerenciamento.  
Você pode testar via **curl** (recomendado: Git Bash).

---

### 1️. Gerenciamento de Pacientes (CRUD Básico)

| Operação        | Método | Endpoint            | Exemplo de Comando curl |
|-----------------|--------|--------------------|--------------------------|
| **Cadastrar**   | POST   | `/patients`        | ```bash curl 18.216.190.52:5000/patients -H "Content-Type: application/json" -d '{"nome": "Maria Clara da Silva", "cpf": "123.456.789-00", "data_nascimento": "15-07-1992", "contato": "99999-1234", "cep": "51020-310", "endereco": "Rua das Flores, 250 - Boa Viagem, Recife - PE", "nome_mae": "Ana Lucia da Silva", "contato_emergencia": "98888-5678", "tipo_sanguineo": "O+"}' ``` |
| **Buscar Todos**| GET    | `/patients`        | ```bash curl http://18.216.190.52:5000/patients ``` |
| **Buscar por CPF** | GET | `/patients/{cpf}` | ```bash curl http://18.216.190.52:5000/patients/111.222.333-44 ``` |
| **Atualizar**   | PUT    | `/patients/{cpf}` | ```bash curl -X PUT http://18.216.190.52:5000/patients/111.222.333-44 -H "Content-Type: application/json" -d '{"contato": "1111-2222"}' ``` |
| **Deletar**     | DELETE | `/patients/{cpf}` | ```bash curl -X DELETE http://18.216.190.52:5000/patients/111.222.333-44 ``` |

---

### 2️. Histórico do Paciente (`/patients/{cpf}/historico`)

Gerencia ocorrências (inserção, remoção e consulta) no prontuário do paciente.

| Operação            | Método | Exemplo de Comando curl |
|----------------------|--------|--------------------------|
| **Inserir Ocorrência** | POST | ```bash curl -X POST http://18.216.190.52:5000/patients/123.456.789-00/historico -H "Content-Type: application/json" -d '{"ocorrencia": "Consulta de rotina", "urgencia": "alta"}' ``` |
| **Remover Ocorrência** | DELETE | ```bash curl -X DELETE http://18.216.190.52:5000/patients/111.111.111-11/historico -H "Content-Type: application/json" -d '{"_id": "[ID_DA_OCORRENCIA]"}' ``` |
| **Consultar Histórico** | GET | ```bash curl 18.216.190.52:5000/patients/111.111.111-11/historico ``` |

---

### 3️. Upload de Arquivo (Prontuário)

Envia arquivos para o prontuário do paciente, que serão armazenados no **AWS S3 (Bucket)**.

#### 🧾 Comando para Upload de Arquivo

```bash
curl -X POST http://18.216.190.52:5000/patients/*cpf*/upload -F 'file=@caminho/nomeDoArquivo.extensao'
```

> **Atenção:** O caminho do arquivo deve estar no formato **Linux** ao usar o Git Bash (use `/` e `c/Users/` ao invés de `C:\Users\`).

#### 🧾 Comando para DELETE de Arquivo

```bash
 curl -X DELETE "http://18.216.190.52:5000/patients/*cpf*/upload"   -H "Content-Type: application/json"   -d '{"file_url": "URL_do_arquivo"}'
```
---

### 🔗 Acesso do Arquivo

Após o upload, será exibido o link de confirmação com o endereço para download.

Outras opções:

- Acessar: `http://18.216.190.52:5000/patients/*cpf*`
- Acessar diretamente o bucket pela **AWS Cloud** e procurar o arquivo nos objetos.

---

## Variáveis de Ambiente

Crie um arquivo `.env` com o seguinte conteúdo para habilitar o upload para o S3:

```bash
AWS_ACCESS_KEY_ID="ID"
AWS_SECRET_ACCESS_KEY="Key"
```

---

## Observações Finais

- O ambiente **Docker** isola todos os serviços, facilitando o deploy em diferentes máquinas.  
- As requisições são totalmente compatíveis com clientes REST como **Insomnia**, **Postman** ou **curl**.  
- O código foi estruturado para permitir **expansão futura** (novas entidades, logs e autenticação).
