# Chatbot de Auditoria com RAG

Este projeto implementa um **chatbot de auditoria inteligente** para a empresa fictícia Dunder Mifflin, inspirado no desafio proposto pelo Toby Flenderson.  

A ferramenta foi desenvolvida para auxiliar na análise de **compliance**, investigação de **comunicações internas** e identificação de **potenciais fraudes financeiras**, utilizando técnicas de recuperação de informação e modelos de linguagem.

O foco do projeto não é apenas responder perguntas, mas **justificar cada resposta com evidências rastreáveis**, tornando o sistema auditável e confiável.

O vídeo do projeto pode ser acessado [aqui](https://drive.google.com/file/d/1PDTED6Ac7q48wRYhrdX8bj___Bpbblw5/view?usp=sharing).

---

## Visão geral da solução

O AuditBot foi estruturado como um conjunto de módulos independentes, cada um responsável por um aspecto do problema.  
Nesta primeira etapa do projeto, foi implementado o **chatbot de consulta à política de compliance**, utilizando a abordagem de *Retrieval-Augmented Generation (RAG)*.

A política de compliance é ingerida, fragmentada em trechos menores, indexada em um mecanismo vetorial e consultada dinamicamente conforme a pergunta do usuário. A resposta final é sempre baseada apenas nos trechos recuperados do documento, evitando alucinações e permitindo a apresentação de evidências.

---

## Estrutura do projeto
```
dunder-auditbot/
│
├── data/
│ ├── politica_compliance.txt
│ ├── transacoes_bancarias.csv
│ └── emails_internos.txt
│
├── src/
│ ├── app.py
│ ├── config.py
│ ├── ingest/
│ ├── rag/
│ ├── detectors/
│ └── utils/
│
├── requirements.txt
├── .env.example
└── README.md
```

Arquivos sensíveis, como chaves de API e ambientes virtuais, não são versionados.

---

## Tecnologias utilizadas

- Python 3
- FAISS para busca vetorial
- OpenAI API (via requisições HTTP)
- python-dotenv para gerenciamento de variáveis de ambiente
- pandas (preparação para as próximas etapas do projeto)

---

## Como rodar o projeto localmente

1. Clone o repositório
2. Crie e ative um ambiente virtual
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo .env a partir do .env.example e insira sua chave da OpenAI

5. Gere o índice da política de compliance:

```bash
python -c "from src.rag.policy_rag import build_policy_index; build_policy_index()"
```

6. Faça uma consulta de teste:

```bash
python -m src.app policy "Quais gastos são proibidos pela política?"
```

### Boas práticas de segurança

A chave da API da OpenAI não é armazenada no código nem versionada. Ela é carregada exclusivamente via arquivo .env, que permanece fora do repositório, conforme boas práticas de segurança.

## Observações finais

Este projeto foi desenvolvido com foco em clareza, rastreabilidade e auditabilidade, priorizando decisões técnicas simples e explicáveis, adequadas ao contexto de uma ferramenta de auditoria.
