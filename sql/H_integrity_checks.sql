-- =====================================================================
-- Módulo H — Integridade de Dados (SQL) · Spring PetClinic REST
-- Casos AIO: SPRINGQA-TC-70, 71, 72 e 73
-- (TC-74 e TC-75 estão nos scripts tc74_api_vs_db.sh e tc75_persistence.sh)
--
-- Execução (a partir da raiz do repo; só faz SELECT, não altera dados):
--   docker exec -i petclinic-postgres psql -U petclinic -d petclinic < sql/H_integrity_checks.sql
--
-- Convenção: cada verificação devolve as linhas "más".
--   0 linhas  = PASS
--   >0 linhas = FAIL (ou observação, quando indicado)
-- =====================================================================
\pset pager off

\echo
\echo '=== TC-70 · Chaves estrangeiras: nenhuma referência quebrada ==='

\echo '--- 70.1 pets.owner_id aponta para owner inexistente (esperado: 0 linhas)'
SELECT p.id AS pet_id, p.owner_id
FROM pets p
LEFT JOIN owners o ON o.id = p.owner_id
WHERE p.owner_id IS NOT NULL AND o.id IS NULL;

\echo '--- 70.2 pets.type_id aponta para tipo inexistente (esperado: 0 linhas)'
SELECT p.id AS pet_id, p.type_id
FROM pets p
LEFT JOIN types t ON t.id = p.type_id
WHERE t.id IS NULL;

\echo '--- 70.3 visits.pet_id aponta para pet inexistente (esperado: 0 linhas)'
SELECT v.id AS visit_id, v.pet_id
FROM visits v
LEFT JOIN pets p ON p.id = v.pet_id
WHERE v.pet_id IS NOT NULL AND p.id IS NULL;

\echo '--- 70.4 vet_specialties com vet ou especialidade inexistente (esperado: 0 linhas)'
SELECT vs.vet_id, vs.specialty_id
FROM vet_specialties vs
LEFT JOIN vets v ON v.id = vs.vet_id
LEFT JOIN specialties s ON s.id = vs.specialty_id
WHERE v.id IS NULL OR s.id IS NULL;

\echo '--- 70.5 roles.username sem utilizador (esperado: 0 linhas)'
SELECT r.id AS role_id, r.username
FROM roles r
LEFT JOIN users u ON u.username = r.username
WHERE u.username IS NULL;

\echo '--- 70.6 (informativo) FKs declaradas e regra ON DELETE'
\echo '    Se nenhuma FK tiver CASCADE, os apagamentos em cascata vistos na API'
\echo '    (SPRINGQA-9 e SPRINGQA-23) vêm da aplicação e não da base de dados.'
SELECT conrelid::regclass AS tabela,
       conname AS fk,
       pg_get_constraintdef(oid) AS definicao,
       CASE confdeltype
            WHEN 'a' THEN 'NO ACTION'
            WHEN 'r' THEN 'RESTRICT'
            WHEN 'c' THEN 'CASCADE'
            WHEN 'n' THEN 'SET NULL'
            WHEN 'd' THEN 'SET DEFAULT'
       END AS on_delete
FROM pg_constraint
WHERE contype = 'f'
ORDER BY 1, 2;

\echo
\echo '=== TC-71 · Registos órfãos ==='

\echo '--- 71.1 pets sem owner (owner_id NULL) (esperado: 0 linhas)'
SELECT id AS pet_id, name
FROM pets
WHERE owner_id IS NULL;

\echo '--- 71.2 visits sem pet (pet_id NULL) (esperado: 0 linhas)'
SELECT id AS visit_id, visit_date, description
FROM visits
WHERE pet_id IS NULL;

\echo
\echo '=== TC-72 · Unicidade ==='

\echo '--- 72.1 usernames duplicados em users (esperado: 0 linhas; a PK já o garante)'
SELECT username, COUNT(*) AS n
FROM users
GROUP BY username
HAVING COUNT(*) > 1;

\echo '--- 72.2 pares (username, role) duplicados em roles (esperado: 0 linhas)'
SELECT username, role, COUNT(*) AS n
FROM roles
GROUP BY username, role
HAVING COUNT(*) > 1;

