# Test Plan & Test Design — Spring PetClinic REST
### Projeto de Portfólio QA — PAC (Semana 2)
**Autor:** Ricardo Neto | **Produto sob teste:** Spring PetClinic REST | **Data:** Setembro 2026

---

## TEST DESIGN

*Técnicas aplicadas: EP = Equivalence Partitioning | BVA = Boundary Value Analysis | DT = Decision Table | EG = Error Guessing | RB = Risk-Based*

### A. Owners

1. Criar owner com todos os campos válidos [positivo]
2. Criar owner com campos obrigatórios em falta (nome, apelido, morada, telefone) [EP-inválida]
3. Telefone com formato inválido (letras, símbolos) [EP-inválida]
4. Telefone no limite mínimo/máximo de comprimento aceite [BVA]
5. Nome/apelido com acentuação e caracteres PT-PT [EP]
6. Nome/apelido com comprimento excessivo (>255 caracteres) [BVA]
7. Criar owner duplicado (mesmo nome + telefone) — validar regra de negócio [EG/RB]
8. Atualizar owner existente com dados válidos [positivo]
9. Atualizar owner com ID inexistente [negativo]
10. Apagar owner sem pets associados [positivo]
11. Apagar owner **com** pets associados — validar comportamento (cascade/bloqueio/erro) [RB — ambiguidade Semana 1]
12. Pesquisar owner por nome parcial, case-insensitive [funcional]
13. Obter owner por ID inexistente → validar código de erro (404) [negativo]

### B. Pets

1. Adicionar pet válido a owner existente [positivo]
2. Adicionar pet a owner inexistente [negativo]
3. Adicionar pet sem PetType associado [EP-inválida]
4. Data de nascimento no futuro [EG/BVA — regra de negócio]
5. Data de nascimento no limite (hoje, ontem) [BVA]
6. Nome de pet vazio ou só espaços [EP-inválida]
7. Atualizar detalhes de um pet existente [positivo]
8. Apagar pet com visitas associadas — validar comportamento [RB — ambiguidade]
9. Obter pet por ID válido/inválido [positivo/negativo]

### C. PetTypes

1. Criar pet type válido (ex: "Dog") [positivo]
2. Criar pet type duplicado — validar se é permitido [EG]
3. Criar pet type com nome vazio [EP-inválida]
4. Apagar pet type em uso por pets existentes — validar integridade [RB]
5. Listar todos os pet types [funcional]

### D. Vets

1. Criar vet válido com especialidade(s) associada(s) [positivo]
2. Criar vet sem especialidade — validar se é permitido [EG]
3. Criar vet com múltiplas especialidades [positivo]
4. Atualizar dados de um vet [positivo]
5. Apagar vet com visitas associadas — validar comportamento [RB]
6. Obter vet inexistente → validar 404 [negativo]

### E. Specialties

1. Criar especialidade válida [positivo]
2. Criar especialidade duplicada [negativo]
3. Apagar especialidade associada a um vet — validar comportamento [RB]
4. Nome de especialidade vazio [EP-inválida]

### F. Visits

1. Criar visita válida associada a pet existente [positivo]
2. Criar visita com data futura vs passada — validar regra de negócio [EG]
3. Criar visita para pet inexistente [negativo]
4. Criar visita sem descrição — validar se é obrigatória [EP]
5. Duas visitas sobrepostas para o mesmo pet — validar se é permitido [RB — ambiguidade Semana 1]
6. Atualizar visita existente [positivo]
7. Apagar visita existente [positivo]
8. Listar visitas de um pet específico [funcional]
9. Validar ausência de ligação direta Visit→Vet no modelo — confirmar se é intencional [RB — ambiguidade]

### G. Users & Autorização *(agora em escopo)*

1. Criar utilizador com role válida (`OWNER_ADMIN`) [positivo]
2. Criar utilizador com role inexistente/inválida [negativo]
3. Aceder a endpoints de Owners com `OWNER_ADMIN` → permitido [DT — controlo de acesso]
4. Aceder a endpoints de Owners com `VET_ADMIN` → deve bloquear (403) [DT — controlo de acesso]
5. Aceder a endpoints de Users sem ser `ADMIN` → deve bloquear (403) [DT]
6. Aceder a qualquer endpoint sem autenticação (com segurança ativa) → 401 [negativo]
7. Login com credenciais inválidas → 401 [negativo]
8. Criar utilizador com username duplicado [negativo]
9. Password vazia ou muito curta [EP/BVA]
10. Comparar comportamento do sistema com segurança ativada vs desativada — validar consistência [RB — risco identificado Semana 1]

### H. Transversal — Integridade de Dados (SQL)

1. Validar chaves estrangeiras: Pet→Owner, Pet→PetType, Visit→Pet
2. Validar ausência de registos órfãos (pets sem owner, visits sem pet)
3. Validar unicidade de campos que deveriam ser únicos (username, etc.)
4. Validar constraints da BD (NOT NULL, tamanho de campos) vs regras da API
5. Validar consistência entre resposta da API e dados persistidos na BD após cada operação CRUD

### I. Transversal — Validações de API

1. Validar códigos de estado HTTP corretos em cada cenário (200, 201, 400, 401, 403, 404, 500)
2. Validar schema/formato da resposta JSON contra a especificação OpenAPI
3. Validar mensagens de erro claras e consistentes
4. Testar métodos HTTP não suportados num endpoint [negativo]
5. Testar payloads JSON malformados [negativo — robustez]

---

**Total de condições de teste identificadas:** ~70, distribuídas pelos 7 módulos funcionais + 2 transversais. Servem de base para a conversão em test cases detalhados na Semana 3, priorizados segundo o risco definido na Semana 1.
