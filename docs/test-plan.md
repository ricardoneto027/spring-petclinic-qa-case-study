# Test Plan & Test Design — Spring PetClinic REST
### Projeto de Portfólio QA — PAC
**Autor:** Ricardo Peres | **Produto sob teste:** Spring PetClinic REST | **Data:** Setembro 2026

---

## TEST PLAN

### 1. Introdução

Este documento define o plano de testes para o Spring PetClinic REST, uma aplicação open-source de gestão de clínica veterinária (API REST + base de dados), utilizada como sistema sob teste (SUT) para um projeto de portfólio de Quality Engineering. O objetivo é simular o processo de QA de um produto real, de ponta a ponta, aplicando testes manuais, automação, validação de dados e integração contínua.

### 2. Objetivos

- Validar que as funcionalidades principais do sistema (gestão de owners, pets, vets, visitas, especialidades e utilizadores) funcionam de acordo com o comportamento esperado.
- Identificar e documentar defeitos, ambiguidades de regras de negócio e riscos técnicos.
- Validar o controlo de acesso (autenticação e autorização) do sistema.
- Construir uma suite de testes automatizados (UI + API) integrada num pipeline de CI.
- Produzir artefactos de QA profissionais (test plan, test cases, bug reports, relatórios) como prova de competência para efeitos de portefólio.

### 3. Scope

**Dentro do escopo:**
- Testes funcionais (manuais e automatizados) de: Owners, Pets, PetTypes, Vets, Specialties, Visits, Users
- Testes de autenticação e autorização (controlo de acesso por role: `OWNER_ADMIN`, `VET_ADMIN`, `ADMIN`)
- Testes de API (funcionais, negativos, BVA) via Postman
- Validação de integridade de dados na base de dados (PostgreSQL) via SQL
- Automação de UI dos fluxos críticos (Selenium + Python + Page Object Model)
- Integração contínua (GitHub Actions) e ambiente containerizado (Docker)
- Testes exploratórios sobre os fluxos críticos e de maior risco
- Testes funcionais e de UI/UX (manuais) executados através da interface Angular (localhost:4200), cobrindo navegação, formulários e consistência visual, complementados por testes de API e validação direta na base de dados para as mesmas regras de negócio.

**Fora do escopo (nesta fase):**
- Testes de performance/carga (JMeter) — o projeto já disponibiliza um plano JMeter oficial, mas fica documentado como extensão futura, após aprendizagem dedicada de JMeter/BlazeMeter (prioridade de 2026)
- Testes de penetração/segurança ofensiva aprofundados (apenas controlo de acesso funcional está incluído, não pentesting)
- Internacionalização/localização
- Testes de compatibilidade cross-browser além do Chrome (pode ser considerado como extensão futura)

### 4. Itens de teste (funcionalidades sob teste)

| Módulo | Descrição |
|---|---|
| Owners | Registo, edição, pesquisa e remoção de donos de animais |
| Pets | Registo e gestão de animais associados a um owner |
| PetTypes | Gestão de espécies/tipos de animal |
| Vets | Registo e gestão de veterinários |
| Specialties | Gestão de especialidades associadas a veterinários |
| Visits | Agendamento e histórico de consultas |
| Users & Auth | Criação de utilizadores, autenticação e controlo de acesso por role |
| UI/UX | Navegação, formulários, feedback visual, consistência de padrões de interface entre módulos |

### 5. Abordagem e Estratégia de Testes

**Níveis de teste aplicados:**
- Testes manuais funcionais (baseados em test cases formais)
- Testes exploratórios (sessões time-boxed sobre áreas de maior risco/ambiguidade)
- Testes de API (Postman — funcionais, negativos, BVA)
- Testes de integridade de dados (SQL sobre PostgreSQL)
- Testes de automação de UI (Selenium + Python, padrão Page Object Model)
- Testes de controlo de acesso (autenticação/autorização por role)
- Testes manuais de UI/UX, focados em navegação, formulários, feedback visual e consistência de padrões de interface
**Técnicas de design de teste utilizadas** (alinhadas com ISTQB Foundation Level):
- Particionamento de equivalência (Equivalence Partitioning)
- Análise de valores de fronteira (Boundary Value Analysis)
- Tabelas de decisão (para regras de negócio com múltiplas condições, ex: permissões por role)
- Testes baseados em erro (Error Guessing) — sobretudo nas ambiguidades já identificadas
- Testes baseados em risco (Risk-Based Testing) — priorização dos fluxos críticos definidos na Semana 1
- Revisão de consistência de UX (comparação de padrões entre módulos da interface) — aplicada com base no meu background de design gráfico

**Priorização:** os testes seguem a priorização de risco definida na Semana 1 — maior atenção a: registo owner→pet, agendamento de visitas, autenticação/autorização de API, e pesquisa.

