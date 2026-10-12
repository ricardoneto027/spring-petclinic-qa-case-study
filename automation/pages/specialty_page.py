"""
Page Object para o fluxo "Adicionar Specialty" (módulo Specialties).

Detalhe importante confirmado no código-fonte (specialty-list.component.html
e specialty-add.component.ts): ao contrário de Owners/Pets/Vets, isto NÃO é
uma página separada. É um formulário embutido (`<app-specialty-add>`) que
aparece/desaparece dentro da própria lista quando se clica em "Add" — e a
rota 'specialties/add' está comentada no routing module, ou seja, nem
existe como URL navegável diretamente.

Outro detalhe importante: a lista de Specialties mostra os nomes dentro de
`<input readonly>` (specialty-list.component.html: `[(ngModel)]="specialty.name"`),
não como texto simples numa `<td>`. Por isso a confirmação de que uma
specialty foi criada usa `input_value()` em vez de comparação de texto
(`has_text` não encontra o valor de um `<input>`, só texto "visível" no DOM).
"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.main import BasePage


class SpecialtyPage(BasePage):
    """Ações da lista de Specialties e do formulário inline de criação."""

    ADD_TOGGLE_BUTTON = "button:has-text('Add')"
    NAME_INPUT = "#name"  # input do formulário inline app-specialty-add
    SAVE_BUTTON = "button:has-text('Save')"
    LIST_NAME_INPUTS = "input[name='spec_name']"  # inputs readonly da lista

    def __init__(self, page: Page, base_url: str = "http://localhost:4200") -> None:
        super().__init__(page)
        self.base_url = base_url

    def open_specialties_list(self) -> None:
        """Rota confirmada em specialties-routing.module.ts: 'specialties'."""
        self.navigate(f"{self.base_url}/petclinic/specialties")

    def open_add_form(self) -> None:
        """
        Clica em "Add" para revelar o formulário inline de nova Specialty.

        Confirmado em specialty-list.component.ts: `showAddSpecialtyComponent`
        só faz toggle de uma flag (`isInsert`) — não há navegação.
        """
        self.click(self.ADD_TOGGLE_BUTTON)
        self.assert_visible(self.NAME_INPUT)

    def fill_and_submit(self, name: str) -> None:
        """Preenche o nome e submete o formulário inline (botão "Save")."""
        self.fill_text(self.NAME_INPUT, name)
        self.click(self.SAVE_BUTTON)

    def specialty_appears_in_list(self, name: str) -> bool:
        """
        Confirma se uma specialty com o nome indicado aparece na lista.

        Os nomes são `<input readonly>`, por isso não dá para usar
        `has_text` (isso só encontra texto no DOM, não valores de input).

        Espera ativamente (até DEFAULT_TIMEOUT) que algum input da lista tenha
        o valor procurado. Ler os inputs uma única vez logo após o "Save"
        criava uma race condition: a lista ainda não tinha sido atualizada
        com a resposta da API. Localmente o slow_mo escondia o problema; em
        CI (headless, sem slow_mo) o teste falhava.
        """
        try:
            self.page.wait_for_function(
                """([selector, expected]) =>
                    Array.from(document.querySelectorAll(selector))
                        .some((input) => input.value === expected)""",
                arg=[self.LIST_NAME_INPUTS, name],
                timeout=self.DEFAULT_TIMEOUT,
            )
            return True
        except Exception:
            return False
