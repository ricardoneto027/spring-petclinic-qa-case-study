# Test Design · Spring PetClinic REST
### Projeto de Portfólio QA (PAC) · Parte 2 de 2 (Semana 2)
**Autor:** Ricardo Peres | **Produto sob teste:** Spring PetClinic REST e Spring PetClinic Angular| **Data:** Setembro 2026

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
6. Validar que os dados inseridos via UI persistem corretamente após reinício do ambiente Docker (não há perda de estado) — ✅ confirmado: pet "parrot" adicionado permaneceu após reinício via Docker

### I. Transversal — Validações de API

1. Validar códigos de estado HTTP corretos em cada cenário (200, 201, 400, 401, 403, 404, 500)
2. Validar schema/formato da resposta JSON contra a especificação OpenAPI
3. Validar mensagens de erro claras e consistentes
4. Testar métodos HTTP não suportados num endpoint [negativo]
5. Testar payloads JSON malformados [negativo — robustez]

### J. Interface & Experiência do Utilizador (UI/UX)

1. Botão "Add Owner" no formulário de novo owner aparece visualmente desativado (cinzento) com campos vazios — validar se fica ativo ao preencher todos os campos obrigatórios, e que feedback visual existe ao tentar submeter incompleto [EG/UX]
2. Mesmo padrão a validar no formulário "Add Vet" (botão "Save Vet", também cinzento por defeito) [EG/UX]
3. Nenhum campo dos formulários "New Owner" ou "New Veterinarian" mostra asterisco ou indicação visual de obrigatoriedade — validar se é intencional ou lacuna de usabilidade [UX — ambiguidade]
4. Validar se existe validação do lado do cliente (antes do submit) ou se toda a validação só ocorre após round-trip ao servidor [UX/funcional]
5. Inconsistência de padrão identificada: "Owners" e "Veterinarians" abrem a adição numa página separada; "Pet Types" e "Specialties" mostram um formulário inline expandido na mesma página. Validar se é intencional — documentar como observação de consistência, não necessariamente bug [UX — consistência]
6. Ambiguidade importante: o dropdown "Specialty" no formulário "Add Vet" só permite selecionar UMA especialidade, mas a lista mostra vets com múltiplas especialidades associadas (ex: Linda Douglas — dentistry + surgery). Validar como/se é possível associar mais do que uma especialidade a um vet através da UI, ou se isso só é possível via API/seed de dados [RB — ambiguidade]
7. Validar comportamento da pesquisa de Owners por "Last name": aceita pesquisa parcial? É case-sensitive? Qual o resultado ao clicar "Find Owner" com o campo vazio? [EP/funcional]
8. Validar se a listagem de Owners suporta paginação quando o número de registos crescer significativamente, ou se carrega tudo de uma vez [UX — escalabilidade]
9. Validar se o botão "Back" nos formulários de adição descarta dados já preenchidos sem qualquer aviso ao utilizador [UX — perda de dados]
10. Validar consistência de nomenclatura nos menus dropdown: "Owners" usa "Search", "Veterinarians" usa "All", para uma ação equivalente (listar/consultar registos) [UX — consistência de nomenclatura]
11. "Pet Types" e "Specialties" não têm menu dropdown na navbar (acesso direto), ao contrário de "Owners" e "Veterinarians" — validar se é intencional [UX — consistência de navegação]
12. Validar legibilidade/contraste dos botões desativados (cinzento sobre fundo cinzento claro) — possível questão de acessibilidade [Acessibilidade]
13. Validar responsividade do layout em ecrãs mais pequenos (tablet/mobile) — os prints disponíveis mostram apenas desktop [UX — a validar]
14. Validar se erros devolvidos pela API (ex: telefone inválido, campos em falta) são apresentados de forma clara na UI, ou apenas na consola do browser (como observámos anteriormente no erro de ligação) [UX/funcional]
15. Confirmar que a tabela de Veterinarians lida corretamente com vets sem especialidade associada (célula vazia, já visível nos prints com James Carter e Sharon Jenkins) mesmo após edição/remoção de especialidade [funcional/regressão]

---

  **Total de condições de teste identificadas:** 82, distribuídas por 10 módulos: 7 funcionais (A a G), 2 transversais (H e I) e UI/UX (J).