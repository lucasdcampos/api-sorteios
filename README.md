# Sistema de Sorteio de Vagas para Condominios

Esse projeto é uma API para um sistema de sorteios de vagas de garagem para condominios criado para um trabalho na faculdade.

O sistema é muito maior, essa parte representa apenas a API. O resto está fechado.

---

## Rodando o projeto

### Passo 1: Clonar o repositório

```bash
git clone https://github.com/lucasdcampos/api-sorteios
cd sorteios
```

---

### Passo 2: Criar e ativar ambiente virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate     # Linux/MacOS
venv\Scripts\activate.bat    # Windows
```

---

### Passo 3: Instalar dependências

```bash
pip install -r requirements.txt
```

---

### Passo 4: Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
SUPABASE_URL=https://url-do-projeto.supabase.co
SUPABASE_KEY=chave-do-supabase
```

---

### Passo 5: Rodar a API

Use o `uvicorn` para iniciar o servidor:

```bash
uvicorn app.main:app --reload
```

- O servidor vai rodar em `http://127.0.0.1:8000`
- A flag `--reload` reinicia o servidor automaticamente quando arquivos são alterados

---

### Passo 6: Testar a API

- Testar rota raiz:

```bash
curl http://127.0.0.1:8000/
```

Resposta esperada:

```json
{
  "message": "Hello, World!"
}
```