\echo '--- 72.3 (regra de negócio, sem constraint na BD) owners duplicados: mesmo nome e telefone'
\echo '    Linhas = a API deixou criar duplicados (SPRINGQA-21, TC-13)'
SELECT first_name, last_name, telephone, COUNT(*) AS n
FROM owners
GROUP BY first_name, last_name, telephone
HAVING COUNT(*) > 1;

\echo '--- 72.4 (regra de negócio) tipos de pet duplicados, ignorando maiúsculas (TC-34)'
SELECT lower(name) AS nome, COUNT(*) AS n
FROM types
GROUP BY lower(name)
HAVING COUNT(*) > 1;

\echo '--- 72.5 (regra de negócio) especialidades duplicadas, ignorando maiúsculas (TC-46)'
SELECT lower(name) AS nome, COUNT(*) AS n
FROM specialties
GROUP BY lower(name)
HAVING COUNT(*) > 1;

\echo '--- 72.6 (regra de negócio) visitas duplicadas: mesmo pet e mesmo dia (TC-54)'
SELECT pet_id, visit_date, COUNT(*) AS n
FROM visits
GROUP BY pet_id, visit_date
HAVING COUNT(*) > 1;

\echo
\echo '=== TC-73 · Constraints da BD vs validações da API ==='

\echo '--- 73.1 Esquema: tipos, tamanhos e NULL por coluna'
SELECT table_name, column_name, data_type, character_maximum_length AS max_len, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('owners','pets','visits','vets','types','specialties','users','roles')
ORDER BY table_name, ordinal_position;

\echo '--- 73.2 Colunas de texto sem limite de tamanho (a API impõe limites que a BD não garante)'
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public'
  AND data_type = 'text'
  AND table_name IN ('owners','pets','visits','vets','types','specialties')
ORDER BY 1, 2;

\echo '--- 73.3 Dados já na BD que a API deveria ter rejeitado'
\echo '    (a) telefones que não são só dígitos ou têm mais de 20 caracteres'
SELECT id, first_name, last_name, telephone
FROM owners
WHERE telephone IS NOT NULL
  AND (telephone !~ '^[0-9]+$' OR length(telephone) > 20);

\echo '    (b) nomes de pet vazios ou só com espaços (TC-28)'
SELECT id, name, owner_id
FROM pets
WHERE name IS NULL OR btrim(name) = '';

\echo '    (c) pets com data de nascimento no futuro'
SELECT id, name, birth_date
FROM pets
WHERE birth_date > CURRENT_DATE;

\echo '--- 73.4 Limite do username na BD (varchar(20)); a API devolveu 404 acima disto (SPRINGQA-20)'
SELECT character_maximum_length AS username_max_len
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'users' AND column_name = 'username';

\echo '--- 73.5 Passwords guardadas sem hash BCrypt (SPRINGQA-26); um hash BCrypt começa por $2'
SELECT username, enabled, left(password, 4) AS inicio_password
FROM users
WHERE password !~ '^\$2[aby]\$'
ORDER BY username;

\echo
\echo '=== Observações adicionais (fora dos TCs) ==='

\echo '--- O.1 Índices duplicados (mesma definição, nomes diferentes)'
SELECT tablename,
       regexp_replace(indexdef, 'INDEX \S+ ON', 'INDEX <nome> ON') AS definicao,
       COUNT(*) AS n,
       array_agg(indexname ORDER BY indexname) AS nomes
FROM pg_indexes
WHERE schemaname = 'public'
GROUP BY tablename, regexp_replace(indexdef, 'INDEX \S+ ON', 'INDEX <nome> ON')
HAVING COUNT(*) > 1;

\echo '--- O.2 Contagem de registos por tabela (linha de base; seed original ≈ 10 owners, 13 pets, 4 visits)'
SELECT 'owners' AS tabela, COUNT(*) AS n FROM owners
UNION ALL SELECT 'pets', COUNT(*) FROM pets
UNION ALL SELECT 'visits', COUNT(*) FROM visits
UNION ALL SELECT 'vets', COUNT(*) FROM vets
UNION ALL SELECT 'types', COUNT(*) FROM types
UNION ALL SELECT 'specialties', COUNT(*) FROM specialties
UNION ALL SELECT 'users', COUNT(*) FROM users
UNION ALL SELECT 'roles', COUNT(*) FROM roles;
