# Test Results · Spring PetClinic REST
### Projeto de Portfólio QA (PAC) · Relatório de resultados

**Autor:** Ricardo Peres | **Produto sob teste:** Spring PetClinic REST e Spring PetClinic Angular | **Data:** Outubro 2026

Este documento consolida os resultados de todas as camadas de teste definidas no [Test Plan](test-plan.md) e no [Test Design](test-design.md). A fonte dos casos de teste e da execução manual é o AIO Tests (Jira); a fonte dos defeitos é o Jira (projeto `SPRINGQA`). Os dois são privados, por isso os resultados ficam aqui registados.

**Ambiente:** Docker Compose com PostgreSQL 16.3, backend `springcommunity/spring-petclinic-rest` (porta 9966) e frontend `spring-petclinic-angular` (porta 4200). Na CI, o frontend está fixado no commit `1978a75`.

---

## 1. Resumo

| Camada | Ferramenta | Âmbito | Resultado |
|---|---|---|---|
| Manual | AIO Tests | 106 casos, módulos A a J | 98 executados manualmente: 52 Pass, 31 Fail, 15 Blocked · os outros 8 são casos só de API, cobertos pela suite Newman |
| API | Postman + Newman | 74 pedidos, 73 casos AIO | Segurança OFF: 29 de 165 asserções falham · ON: 39 de 173 · todas são bugs conhecidos |
| UI | Playwright + Pytest (POM) | 8 testes automatizados | 4 Pass, 4 xfail (bugs conhecidos), 0 Fail |
| Base de dados | SQL (PostgreSQL) | 6 casos, módulo H | 5 Pass, 1 Fail |
| CI | GitHub Actions | 2 pipelines (API e UI) | Verdes: falham apenas com regressões novas |
| Defeitos | Jira | 30 registados | 29 válidos (2 de severidade Crítica, 5 Alta, 13 Média, 9 Baixa) |

Um caso com Fail não corresponde a um bug novo: vários casos de teste podem falhar pela mesma causa (por exemplo, o SPRINGQA-17 faz falhar os casos TC-8, TC-9 e TC-27).

---

## 2. Execução manual (AIO Tests)

### 2.1 Resultados por módulo

| Módulo | Casos no AIO | Pass | Fail | Blocked | Só API |
|---|---:|---:|---:|---:|---:|
| A. Owners | 20 | 10 | 8 | 0 | 2 |
| B. Pets | 12 | 5 | 1 | 3 | 3 |
| C. PetTypes | 5 | 3 | 2 | 0 | 0 |
| D. Vets | 6 | 3 | 1 | 1 | 1 |
| E. Specialties | 4 | 1 | 3 | 0 | 0 |
| F. Visits | 10 | 0 | 0 | 8 | 2 |
| G. Users & Auth | 11 | 4 | 4 | 3 | 0 |
| H. Integridade de Dados (SQL) | 6 | 5 | 1 | 0 | 0 |
| I. API | 6 | 3 | 3 | 0 | 0 |
| J. UI/UX | 26 | 18 | 8 | 0 | 0 |
| **Total** | **106** | **52** | **31** | **15** | **8** |

**Só API:** nos módulos A, B, D e F, alguns casos testam a API diretamente (por exemplo, pedidos com IDs inexistentes) e não têm passos na interface. Não foram executados manualmente, porque são cobertos pela suite de API (secção 3), que inclui todos os casos destes módulos com componente de API.

As 82 condições do Test Design deram origem a 106 casos de teste. Algumas condições foram desdobradas em vários casos (por exemplo, cada campo obrigatório em falta no módulo A tem o seu próprio caso).

### 2.2 Bloqueios

- **D. Vets:** o TC-43 (apagar vet com visitas associadas) está bloqueado. Devido a um erro de UI, não é possível confirmar que vet tem visitas associadas a que pets.
- **F. Visits:** a UI não permite verificar visitas, porque a página de detalhe do owner não mostra pets nem visitas (SPRINGQA-6). As visitas foram validadas pela API (secção 3), onde só o TC-54 falha.
- **G. Users & Auth:** TC-61, TC-62 e TC-63 estão bloqueados pelo SPRINGQA-26. Os utilizadores criados pela API não se conseguem autenticar, por isso não é possível testar as permissões por role.

---

## 3. Testes de API (Postman + Newman)

A coleção `api-tests/postman/PetClinic.postman_collection.json` tem 74 pedidos e cobre 73 casos do AIO (módulos A a G e I). Corre em dois modos: com a segurança da API desligada (defeito da aplicação) e ligada (HTTP Basic). Com a segurança ligada, os testes do módulo G (utilizadores e roles) correm por completo, o que explica as asserções e as falhas a mais.

