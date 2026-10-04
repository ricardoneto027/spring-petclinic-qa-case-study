"""
Page Object para o fluxo "Adicionar Visita" (módulo Visits).

Seletores confirmados a partir de visit-add.component.html e do mesmo
MY_DATE_FORMATS ("YYYY/MM/DD") usado no módulo Pets (confirmado também em
visits.module.ts, que regista o mesmo DateAdapter/MAT_DATE_FORMATS).
"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.main import BasePage

DATE_FORMAT = "%Y/%m/%d"  # ex: "2026/10/03" — mesmo formato do módulo Pets


class VisitPage(BasePage):
    """Ações do formulário "New Visit", acedido a partir do pet (botão "Add Visit")."""

    DATE_INPUT = "#date"
    DESCRIPTION_INPUT = "#description"
    SUBMIT_BUTTON = "button:has-text('Add Visit')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def fill_visit_form(self, date_text: str, description: str) -> None:
        """
        Preenche o formulário de nova visita.

        `date_text` no formato "YYYY/MM/DD" (ver DATE_FORMAT).
        """
        self.fill_text(self.DATE_INPUT, date_text)
        self.fill_text(self.DESCRIPTION_INPUT, description)

    def submit(self) -> None:
        """Submete o formulário (botão "Add Visit")."""
        self.click(self.SUBMIT_BUTTON)

    def visit_appears_for_pet(self, description: str) -> bool:
        """
        Confirma se uma visita com a descrição indicada aparece na lista de
        visitas do pet (visit-list.component.html mostra a descrição numa
        `<td>`).
        """
        locator = self.page.locator("td", has_text=description)
        try:
            locator.first.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
            return True
        except Exception:
            return False
