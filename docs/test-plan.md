# Test Plan & Test Design — Spring PetClinic REST
### Projeto de Portfólio QA — PAC (Semana 2)
**Autor:** Ricardo Neto | **Produto sob teste:** Spring PetClinic REST | **Data:** Setembro 2026

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

### 3. Escopo

**Dentro do escopo:**
- Testes funcionais (manuais e automatizados) de: Owners, Pets, PetTypes, Vets, Specialties, Visits, Users
- Testes de autenticação e autorização (controlo de acesso por role: `OWNER_ADMIN`, `VET_ADMIN`, `ADMIN`)
- Testes de API (funcionais, negativos, BVA) via Postman
- Validação de integridade de dados na base de dados (PostgreSQL) via SQL
- Automação de UI dos fluxos críticos (Selenium + Python + Page Object Model)
- Integração contínua (GitHub Actions) e ambiente containerizado (Docker)
- Testes exploratórios sobre os fluxos críticos e de maior risco

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

### 5. Abordagem e Estratégia de Testes

**Níveis de teste aplicados:**
- Testes manuais funcionais (baseados em test cases formais)
- Testes exploratórios (sessões time-boxed sobre áreas de maior risco/ambiguidade)
- Testes de API (Postman — funcionais, negativos, BVA)
- Testes de integridade de dados (SQL sobre PostgreSQL)
- Testes de automação de UI (Selenium + Python, padrão Page Object Model)
- Testes de controlo de acesso (autenticação/autorização por role)

**Técnicas de design de teste utilizadas** (alinhadas com ISTQB Foundation Level):
- Particionamento de equivalência (Equivalence Partitioning)
- Análise de valores de fronteira (Boundary Value Analysis)
- Tabelas de decisão (para regras de negócio com múltiplas condições, ex: permissões por role)
- Testes baseados em erro (Error Guessing) — sobretudo nas ambiguidades já identificadas
- Testes baseados em risco (Risk-Based Testing) — priorização dos fluxos críticos definidos na Semana 1

**Priorização:** os testes seguem a priorização de risco definida na Semana 1 — maior atenção a: registo owner→pet, agendamento de visitas, autenticação/autorização de API, e pesquisa.

### 6. Critérios de Entrada

- Ambiente local a correr com sucesso via Docker (perfil PostgreSQL)
- Acesso ao Swagger UI e à documentação OpenAPI do produto
- Test Plan e Test Design aprovados (este documento)
- Ferramentas configuradas: Postman, Jira, Confluence, GitHub

### 7. Critérios de Saída

- 100% dos test cases das funcionalidades críticas executados (mesmo que com defeitos documentados)
- Todos os defeitos encontrados reportados e priorizados no Jira
- Suite de automação (UI + API) a correr com sucesso no pipeline de CI
- Documentação final publicada no Confluence
- Nenhum defeito crítico/bloqueante em aberto sem justificação documentada

### 8. Ambiente de Teste

- **Aplicação:** Spring PetClinic REST, corrida via Docker (`docker-compose --profile postgres up`)
- **Base de dados:** PostgreSQL 16 (containerizado)
- **Documentação da API:** Swagger UI (`/petclinic/swagger-ui.html`) e OpenAPI spec
- **Ferramentas:** Postman (API), Selenium + Python (UI), pgAdmin ou DBeaver (SQL), Jira (bugs), Confluence (documentação), GitHub + GitHub Actions (versionamento e CI)

### 9. Entregáveis de Teste

- Test Plan (este documento)
- Test Design (Parte 2 deste documento)
- Test Cases detalhados (Semana 3)
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
| 2 (atual) | Test Plan + Test Design |
| 3 | Test Cases detalhados + testes exploratórios + primeiros bug reports (Jira) |
| 4 | Automação de UI — setup Selenium + POM sobre fluxos críticos |
| 5 | Automação de UI (continuação) + testes de API (Postman), incluindo autorização |
| 6 | Validação de dados (SQL/PostgreSQL) + consolidação da suite de automação |
| 7 | Containerização (Docker) + pipeline de CI (GitHub Actions) |
| 8 | Documentação final (Confluence) + relatório final + apresentação final |

### 12. Riscos e Contingências

| Risco | Mitigação |
|---|---|
| Tempo limitado (10-15h/semana) para o escopo definido | Priorização por risco: funcionalidades críticas primeiro; scope claramente delimitado |
| Inclusão de testes de autorização aumenta o esforço | Integrado nas fases já existentes (manual + API), sem criar fase extra |
| Ambiguidades de regras de negócio podem consumir tempo de investigação | Documentadas antecipadamente (secção de ambiguidades); tratadas como parte do exploratory testing |
| Complexidade de setup (Docker, ambiente) | Testado previamente na Semana 1; scripts e comandos já documentados |
| Risco de dispersão de escopo | Escopo fechado neste documento; JMeter e pentesting explicitamente fora de escopo |

### 13. Ferramentas — Resumo

Python, Selenium, Postman, PostgreSQL/SQL, Jira, Confluence, GitHub, GitHub Actions, Docker.