| | Segurança OFF | Segurança ON |
|---|---:|---:|
| Pedidos da coleção | 74 | 74 |
| Asserções | 165 | 173 |
| Asserções falhadas | 29 | 39 |
| Casos AIO com falha | 16 | 23 |
| Falhas fora da baseline (regressões) | 0 | 0 |

### 3.1 Execuções guardadas

| Execução | Data | Pasta | Função |
|---|---|---|---|
| Local (referência) | 10/10/2026 | `api-tests/postman/results/` e `api-tests/postman/reports/` | Evidência citada nos bugs do Jira e nos casos do AIO |
| CI (GitHub Actions) | 12/10/2026 | `reports/api-results-sec-off/` e `reports/api-results-sec-on/` | Inclui também a saída das verificações SQL do módulo H |

As duas execuções têm exatamente os mesmos números.

### 3.2 Baseline de falhas conhecidas

A suite inclui testes que falham de propósito, porque documentam bugs abertos. Para que o pipeline não fique sempre vermelho nem esconda problemas novos, `ci/check_newman_results.py` compara cada execução com `ci/known-failures-sec-off.txt` e `ci/known-failures-sec-on.txt`:

- falha nova num caso que não está na lista: o pipeline falha (regressão);
- caso da lista que passa a passar: aviso (o bug pode ter sido corrigido e deve ser retestado);
- execução sem pedidos: o pipeline falha.

| Caso(s) AIO | Bug | Modo |
|---|---|---|
| TC-8, TC-9, TC-27 | SPRINGQA-17 | OFF e ON |
| TC-13 | SPRINGQA-21 | OFF e ON |
| TC-17, TC-47 | SPRINGQA-20 | OFF e ON |
| TC-18 | SPRINGQA-5 | OFF e ON |
| TC-28 | SPRINGQA-22 | OFF e ON |
| TC-30 | SPRINGQA-23 | OFF e ON |
| TC-34 | SPRINGQA-8 | OFF e ON |
| TC-36 | SPRINGQA-9 | OFF e ON |
| TC-46 | SPRINGQA-11 | OFF e ON |
| TC-54 | SPRINGQA-25 | OFF e ON |
| TC-78 | SPRINGQA-24 | OFF e ON |
| TC-79 | SPRINGQA-19 | OFF e ON |
| TC-80 | SPRINGQA-18 | OFF e ON |
| TC-60 | SPRINGQA-27 | Só ON |
| TC-61, TC-62, TC-63 | SPRINGQA-26 (bloqueados) | Só ON |
| TC-66 | SPRINGQA-20 | Só ON |
| TC-67 | SPRINGQA-28 | Só ON |
| TC-69 | SPRINGQA-24 | Só ON |

---

## 4. Automação UI (Playwright + Pytest)

Última execução: GitHub Actions, 21/10/2026, Chromium headless. Relatórios em `reports/ui-results/` (`junit-ui.xml` e `report-ui.html`).

| Teste automatizado | Caso AIO | Resultado | Bug |
|---|---|---|---|
| `test_owners.py::test_criar_owner_valido` (TC-OWN-01) | SPRINGQA-TC-1 | Pass | |
| `test_owners.py::test_criar_owner_telefone_9_digitos_bug_conhecido` | SPRINGQA-TC-9 | xfail | SPRINGQA-3 |
| `test_pets.py::test_adicionar_pet_valido` (TC-PET-01) | SPRINGQA-TC-21 | xfail | SPRINGQA-6 |
| `test_pets.py::test_adicionar_pet_data_nascimento_futura_bug_conhecido` (TC-PET-04) | SPRINGQA-TC-24 | xfail | SPRINGQA-7 |
| `test_specialties.py::test_criar_specialty_valida` | SPRINGQA-TC-45 | Pass | |
| `test_vets.py::test_criar_vet_com_especialidade` | SPRINGQA-TC-39 | Pass | |
| `test_vets.py::test_criar_vet_sem_especialidade` | SPRINGQA-TC-40 | Pass | |
| `test_visits.py::test_adicionar_visita_valida` | SPRINGQA-TC-49 | xfail | SPRINGQA-6 |

**xfail** significa "falha esperada": o teste descreve o comportamento correto e falha enquanto o bug estiver aberto. Quando o bug for corrigido, o teste passa a passar (`XPASS`) e a marcação é retirada. Os testes de bugs conhecidos ficam na suite em vez de serem apagados, para documentarem o defeito e detetarem a correção.

