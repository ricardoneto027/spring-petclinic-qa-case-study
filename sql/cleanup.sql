-- =====================================================================
-- Repõe a BD do PetClinic ao estado do seed, apagando os dados deixados pelos testes.
-- ATENÇÃO: apaga dados! Usa só no ambiente local de testes.
--
-- Critérios (seed do PetClinic: owners 1-10, pets 1-13, visits 1-4):
--   - visits com id > 4, pets com id > 13, owners com id > 10
--   - utilizadores criados pela API, identificados por a password não ser um hash BCrypt
--     (o utilizador admin tem hash e é preservado), e as respetivas roles
--
-- Execução (a partir da raiz do repo):
--   docker exec -i petclinic-postgres psql -U petclinic -d petclinic < sql/cleanup.sql
-- =====================================================================
\pset pager off
BEGIN;

\echo '--- Antes'
SELECT 'owners' AS tabela, COUNT(*) AS n FROM owners
UNION ALL SELECT 'pets', COUNT(*) FROM pets
UNION ALL SELECT 'visits', COUNT(*) FROM visits
UNION ALL SELECT 'users', COUNT(*) FROM users
UNION ALL SELECT 'roles', COUNT(*) FROM roles;

DELETE FROM visits WHERE id > 4;
DELETE FROM pets   WHERE id > 13;
DELETE FROM owners WHERE id > 10;
DELETE FROM roles  WHERE username IN (SELECT username FROM users WHERE password !~ '^\$2[aby]\$');
DELETE FROM users  WHERE password !~ '^\$2[aby]\$';

\echo '--- Depois (esperado: owners 10, pets 13, visits 4)'
SELECT 'owners' AS tabela, COUNT(*) AS n FROM owners
UNION ALL SELECT 'pets', COUNT(*) FROM pets
UNION ALL SELECT 'visits', COUNT(*) FROM visits
UNION ALL SELECT 'users', COUNT(*) FROM users
UNION ALL SELECT 'roles', COUNT(*) FROM roles;

COMMIT;
