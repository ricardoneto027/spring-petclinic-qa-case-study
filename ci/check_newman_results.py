#!/usr/bin/env python3
"""Compara as falhas de um run do Newman com a lista de falhas conhecidas.

A suite de API inclui testes que falham de propósito: documentam bugs abertos
no Jira. Por isso a CI não falha por esses, mas falha se:
  - aparecer uma falha num TC que não está na lista (regressão nova);
  - o run não tiver executado nenhum pedido.
Se um TC da lista passar a passar, é emitido um aviso (bug possivelmente
corrigido: retirar da lista e retestar o bug no Jira).

Uso: python3 ci/check_newman_results.py <results.json> <known-failures.txt>
"""
import json
import os
import re
import sys

TC_RE = re.compile(r"SPRINGQA-TC-\d+")


def load_known(path):
    known = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = TC_RE.search(line.split("#", 1)[0])
            if m:
                known.add(m.group(0))
    return known


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    results_path, known_path = sys.argv[1], sys.argv[2]
    with open(results_path, encoding="utf-8") as f:
        run = json.load(f)["run"]
    known = load_known(known_path)

    executed, failed = set(), set()
    for ex in run.get("executions", []):
        m = TC_RE.search(ex.get("item", {}).get("name", ""))
        if m:
            executed.add(m.group(0))
    for fail in run.get("failures", []):
        m = TC_RE.search((fail.get("source") or {}).get("name", ""))
        if m:
            failed.add(m.group(0))

    stats = run.get("stats", {}).get("assertions", {})
    new_failures = sorted(failed - known, key=lambda t: int(t.split("-")[-1]))
    fixed = sorted((known & executed) - failed, key=lambda t: int(t.split("-")[-1]))

    lines = [
        f"### Resultado Newman: {os.path.basename(results_path)}",
        "",
        f"- Pedidos executados: {len(executed)} TCs",
        f"- Assertions: {stats.get('total', '?')} total, {stats.get('failed', '?')} falhadas",
        f"- TCs com falha: {len(failed)} (conhecidas: {len(failed & known)}, novas: {len(new_failures)})",
        "",
    ]
    if new_failures:
        lines.append("**Falhas novas (não estão na lista de bugs conhecidos):** " + ", ".join(new_failures))
    if fixed:
        lines.append("**Falhas conhecidas que passaram (bug possivelmente corrigido):** " + ", ".join(fixed))
    if not new_failures and not fixed:
        lines.append("Sem regressões: todas as falhas correspondem a bugs conhecidos.")
    report = "\n".join(lines)
    print(report)

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(report + "\n\n")
    for tc in fixed:
        print(f"::warning::{tc} estava na lista de falhas conhecidas mas passou. Retestar o bug e atualizar {known_path}.")

    if not executed:
        print("::error::O Newman não executou nenhum pedido.")
        return 1
    if new_failures:
        print("::error::Falhas novas: " + ", ".join(new_failures))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