**Histórico:** a primeira execução na CI (12/10/2026) teve 2 falhas, em Specialties e Vets. A causa era uma race condition: em modo headless, o teste verificava a lista de specialties antes de ela acabar de carregar. Localmente, com o browser em câmara lenta, não aparecia. Foi corrigida no commit `c417728`: em vez de ler a lista uma única vez logo após o "Save", o teste espera ativamente até o valor aparecer (com limite de tempo).

---

## 5. Integridade de dados (SQL · módulo H)

Scripts: `sql/H_integrity_checks.sql` (só `SELECT`, não altera dados), `sql/tc74_api_vs_db.sh` e `sql/tc75_persistence.sh`. Cada verificação devolve as linhas "más": 0 linhas é Pass.

Execução manual a 10/10/2026 (`sql/H_integrity_after_runs.txt`). As verificações correm também no fim de cada pipeline de API (`reports/api-results-*/H_integrity-*.txt`).

| Caso | Verificação | Resultado | Bug |
|---|---|---|---|
| TC-70 | Chaves estrangeiras: nenhuma referência quebrada | Pass | |
| TC-71 | Nenhum registo órfão (pets sem owner, visitas sem pet) | Pass | |
| TC-72 | Unicidade (usernames, pares username/role) | Pass | |
| TC-73 | Constraints da BD vs validações da API | Fail | SPRINGQA-20, 22, 26, 28, 30 |
| TC-74 | Resposta da API igual aos dados gravados na BD | Pass | |
| TC-75 | Dados persistem após reinício dos containers | Pass | |

Principais resultados do TC-73: 12 passwords guardadas sem hash BCrypt (SPRINGQA-26), colunas de texto sem limite de tamanho na BD apesar de a API impor limites, e um utilizador gravado com o nome literal `{{dupUser}}` (SPRINGQA-30).

**Observação O.1:** a cada arranque do backend é criada uma cópia nova de 7 índices (4 cópias, depois 6, depois 7, em três medições). Registado como SPRINGQA-29. Não afeta a funcionalidade, mas desperdiça espaço e torna as escritas mais lentas.

---

## 6. Defeitos (Jira)

30 bugs registados. O SPRINGQA-1 foi fechado como duplicado do SPRINGQA-3 depois do reteste com um telefone de 10 dígitos, por isso ficam **29 defeitos válidos**, todos com prioridade e severidade definidas.

### 6.1 Prioridade × Severidade

| Prioridade \ Severidade | Crítica | Alta | Média | Baixa | Total |
|---|---:|---:|---:|---:|---:|
| Highest | 1 | 2 | 0 | 0 | 3 |
| High | 1 | 3 | 5 | 0 | 9 |
| Medium | 0 | 0 | 6 | 4 | 10 |
| Low | 0 | 0 | 2 | 5 | 7 |
| **Total** | **2** | **5** | **13** | **9** | **29** |

A severidade mede o impacto no produto; a prioridade mede a urgência da correção. Por isso não coincidem sempre: o SPRINGQA-11 (specialty duplicada) tem severidade Crítica e prioridade High.

### 6.2 Onde foram encontrados

| Camada | Bugs | Quantidade |
|---|---|---:|
| UI (execução manual) | SPRINGQA-2 a 16 | 15 |
| API (Postman/Newman) | SPRINGQA-17 a 28 | 12 |
| Base de dados (SQL) | SPRINGQA-29 e 30 | 2 |

### 6.3 Lista completa

