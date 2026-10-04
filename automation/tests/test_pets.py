"""
Testes automatizados do fluxo "Adicionar Pet" (módulo B do Test Design).

Cada teste cria o seu próprio Owner (nome único, baseado em timestamp) para
não depender de dados deixados por execuções anteriores nem por outros
testes — cada teste tem de poder correr isoladamente.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page

from pages.owner_page import OwnerPage
from pages.pet_page import PetPage


OWNER_FIRST_NAME = "Marta"
OWNER_LAST_NAME = "Nogueira"


def _create_owner_and_open_detail(page: Page) -> tuple[OwnerPage, str]:
    """
    Cria um owner novo com dados válidos e abre o seu detalhe.

    Devolve a OwnerPage (já no detalhe do owner) e o nome completo criado,
    para os testes poderem continuar a partir daí (ex: adicionar um pet).
    """
    first_name, last_name = OWNER_FIRST_NAME, OWNER_LAST_NAME
    full_name = f"{first_name} {last_name}"

    owner_page = OwnerPage(page)
    owner_page.open_new_owner_form()
    owner_page.fill_owner_form(
        first_name=first_name,
        last_name=last_name,
        address="Rua de Teste, 99",
        city="Coimbra",
        telephone="9199999999",  # 10 dígitos válidos
    )
    owner_page.submit()
    owner_page.open_owner_detail(full_name)
    return owner_page, full_name


class TestAddPet:
    """Testes para a criação de Pets associados a um Owner (TC-PET-01 e relacionados)."""

    @pytest.mark.xfail(
        reason=(
            "Bug conhecido (SPRINGQA-6, confirmado no Jira): a página de "
            "detalhe do Owner não apresenta nenhum dado — nem os campos do "
            "próprio owner (Name/Address/City/Telephone ficam vazios) nem a "
            "secção 'Pets and Visits'. O pet É criado com sucesso no "
            "backend (confirmável via Swagger, GET /api/owners/{id}), mas "
            "não há forma de o confirmar visualmente pela UI enquanto este "
            "bug não for corrigido. Remover o xfail quando a página voltar "
            "a renderizar os dados."
        ),
        strict=False,
    )
    def test_adicionar_pet_valido(self, page: Page) -> None:
        """
        TC-PET-01 — Caminho feliz: adicionar um pet válido a um owner existente.

        O pet é persistido corretamente no backend, mas a UI não o mostra
        (SPRINGQA-6) — por isso este teste documenta o bug em vez de
        confirmar o caminho feliz.
        """
        owner_page, _ = _create_owner_and_open_detail(page)
        owner_page.click_add_new_pet()

        pet_page = PetPage(page)
        pet_page.fill_pet_form(
            name="Rex",
            birth_date_text="2022/01/15",  # formato confirmado: YYYY/MM/DD
            type_index=0,  # primeiro Pet Type disponível, seja qual for
        )
        pet_page.submit()

        assert pet_page.pet_appears_in_owner_detail("Rex"), (
            "O pet 'Rex' deveria aparecer no detalhe do owner após a "
            "criação com dados válidos."
        )

    @pytest.mark.xfail(
        reason=(
            "Bug conhecido (mesma família do SPRINGQA-7 — falha silenciosa): "
            "o backend rejeita uma Birth Date no futuro (TC-PET-04), mas a "
            "Angular UI não mostra nenhum erro. Nota: devido ao SPRINGQA-6, "
            "a primeira asserção (pet não aparece no detalhe) não é um "
            "sinal fiável por si só, porque a página não mostra pets "
            "nenhuns, válidos ou não — a segunda asserção (mensagem de "
            "erro visível) é a que realmente documenta este bug. Remover o "
            "xfail quando for corrigido."
        ),
        strict=False,
    )
    def test_adicionar_pet_data_nascimento_futura_bug_conhecido(self, page: Page) -> None:
        """
        TC-PET-04 — Data de nascimento no futuro.

        Comportamento correto esperado: o sistema deveria rejeitar a
        submissão E mostrar um erro visível. Atualmente falha
        silenciosamente (pet não é criado, mas também não há mensagem).
        """
        owner_page, _ = _create_owner_and_open_detail(page)
        owner_page.click_add_new_pet()

        pet_page = PetPage(page)
        pet_page.fill_pet_form(
            name="PetFuturo",
            birth_date_text="2099/01/01",  # data no futuro — deveria ser inválida
            type_index=0,
        )
        pet_page.submit()

        assert not pet_page.pet_appears_in_owner_detail("PetFuturo"), (
            "O pet não deveria ter sido criado com uma data de nascimento no futuro."
        )
        # TODO: VERIFICAR texto real da mensagem de erro, quando a UI passar a mostrá-la
        pet_page.assert_visible("text=cannot be in the future")
