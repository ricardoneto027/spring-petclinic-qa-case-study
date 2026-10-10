#!/usr/bin/env bash
# SPRINGQA-TC-75 · Persistência de dados após reinício do Docker
#
# Cria um owner via API, reinicia os containers da BD e do backend, espera que a
# API volte e confirma que o registo continua na BD. No fim apaga o owner.
#
# Nota: isto testa um reinício (docker restart). Para testar também a recriação
# dos containers (sem apagar o volume), corre antes manualmente, na pasta do
# docker-compose.yml:  docker compose down && docker compose up -d
# (sem a opção -v, que apagaria o volume e os dados).
#
# Nota: cada arranque do backend parece acrescentar índices duplicados na BD
# (ver H_integrity_checks.sql, observação O.1).
#
# Uso (a partir da raiz do repo, com a stack Docker a correr):
#   bash sql/tc75_persistence.sh
#
# Variáveis opcionais:
#   API=http://localhost:9966/petclinic/api   AUTH=admin:admin
#   PSQL_CMD="docker exec -i petclinic-postgres psql -U petclinic -d petclinic"
#   RESTART_CMD="docker restart petclinic-postgres petclinic-backend"
set -euo pipefail

API="${API:-http://localhost:9966/petclinic/api}"
AUTH="${AUTH:-admin:admin}"
PSQL_CMD="${PSQL_CMD:-docker exec -i petclinic-postgres psql -U petclinic -d petclinic}"
RESTART_CMD="${RESTART_CMD:-docker restart petclinic-postgres petclinic-backend}"

PAYLOAD='{"firstName":"Persiste","lastName":"Teste","address":"Rua do Volume 2","city":"Porto","telephone":"9123456780"}'

echo "1) Criar owner via API"
HTTP=$(curl -s -o /tmp/tc75_resp.json -w '%{http_code}' -u "$AUTH" -X POST \
  -H "Content-Type: application/json" -d "$PAYLOAD" "$API/owners")
[ "$HTTP" = "201" ] || { echo "FAIL: esperado 201, obtido $HTTP"; cat /tmp/tc75_resp.json; echo; exit 1; }
ID=$(sed -n 's/.*"id": *\([0-9][0-9]*\).*/\1/p' /tmp/tc75_resp.json | head -n 1)
[ -n "$ID" ] || { echo "FAIL: não foi possível ler o id"; exit 1; }
echo "   owner id=$ID"

count_in_db() { echo "SELECT count(*) FROM owners WHERE id = $ID;" | $PSQL_CMD -At; }
echo "2) Antes do reinício, registos na BD com id=$ID: $(count_in_db)"

echo "3) Reiniciar containers: $RESTART_CMD"
$RESTART_CMD >/dev/null

echo "4) A esperar que a API volte (máx. 180 s)"
for i in $(seq 1 90); do
  CODE=$(curl -s -o /dev/null -w '%{http_code}' -u "$AUTH" "$API/owners/$ID" || true)
  if [ "$CODE" = "200" ]; then echo "   API de volta ao fim de ~$((i*2)) s"; break; fi
  sleep 2
done

AFTER=$(count_in_db)
echo "5) Depois do reinício, registos na BD com id=$ID: $AFTER"

echo "6) Limpeza: DELETE $API/owners/$ID"
curl -s -o /dev/null -w '   resposta HTTP: %{http_code}\n' -u "$AUTH" -X DELETE "$API/owners/$ID" || true

if [ "$AFTER" = "1" ]; then
  echo "PASS: o registo persistiu após o reinício"
else
  echo "FAIL: o registo desapareceu após o reinício"
  exit 1
fi
