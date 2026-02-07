# Delta 360 — Documentação Completa das Tabelas

Este documento descreve **todas as tabelas do banco de dados** utilizadas no projeto **Delta 360**, incluindo finalidade, campos, relacionamentos e observações arquiteturais.

---

## Tabela: users

### Descrição
Tabela central de autenticação e autorização do sistema.

### Campos
- id (INTEGER, PK)
- username (STRING, único)
- email (STRING, único)
- hashed_password (STRING)
- role (STRING)
- created_at (TIMESTAMP)

### Relacionamentos
- 1:1 com Admin
- 1:1 com Funcionarios
- 1:1 com Parceiros
- 1:1 com Usuarios

---

## Tabela: admin

### Descrição
Representa usuários com permissão administrativa total.

### Campos
- id (INTEGER, PK)
- user_id (FK → users.id)

---

## Tabela: funcionarios

### Descrição
Funcionários técnicos e operacionais.

### Campos
- id (INTEGER, PK)
- user_id (FK → users.id)
- documento (STRING)
- role (STRING)

---

## Tabela: parceiros

### Descrição
Parceiros institucionais que podem abrir chamados.

### Campos
- id (INTEGER, PK)
- user_id (FK → users.id)
- telefone
- telefone_secundario
- email_secundario
- endereco
- prioridade (BOOLEAN)

---

## Tabela: chamados

### Descrição
Tabela central de ocorrências operacionais.

### Campos
- id (INTEGER, PK)
- protocolo (STRING)
- descricao (TEXT)
- status (STRING)
- client_id (FK → users.id)
- endereco_id (FK → enderecos.id)
- tipo_id (FK → tipos_chamados.id)
- criado_em (TIMESTAMP)
- atualizado_em (TIMESTAMP)

### Relacionamentos
- N:1 Enderecos
- N:1 TiposChamados
- 1:N Fotos

---

## Tabela: solicitacoes

### Descrição
Pré-chamados criados antes da aprovação operacional.

### Campos
- id (INTEGER, PK)
- descricao (TEXT)
- status (STRING)
- client_id (FK → users.id)
- endereco_id (FK → enderecos.id)
- tipo_id (FK → tipos_chamados.id)

---

## Tabela: enderecos

### Descrição
Localização geográfica e operacional das ocorrências.

### Campos
- id (INTEGER, PK)
- cep
- logradouro
- numero
- cidade
- uf

---

## Tabela: fotos

### Descrição
Evidências visuais associadas a chamados ou solicitações.

### Campos
- id (INTEGER, PK)
- nome_original
- nome_armazenado
- caminho
- origem
- content_type
- criado_em
- chamado_id (FK)
- solicitacao_id (FK)

---

## Tabela: refresh_tokens

### Descrição
Controle de sessões e autenticação persistente.

### Campos
- id (INTEGER, PK)
- token
- user_id (FK → users.id)

---

## Tabela: risk_audit

### Descrição
Auditoria completa das análises de risco realizadas pela IA.

### Campos
- id (INTEGER, PK)
- input_text
- visual_description
- risco
- confianca
- model_version
- used_fallback
- explain_terms
- created_at

---

## Tabela: tipos_chamados

### Descrição
Classificação dos tipos de ocorrência.

### Campos
- id (INTEGER, PK)
- tipo_chamado
- precisa_foto (BOOLEAN)

---

## Tabela: usuarios

### Descrição
Extensão do usuário final com dados adicionais.

### Campos
- id (INTEGER, PK)
- user_id (FK → users.id)
- telefone

---

## Observações Finais

- Todas as relações utilizam **integridade referencial**
- Fotos são removidas em cascata
- Estrutura preparada para:
  - IA
  - Auditoria
  - Escalabilidade
  - Governança

---
Base URL (local):
```
http://190.102.41.9:8080
```

Autenticação:
```
Authorization: Bearer SEU_TOKEN_JWT
```

---

## Autenticação (exemplo)

```http
POST /auth/login
Content-Type: application/json

{
  "email": "usuario@email.com",
  "password": "senha123"
}
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## Criar Chamado (com imagem)

```http
POST /chamados
Authorization: Bearer SEU_TOKEN_JWT
Content-Type: multipart/form-data
```

FormData:
```
descricao=Queda de energia em toda a rua
tipo_id=1
endereco_id=42
imagem=@poste_quebrado.jpg
```

Resposta:
```json
{
  "id": 10,
  "protocolo": "CH-5-1",
  "status": "ABERTO",
  "descricao": "Queda de energia em toda a rua"
}
```

---

## Anexar Foto a Chamado Existente

```http
POST /chamados/10/foto
Authorization: Bearer SEU_TOKEN_JWT
Content-Type: multipart/form-data
```

FormData:
```
imagem=@transformador.jpg
```

Resposta:
```json
{
  "msg": "Imagem anexada ao chamado",
  "foto_id": 7
}
```

---

## Criar Solicitação

```http
POST /solicitacoes
Authorization: Bearer SEU_TOKEN_JWT
Content-Type: multipart/form-data
```

FormData:
```
descricao=Poste pegando fogo
tipo_id=2
endereco_id=55
imagem=@incendio.jpg
```

Resposta:
```json
{
  "id": 21,
  "status": "PENDENTE"
}
```

---

## Aprovar Solicitação (gera chamado)

```http
POST /solicitacoes/21/aprovar
Authorization: Bearer TOKEN_FUNCIONARIO
```

Resposta:
```json
{
  "msg": "Solicitação aprovada e chamado criado"
}
```

---

## Rejeitar Solicitação

```http
POST /solicitacoes/21/rejeitar
Authorization: Bearer TOKEN_FUNCIONARIO
Content-Type: application/x-www-form-urlencoded
```

Body:
```
motivo=Solicitação fora da área de atendimento
```

Resposta:
```json
{
  "msg": "Solicitação rejeitada"
}
```

---

## Análise de Risco com IA

```http
POST /risk/analyze
Authorization: Bearer TOKEN_PARCEIRO
Content-Type: multipart/form-data
```

FormData:
```
texto=Poste caído próximo a escola
imagem=@poste_caido.jpg
```

Resposta:
```json
{
  "risco": "ALTO",
  "descricao": "Risco elevado devido à proximidade com área escolar."
}
```

---

## Observações

- Todos os endpoints exigem autenticação JWT
- Uploads suportam imagens JPG, PNG e WEBP
- IA é carregada sob demanda (lazy loading)
- Compatível com Swagger: `/docs`