| ID | Título | Prioridade | Severidade | Camada | Caso(s) AIO |
|---|---|---|---|---|---|
| SPRINGQA-1 | Criar owner com dados válidos falha (telefone de 9 dígitos). *Fechado, duplicado do SPRINGQA-3* | Highest | Alta | UI | TC-1 |
| SPRINGQA-2 | Telefone abaixo do limite mínimo rejeitado sem mensagem | High | Média | UI | TC-8 |
| SPRINGQA-3 | O backend exige telefone com exatamente 10 dígitos e a rejeição é silenciosa na UI | High | Alta | UI | TC-8, TC-9 |
| SPRINGQA-4 | Nomes com acentuação PT-PT rejeitados pela UI e aceites pela API | Medium | Média | UI | TC-5, TC-11 |
| SPRINGQA-5 | Pesquisa de owner por nome parcial | Medium | Média | UI | TC-18 |
| SPRINGQA-6 | O detalhe do owner não mostra dados, pets nem visitas | Highest | Alta | UI | TC-21 |
| SPRINGQA-7 | Erros de validação na criação de pet não aparecem ao utilizador | Highest | Alta | UI | TC-24 |
| SPRINGQA-8 | PetType duplicado aceite | High | Média | UI | TC-34 |
| SPRINGQA-9 | Apagar um PetType em uso apaga os pets associados (perda de dados) | Highest | Crítica | UI | TC-36 |
| SPRINGQA-10 | Não é possível criar um vet com várias especialidades | High | Média | UI | TC-41 |
| SPRINGQA-11 | Specialty duplicada aceite | High | Crítica | UI | TC-46 |
| SPRINGQA-12 | Apagar uma specialty associada a um vet não mostra um erro claro | Low | Média | UI | TC-47 |
| SPRINGQA-13 | Specialty com nome vazio não mostra erro na UI | Low | Média | UI | TC-48 |
| SPRINGQA-14 | Campos obrigatórios sem indicação visual em "New Owner" | Medium | Baixa | UI | TC-85 |
| SPRINGQA-15 | Listagem de owners sem paginação | Medium | Baixa | UI | TC-94 |
| SPRINGQA-16 | "Back" descarta os dados preenchidos sem aviso | Medium | Média | UI | TC-96 |
| SPRINGQA-17 | Erros de validação devolvem 500 em vez de 400 | High | Média | API | TC-8, TC-9, TC-27 |
| SPRINGQA-18 | JSON malformado devolve 500 em vez de 400 | Medium | Baixa | API | TC-80 |
| SPRINGQA-19 | Método HTTP não suportado devolve 500 em vez de 405 | Medium | Baixa | API | TC-79 |
| SPRINGQA-20 | Violação de integridade referencial devolve 404 em vez de 409 | High | Média | API | TC-17, TC-47, TC-66 |
| SPRINGQA-21 | Owner duplicado aceite | Medium | Média | API | TC-13 |
| SPRINGQA-22 | Pet com nome só com espaços aceite | Low | Baixa | API | TC-28 |
| SPRINGQA-23 | Apagar um pet apaga as suas visitas (perda de dados) | High | Alta | API | TC-30 |
| SPRINGQA-24 | Formato de erro inconsistente (404 sem corpo, outros com ProblemDetail) | Low | Baixa | API | TC-69, TC-78 |
| SPRINGQA-25 | Duas visitas no mesmo dia para o mesmo pet | Low | Baixa | API | TC-54 |
| SPRINGQA-26 | Utilizadores criados não se autenticam; password guardada em texto simples | High | Alta | API | TC-61, TC-62, TC-63, TC-73 |
| SPRINGQA-27 | Role inexistente aceite em `POST /users` | Medium | Média | API | TC-60 |
| SPRINGQA-28 | Password de 2 caracteres aceite | Medium | Média | API | TC-67, TC-73 |
| SPRINGQA-29 | Índices duplicados a cada arranque do backend | Low | Baixa | SQL | TC-75 |
| SPRINGQA-30 | Username sem validação de formato | Low | Baixa | SQL | TC-73 |

---

## 7. Rastreabilidade

Cada resultado liga-se ao resto da cadeia:

**Condição no Test Design → caso no AIO → execução (manual, API, UI ou SQL) → bug no Jira → teste automatizado que o documenta**

Exemplo: a condição C.4 do Test Design ("Apagar pet type em uso por pets existentes") deu origem ao SPRINGQA-TC-36. Na execução manual, o caso falhou e foi registado o SPRINGQA-9. Na API, o mesmo caso está na baseline de falhas conhecidas (`ci/known-failures-*.txt`), por isso a CI deteta quando o bug for corrigido.

| Camada | Casos AIO cobertos | Onde está a ligação |
|---|---:|---|
| Manual | 106 | AIO Tests (ciclos de execução) |
| API | 73 | Nome de cada pedido na coleção (`SPRINGQA-TC-n`) |
| UI automatizada | 8 | Tabela da secção 4 |
| SQL | 6 | Cabeçalho de cada verificação em `sql/H_integrity_checks.sql` |

---

## 8. Critérios de saída (Test Plan, secção 7)

| Critério | Estado |
|---|---|
| 100% dos casos das funcionalidades críticas executados | Cumprido: 98 casos executados manualmente e os 8 casos só de API executados na suite Newman |
| Todos os defeitos reportados e priorizados no Jira | Cumprido: 29 defeitos com prioridade e severidade |
| Suite de automação implementada e a correr na CI | Cumprido: pipelines de API (OFF e ON) e de UI verdes |
| Documentação final publicada no Confluence | Em curso |
| Nenhum defeito crítico em aberto sem avaliação de impacto | Cumprido: SPRINGQA-9 e SPRINGQA-11 têm impacto, evidência e passos documentados |
