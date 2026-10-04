"""
Classe base (BasePage) com ações reutilizáveis para todas as Pages do projeto.

Todas as Pages concretas (OwnerPage, PetPage, VisitPage, ...) devem herdar
desta classe. Isto evita repetir chamadas diretas ao Playwright em cada
Page, e centraliza as esperas explícitas (nenhum time.sleep em lado nenhum).
"""

from __future__ import annotations

from playwright.sync_api import Page, expect


class BasePage:
    """Ações genéricas de interação com a página, com espera explícita embutida."""

    DEFAULT_TIMEOUT = 10_000  # 10 segundos, em milissegundos (padrão do Playwright)

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str) -> None:
        """Navega para o URL indicado e espera a rede estabilizar (SPA Angular)."""
        self.page.goto(url, wait_until="networkidle")

    def click(self, selector: str, timeout: int | None = None) -> None:
        """Clica num elemento, esperando explicitamente que esteja visível antes."""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout or self.DEFAULT_TIMEOUT)
        locator.click()

    def fill_text(self, selector: str, text: str, timeout: int | None = None) -> None:
        """Preenche um campo de texto (o Playwright limpa o campo antes de escrever)."""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout or self.DEFAULT_TIMEOUT)
        locator.fill(text)

    def get_text(self, selector: str, timeout: int | None = None) -> str:
        """Devolve o texto visível de um elemento, após esperar que exista."""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout or self.DEFAULT_TIMEOUT)
        return locator.inner_text()

    def is_visible(self, selector: str, timeout: int | None = None) -> bool:
        """Verifica se um elemento está visível, sem levantar exceção se não estiver."""
        try:
            self.page.locator(selector).wait_for(
                state="visible", timeout=timeout or self.DEFAULT_TIMEOUT
            )
            return True
        except Exception:
            return False

    def assert_visible(self, selector: str, timeout: int | None = None) -> None:
        """Assert explícito de visibilidade (usa o auto-retry nativo do `expect`)."""
        expect(self.page.locator(selector)).to_be_visible(
            timeout=timeout or self.DEFAULT_TIMEOUT
        )

    def assert_text_contains(
        self, selector: str, expected_text: str, timeout: int | None = None
    ) -> None:
        """Assert explícito de que um elemento contém um determinado texto."""
        expect(self.page.locator(selector)).to_contain_text(
            expected_text, timeout=timeout or self.DEFAULT_TIMEOUT
        )