### 6. Critérios de Entrada

- Ambiente local a correr com sucesso via Docker (perfil PostgreSQL)
- Acesso ao Swagger UI e à documentação OpenAPI do produto
- Test Plan e Test Design concluídos e revistos antes do início da execução.
- Ferramentas configuradas: Postman, Jira, Confluence, GitHub, GitHub Actions, Docker

### 7. Critérios de Saída

- 100% dos test cases das funcionalidades críticas executados (mesmo que com defeitos documentados)
- Todos os defeitos encontrados reportados e priorizados no Jira
- Suite de automação planeada implementada e executada no pipeline de CI, com todos os testes críticos automatizados executados e resultados documentados.
- Documentação final publicada no Confluence
- Nenhum defeito crítico/bloqueante em aberto sem avaliação de impacto, evidência e justificação documentada.

### 8. Ambiente de Teste

- **Aplicação:** Spring PetClinic REST, corrida via Docker (`docker-compose --profile postgres up`)
- Front-end: Spring PetClinic Angular, servido via Vite dev server em container Node (node:22), acessível em http://localhost:4200. O ambiente completo (backend + PostgreSQL + front-end) corre através de um único docker-compose.yml, com os três serviços na mesma rede Docker.
- **Base de dados:** PostgreSQL 16 (containerizado)
- **Documentação da API:** Swagger UI (`/petclinic/swagger-ui.html`) e OpenAPI spec
- **Ferramentas:** Postman (API), Selenium + Python (UI), pgAdmin ou DBeaver (SQL), Jira (bugs), Confluence (documentação), GitHub + GitHub Actions (versionamento e CI)

### 9. Entregáveis de Teste

- Test Plan (este documento)
- Test Design (Parte 2 deste documento)
- Test Cases detalhados (AIO Tests + Jira)
- Relatórios de bugs (Jira)
- Suite de automação (repositório GitHub)
- Relatórios de execução de CI (GitHub Actions)
- Relatório final de resultados (Confluence)

### 10. Papéis e Responsabilidades

Como projeto individual, assumo os três papéis normalmente distribuídos numa equipa de QA — uma forma deliberada de demonstrar visão completa do processo:
- **Test Analyst:** análise de requisitos, design de testes, execução manual
- **QA Automation Engineer:** automação UI/API, integração de CI
- **Test Lead:** planeamento, priorização de risco, reporting final

### 11. Cronograma (ajustado a 10-15h/semana)

| Semana | Foco |
|---|---|
| 1 ✅ | Definição do produto, escopo e apresentação inicial |
| 2 ✅ | Test Plan + Test Design |
| 3 🔄 | Test Cases detalhados + testes exploratórios + primeiros bug reports (Jira) |
| 4 | Automação de UI — setup Selenium + POM sobre fluxos críticos |
| 5 | Automação de UI (continuação) + testes de API (Postman), incluindo autorização |
| 6 | Validação de dados (SQL/PostgreSQL) + consolidação da suite de automação |
| 7 | Containerização (Docker) + pipeline de CI (GitHub Actions) |
| 8 | Documentação final (Confluence) + relatório final + apresentação final |

### 12. Riscos e Contingências

| Risco | Mitigação |
|---|---|
| Tempo definido (10-15h/semana) para o escopo definido | Priorização por risco: funcionalidades críticas primeiro; scope claramente delimitado |
| Inclusão de testes de autorização aumenta o esforço | Integrado nas fases já existentes (manual + API), sem criar fase extra |
| Ambiguidades de regras de negócio podem consumir tempo de investigação | Documentadas antecipadamente (secção de ambiguidades); tratadas como parte do exploratory testing |
| Complexidade de setup (Docker, ambiente) | Testado previamente na Semana 1; scripts e comandos já documentados |
| Risco de dispersão de escopo | Escopo fechado neste documento; JMeter e pentesting explicitamente fora de escopo |

### 13. Ferramentas — Resumo

Python, Selenium, Postman, PostgreSQL/SQL, Jira, Confluence, GitHub, GitHub Actions, Docker.

### 14. Test Data Management

| Dados pré-existentes fornecidos pela aplicação serão utilizados como baseline. |
| Serão criados dados de teste específicos para cenários positivos e negativos. |
| IDs e entidades relacionadas serão controlados para evitar dependências entre testes. |
| Serão utilizados dados válidos, inválidos, limites e duplicados conforme a técnica de teste aplicada. |
| Dados utilizados nos testes de API serão documentados no Postman. |
| Quando necessário, o estado da base de dados será validado antes/depois da execução através de SQL. |
| Credenciais e dados sensíveis não serão armazenados diretamente no repositório. |
