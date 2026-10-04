"""
Page Object para o fluxo "Adicionar Veterinário" (módulo Vets).

Seletores e rota confirmados a partir do código-fonte real
(vet-add.component.html/.ts, vet-list.component.html, vets-routing.module.ts).

Nota: o campo "Specialty" NÃO é obrigatório neste formulário (sem `required`
no `<select>`) — por isso dá para criar um Vet sem especialidade associada.
"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.main import BasePage


class VetPage(BasePage):
    """Ações do formulário "New Veterinarian" e da lista de Vets."""

    FIRST_NAME_INPUT = "#firstName"
    LAST_NAME_INPUT = "#lastName"
    SPECIALTY_SELECT = "#specialties"
    SUBMIT_BUTTON = "button:has-text('Save Vet')"
    VET_LIST_TABLE = "#vets"

    def __init__(self, page: Page, base_url: str = "http://localhost:4200") -> None:
        super().__init__(page)
        self.base_url = base_url

    def open_new_vet_form(self) -> None:
        """Rota confirmada em vets-routing.module.ts: 'vets/add'."""
        self.navigate(f"{self.base_url}/petclinic/vets/add")

    def fill_vet_form(self, first_name: str, last_name: str, specialty_name: str | None = None) -> None:
        """
        Preenche o formulário "New Veterinarian".

        `specialty_name` é opcional: o campo não tem validação `required`
        no código-fonte, por isso um Vet pode ser criado sem especialidade.
        """
        self.fill_text(self.FIRST_NAME_INPUT, first_name)
        self.fill_text(self.LAST_NAME_INPUT, last_name)
        if specialty_name is not None:
            self.page.locator(self.SPECIALTY_SELECT).select_option(label=specialty_name)

    def submit(self) -> None:
        """Submete o formulário (botão "Save Vet")."""
        self.click(self.SUBMIT_BUTTON)

    def vet_appears_in_list(self, full_name: str) -> bool:
        """
        Confirma se um vet com o nome completo indicado aparece na lista.

        Confirmado em vet-list.component.html: o nome é texto simples numa
        `<td>` (não um input, ao contrário da lista de Specialties).
        """
        row_locator = self.page.locator(f"{self.VET_LIST_TABLE} tr", has_text=full_name)
        try:
            row_locator.first.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
            return True
        except Exception:
            return False
