#!/usr/bin/env bash
# SPRINGQA-TC-74 · Consistência entre a resposta da API e os dados na BD
#
# Cria um owner via API, lê a linha correspondente diretamente na BD e compara
# campo a campo. No fim apaga o owner criado.
#
# Uso (a partir da raiz do repo, com a stack Docker a correr):
#   bash sql/tc74_api_vs_db.sh
#
# Variáveis opcionais:
#   API=http://localhost:9966/petclinic/api   AUTH=admin:admin
#   PSQL_CMD="docker exec -i petclinic-postgres psql -U petclinic -d petclinic"
set -euo pipefail

API="${API:-http://localhost:9966/petclinic/api}"
AUTH="${AUTH:-admin:admin}"
PSQL_CMD="${PSQL_CMD:-docker exec -i petclinic-postgres psql -U petclinic -d petclinic}"

FIRST="Sql"; LAST="Teste"; ADDRESS="Rua da BD 1"; CITY="Lisboa"; PHONE="9123456789"
PAYLOAD=$(printf '{"firstName":"%s","lastName":"%s","address":"%s","city":"%s","telephone":"%s"}' \
  "$FIRST" "$LAST" "$ADDRESS" "$CITY" "$PHONE")

echo "1) POST $API/owners"
HTTP=$(curl -s -o /tmp/tc74_resp.json -w '%{http_code}' -u "$AUTH" -X POST \
  -H "Content-Type: application/json" -d "$PAYLOAD" "$API/owners")
echo "   resposta HTTP: $HTTP"
[ "$HTTP" = "201" ] || { echo "FAIL: esperado 201"; cat /tmp/tc74_resp.json; echo; exit 1; }

ID=$(sed -n 's/.*"id": *\([0-9][0-9]*\).*/\1/p' /tmp/tc74_resp.json | head -n 1)
[ -n "$ID" ] || { echo "FAIL: não foi possível ler o id da resposta"; exit 1; }
echo "   owner criado com id=$ID"

echo "2) SELECT na BD (id=$ID)"
DB_ROW=$(echo "SELECT first_name || '|' || last_name || '|' || address || '|' || city || '|' || telephone FROM owners WHERE id = $ID;" \
  | $PSQL_CMD -At)
echo "   BD:       $DB_ROW"

EXPECTED="$FIRST|$LAST|$ADDRESS|$CITY|$PHONE"
echo "   esperado: $EXPECTED"

echo "3) Limpeza: DELETE $API/owners/$ID"
curl -s -o /dev/null -w '   resposta HTTP: %{http_code}\n' -u "$AUTH" -X DELETE "$API/owners/$ID"

if [ "$DB_ROW" = "$EXPECTED" ]; then
  echo "PASS: os dados persistidos na BD coincidem com os enviados/devolvidos pela API"
else
  echo "FAIL: os dados na BD diferem do esperado"
  exit 1
fi
