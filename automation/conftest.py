"""
Configuração partilhada do pytest (fixtures) para os testes de automação.

- `browser`: iniciado uma única vez por sessão de testes (mais rápido).
- `page`: um `BrowserContext` + `Page` novos por teste, para garantir que
  os testes são isolados entre si (sem cookies/estado partilhado).
"""

from __future__ import annotations

import os
from typing import Iterator

import pytest
from playwright.sync_api import Browser, Page, sync_playwright

# URL base da app Angular a correr localmente via Docker/npm.
# TODO: VERIFICAR — confirmar que esta é a porta/host correta no teu ambiente.
BASE_URL = "http://localhost:4200"

# Em CI (o GitHub Actions define CI=true) o browser corre sem interface.
# Localmente abre o browser em câmara lenta para se ver a execução;
# para forçar o modo sem interface localmente: HEADLESS=true pytest
HEADLESS = os.getenv("CI") == "true" or os.getenv("HEADLESS", "").lower() == "true"


@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    """
    Lança o browser Chromium uma vez para toda a sessão de testes.

    Em CI corre sem interface visível (mais rápido). Localmente abre o
    browser com slow_mo para se ver a execução (ver HEADLESS acima).
    """
    with sync_playwright() as playwright:
        browser_instance = playwright.chromium.launch(
            headless=HEADLESS, slow_mo=0 if HEADLESS else 300
        )
        yield browser_instance
        browser_instance.close()


@pytest.fixture
def page(browser: Browser) -> Iterator[Page]:
    """
    Cria um `BrowserContext` e `Page` novos e isolados para cada teste.

    Usar um contexto novo por teste (em vez de reutilizar a mesma Page)
    evita que o estado de um teste (ex: um formulário parcialmente
    preenchido, ou cookies) afete o teste seguinte.
    """
    context = browser.new_context(
        base_url=BASE_URL,
        viewport={"width": 1280, "height": 800},
    )
    new_page = context.new_page()
    yield new_page
    # Teardown seguro: fecha sempre o contexto, mesmo que o teste falhe.
    context.close()
