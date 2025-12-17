# Chatbot de Auditoria com RAG

Este projeto implementa um **chatbot de auditoria inteligente** para a empresa fictícia Dunder Mifflin, inspirado no desafio proposto pelo Toby Flenderson.  

A ferramenta foi desenvolvida para auxiliar na análise de **compliance**, investigação de **comunicações internas** e identificação de **potenciais fraudes financeiras**, utilizando técnicas de recuperação de informação e modelos de linguagem.

O foco do projeto não é apenas responder perguntas, mas **justificar cada resposta com evidências rastreáveis**, tornando o sistema auditável e confiável.

O vídeo do projeto pode ser acessado [aqui](https://drive.google.com/file/d/1PDTED6Ac7q48wRYhrdX8bj___Bpbblw5/view?usp=sharing).

---

## Visão geral da solução

O AuditBot foi estruturado como um conjunto de módulos independentes, cada um responsável por um aspecto do problema.  
Nesta primeira etapa do projeto, foi implementado o **chatbot de consulta à política de compliance**, utilizando a abordagem de *Retrieval-Augmented Generation (RAG)*.

## Visão geral da solução

O AuditBot foi estruturado como um conjunto de módulos independentes, cada um responsável por um aspecto específico do problema. A arquitetura separa claramente **ingestão de dados**, **recuperação de informação**, **lógica de auditoria** e **uso pontual de modelos de linguagem**.

A solução cobre três frentes principais:

1. Consulta à política de compliance por meio de RAG  
2. Investigação de possíveis conspirações a partir de emails internos  
3. Detecção de violações de compliance e fraudes financeiras, tanto diretas (`audit_rules()`) quanto contextuais (`audit_contexts()`)

Em todos os casos, o sistema retorna não apenas conclusões, mas também **as evidências que sustentam cada decisão**.

---

### Funcionalidades

### 1. Chatbot de política de compliance (RAG)

- Leitura do documento de política de compliance
- Fragmentação em trechos menores com sobreposição
- Geração de embeddings e indexação vetorial com FAISS
- Recuperação dos trechos mais relevantes para cada pergunta
- Geração da resposta baseada exclusivamente no contexto recuperado
- Retorno explícito das evidências utilizadas

Essa funcionalidade permite que colaboradores consultem regras de compliance de forma rápida, explicável e auditável.

---

### 2. Detecção de conspiração em comunicações internas

- Parsing estruturado do dump de emails (De, Para, Data, Assunto, Mensagem)
- Identificação de mensagens com linguagem suspeita ou conspiratória
- Filtro baseado em termos-chave e contexto (ex.: menções ao Toby)
- Veredito final indicando se há evidência, ausência de evidência ou inconclusão
- Apresentação de trechos específicos dos emails como evidência

O modelo de linguagem é utilizado apenas para **sintetizar e justificar** conclusões a partir de evidências já selecionadas.

---

### 3. Auditoria de transações financeiras

#### Auditoria baseada em regras (transações isoladas)

- Leitura do extrato de gastos em CSV
- Aplicação de regras determinísticas (palavras proibidas, fornecedores suspeitos, valores elevados)
- Identificação de transações que violam compliance por si só
- Associação de cada violação a trechos relevantes da política de compliance (via busca vetorial)
- Processo escalável e independente de LLM para tomada de decisão

#### Auditoria contextual (transações + emails)

- Seleção de transações suspeitas por heurísticas
- Cruzamento com emails contendo linguagem de encobrimento ou fraude
- Avaliação contextual para identificar possíveis combinações de desvio
- Conclusão classificada como “fraude provável” ou “inconclusivo”
- Evidências apresentadas tanto do extrato financeiro quanto das comunicações internas

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

6. Comandos disponíveis:

**Consulta à política de compliance:**

```bash
python -m src.app policy "Quais gastos são proibidos pela política?"
```

**Investigação de conspiração em emails:**

```bash
python -m src.app conspiracy
```

**Auditoria de transações baseada em regras:**

```bash
python -m src.app audit_rules
```

**Auditoria de fraudes com contexto (emails + transações):**

```bash
python -m src.app audit_context
```

### Boas práticas de segurança

A chave da API da OpenAI não é armazenada no código nem versionada. Ela é carregada exclusivamente via arquivo .env, que permanece fora do repositório, conforme boas práticas de segurança.

## Observações finais

Este projeto foi desenvolvido com foco em clareza, rastreabilidade e auditabilidade, priorizando decisões técnicas simples e explicáveis, adequadas ao contexto de uma ferramenta de auditoria.
