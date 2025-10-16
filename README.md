# 🏥 Projeto: Pacientes & Prontuário (Core do Sistema)

Este projeto é o **core** do sistema de informação de saúde, responsável pela gestão centralizada dos dados de pacientes e seus prontuários eletrônicos. Ele é a fonte primária de verdade para informações clínicas essenciais.

## 🌟 Visão Geral

O módulo "Pacientes & Prontuário" gerencia todo o ciclo de vida da informação clínica do paciente, desde o cadastro inicial até o registro de seu histórico de saúde detalhado.

### 📋 Responsabilidades Principais

* **Cadastro de Pacientes:** Informações demográficas e de contato.
* **Histórico Clínico:** Registro de condições médicas, doenças preexistentes e histórico de saúde geral.
* **Gestão de Alergias:** Registro e rastreamento de alergias medicamentosas e não-medicamentosas.
* **Documentos Clínicos Estruturados:** Gerenciamento de documentos como notas de evolução, laudos e resumos de alta.

## 🛠️ Stack Tecnológico

| Componente | Tecnologia | Detalhes |
| :--- | :--- | :--- |
| **Banco de Dados Principal** | MongoDB | Armazenamento de dados estruturados (cadastros, históricos, etc.). |
| **Armazenamento de Anexos** | Amazon S3 (ou compatível) | Armazenamento de documentos clínicos não-estruturados (PDFs, Imagens, etc.). |
| **Arquitetura** | API RESTful (Microserviço) | Interface de comunicação para outros sistemas. |
| **Comunicação Assíncrona** | Mensageria/Eventos | Para notificação e coordenação com outros módulos. |

## 💡 Estrutura da API (Endpoints Principais)

A API é o principal ponto de integração para leitura e escrita de dados no sistema.

| Endpoint | Método | Descrição |
| :--- | :--- | :--- |
| `/patients` | `GET`, `POST` | Gerenciamento e busca de **pacientes**. |
| `/patients/{id}` | `GET`, `PUT`, `DELETE` | Operações em um paciente específico. |
| `/conditions` | `GET`, `POST` | Registro de **condições clínicas** e histórico. |
| `/allergies` | `GET`, `POST` | Registro e consulta de **alergias** do paciente. |
| `/encounters` | `GET`, `POST` | Gerenciamento de **encontros** ou atendimentos clínicos. |

*(Nota: A estrutura exata dos endpoints pode variar conforme a implementação REST/HATEOAS.)*


