"""
Page Object para o fluxo "Owners" (Donos de animais).

Exemplo concreto de fluxo crítico, usado em substituição de "Login"
(a app Spring PetClinic não tem autenticação ativa por padrão), seguindo
o TC-OWN-01 do Test Design: "Criar owner válido".

Seletores e rotas confirmados a partir do código-fonte real do
`spring-petclinic-angular` (owner-add.component.html/.ts,
owner-list.component.html, owner-detail.component.html/.ts,
owners-routing.module.ts).
"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.main import BasePage


class OwnerPage(BasePage):
    """Ações do formulário "New Owner", da lista e do detalhe de um Owner."""

    FIRST_NAME_INPUT = "input[name='firstName']"
    LAST_NAME_INPUT = "input[name='lastName']"
    ADDRESS_INPUT = "input[name='address']"
    CITY_INPUT = "input[name='city']"
    TELEPHONE_INPUT = "input[name='telephone']"
    SUBMIT_BUTTON = "button:has-text('Add Owner')"
    OWNER_LIST_TABLE = "table"
    ADD_NEW_PET_BUTTON = "button:has-text('Add New Pet')"

    def __init__(self, page: Page, base_url: str = "http://localhost:4200") -> None:
        super().__init__(page)
        self.base_url = base_url

    def open_new_owner_form(self) -> None:
        """
        Navega diretamente para o formulário de criação de Owner.

        Rota confirmada em owners-routing.module.ts: 'owners/add'.
        """
        self.navigate(f"{self.base_url}/petclinic/owners/add")

    def fill_owner_form(
        self,
        first_name: str,
        last_name: str,
        address: str,
        city: str,
        telephone: str,
    ) -> None:
        """Preenche todos os campos do formulário "New Owner" com os dados dados."""
        self.fill_text(self.FIRST_NAME_INPUT, first_name)
        self.fill_text(self.LAST_NAME_INPUT, last_name)
        self.fill_text(self.ADDRESS_INPUT, address)
        self.fill_text(self.CITY_INPUT, city)
        self.fill_text(self.TELEPHONE_INPUT, telephone)

    def is_submit_button_enabled(self) -> bool:
        """
        Verifica se o botão de submit está habilitado.

        Relevante para o TC-UX-01b (achado de exploração): em alguns casos o
        formulário pode permitir submissão com dados ainda inválidos — este
        método serve para o teste poder verificar esse comportamento
        explicitamente, em vez de assumir.
        """
        locator = self.page.locator(self.SUBMIT_BUTTON)
        locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        return locator.is_enabled()

    def submit(self) -> None:
        """Submete o formulário "New Owner"."""
        self.click(self.SUBMIT_BUTTON)

    def owner_appears_in_list(self, full_name: str) -> bool:
        """
        Confirma se um owner com o nome completo indicado aparece na lista.

        Usa `page.locator` com filtro de texto em vez de `get_text`, porque
        a lista pode conter vários owners — procuramos uma linha específica.
        """
        row_locator = self.page.locator(f"{self.OWNER_LIST_TABLE} tr", has_text=full_name)
        try:
            row_locator.first.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
            return True
        except Exception:
            return False

    def open_owner_detail(self, full_name: str) -> None:
        """
        Clica no link do owner (na lista) para abrir o seu detalhe.

        Confirmado em owner-list.component.html: o nome é um `<a>` com
        `routerLink="/owners/{{owner.id}}"`.
        """
        link = self.page.locator("a", has_text=full_name)
        link.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        link.click()
        # Confirma que chegámos ao detalhe (owner-detail.component.html)
        self.assert_visible("h2:has-text('Owner Information')")

    def click_add_new_pet(self) -> None:
        """
        A partir do detalhe do owner, clica em "Add New Pet".

        Confirmado em owner-detail.component.html/.ts: navega para
        'owners/:id/pets/add'.
        """
        self.click(self.ADD_NEW_PET_BUTTON)
