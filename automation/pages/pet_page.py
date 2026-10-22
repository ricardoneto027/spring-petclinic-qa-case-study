"""
Page Object para o fluxo "Adicionar Pet" (TC-PET-01 e relacionados).

Todos os seletores e o formato de data abaixo foram confirmados a partir
do código-fonte real do `spring-petclinic-angular` (pet-add.component.html
e pets.module.ts), não inferidos.

Detalhe importante confirmado em `pets.module.ts` (MY_DATE_FORMATS):
o datepicker (Material + Moment) espera o formato "YYYY/MM/DD" (com
barras), não "YYYY-MM-DD". Usar o formato errado faz o Playwright escrever
uma data que o datepicker não consegue interpretar.
"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.main import BasePage

# Formato de data exigido pelo datepicker desta app (confirmado em pets.module.ts)
DATE_FORMAT = "%Y/%m/%d"  # ex: "2022/01/15"


class PetPage(BasePage):
    """Ações do formulário "Add Pet", acedido a partir do detalhe de um Owner."""

    NAME_INPUT = "#name"
    BIRTHDATE_INPUT = "#birthDate"
    TYPE_SELECT = "#type"
    SUBMIT_BUTTON = "button:has-text('Save Pet')"

    def __init__(self, page: Page, base_url: str = "http://localhost:4200") -> None:
        super().__init__(page)
        self.base_url = base_url

    def open_new_pet_form(self, owner_id: int) -> None:
        """
        Navega diretamente para o formulário "Add Pet" de um owner.

        Rota confirmada em pets-routing.module.ts: 'owners/:id/pets/add'.
        """
        self.navigate(f"{self.base_url}/petclinic/owners/{owner_id}/pets/add")

    def fill_pet_form(self, name: str, birth_date_text: str, type_index: int = 0) -> None:
        """
        Preenche o formulário "Add Pet".

        `birth_date_text` deve já vir no formato "YYYY/MM/DD" (usa
        `DATE_FORMAT` acima para converter uma `datetime.date`).

        `type_index` seleciona o Pet Type pela posição no dropdown (0 =
        primeiro disponível), em vez de um nome fixo como "dog" — porque os
        pet types existentes podem variar (ex: já apagaste "dog" e "cat"
        durante os testes manuais do bug de cascade-delete). Usa
        `select_pet_type_by_name` em vez deste parâmetro se precisares de
        um tipo específico que sabes que ainda existe.
        """
        self.fill_text(self.NAME_INPUT, name)
        self.fill_text(self.BIRTHDATE_INPUT, birth_date_text)
        self.page.locator(self.TYPE_SELECT).select_option(index=type_index)

    def select_pet_type_by_name(self, type_name: str) -> None:
        """Seleciona o Pet Type pelo nome visível na dropdown (ex: 'hamster')."""
        self.page.locator(self.TYPE_SELECT).select_option(label=type_name)

    def submit(self) -> None:
        """Submete o formulário "Add Pet" (botão "Save Pet")."""
        self.click(self.SUBMIT_BUTTON)

    def pet_appears_in_owner_detail(self, pet_name: str) -> bool:
        """
        Confirma se um pet com o nome indicado aparece no detalhe do owner.

        Baseado em pet-list.component.html: o nome do pet é mostrado num
        `<dd>` dentro da tabela "Pets and Visits" do owner-detail.
        """
        locator = self.page.locator("dd", has_text=pet_name)
        try:
            locator.first.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
            return True
        except Exception:
            return False

    def click_add_visit_for_pet(self, pet_name: str) -> None:
        """
        A partir do detalhe do owner, clica em "Add Visit" na linha do pet
        indicado.

        Confirmado em pet-list.component.html: cada pet tem a sua própria
        `<tr>` com o botão "Add Visit" — por isso filtramos a `tr` que
        contém o nome do pet antes de procurar o botão dentro dela.
        """
        row = self.page.locator("tr", has_text=pet_name)
        button = row.locator("button:has-text('Add Visit')")
        button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        button.click()
