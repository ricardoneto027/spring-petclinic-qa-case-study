"""
Testes automatizados do fluxo "Adicionar Visita" (módulo Visits).

Depende do fluxo completo: criar Owner -> criar Pet -> adicionar Visita,
pela mesma razão de isolamento usada em test_pets.py (nomes únicos por
execução, sem depender de dados de testes anteriores).
"""

from __future__ import annotations

import time

import pytest
from playwright.sync_api import Page

from pages.owner_page import OwnerPage
from pages.pet_page import PetPage
from pages.visit_page import VisitPage

# Nome fixo do owner usado neste ficheiro (ver nota em test_pets.py: o
# campo First/Last Name só aceita letras, por isso não pode ter sufixo
# numérico). Diferente do nome usado em test_pets.py só para ser fácil de
# distinguir nos dados de teste.
OWNER_FIRST_NAME = "Tiago"
OWNER_LAST_NAME = "Pereira"


def _unique_suffix() -> str:
    """
    Sufixo numérico só para o nome do Pet e a descrição da Visita — esses
    campos aceitam dígitos (confirmado em pet-add.component.html:
    pattern="^[A-Za-z0-9].{0,29}$" para o nome do pet; a descrição da
    visita não tem pattern nenhum). Mantém estes dados distintos entre
    execuções, mesmo reutilizando sempre o mesmo owner.
    """
    return str(int(time.time() * 1000))[-8:]


class TestAddVisit:
    """Teste do caminho feliz para adicionar uma visita a um pet existente."""

    @pytest.mark.xfail(
        reason=(
            "Bug conhecido (SPRINGQA-6, confirmado no Jira): a página de "
            "detalhe do Owner não apresenta nenhum dado — nem os campos do "
            "próprio owner, nem a secção 'Pets and Visits'. Isto bloqueia a "
            "verificação visual tanto de Pets (ver test_pets.py) como de "
            "Visits: nenhum dos dois é possível confirmar pela UI enquanto "
            "este bug não for corrigido, mesmo que ambos sejam persistidos "
            "corretamente no backend. Remover o xfail quando a página "
            "voltar a renderizar os dados."
        ),
        strict=False,
    )
    def test_adicionar_visita_valida(self, page: Page) -> None:
        """
        Caminho feliz: criar owner -> pet -> visita.

        Documenta o SPRINGQA-6: nem o pet nem a visita aparecem no detalhe
        do owner, apesar de ambos serem criados corretamente no backend.
        """
        suffix = _unique_suffix()
        first_name, last_name = OWNER_FIRST_NAME, OWNER_LAST_NAME
        full_name = f"{first_name} {last_name}"
        pet_name = f"PetVisit{suffix}"
        visit_description = f"Consulta de rotina {suffix}"

        # 1. Criar owner
        owner_page = OwnerPage(page)
        owner_page.open_new_owner_form()
        owner_page.fill_owner_form(
            first_name=first_name,
            last_name=last_name,
            address="Rua das Visitas, 1",
            city="Braga",
            telephone="9188888888",
        )
        owner_page.submit()
        owner_page.open_owner_detail(full_name)

        # 2. Criar pet associado a este owner
        owner_page.click_add_new_pet()
        pet_page = PetPage(page)
        pet_page.fill_pet_form(
            name=pet_name,
            birth_date_text="2021/05/20",
            type_index=0,
        )
        pet_page.submit()
        assert pet_page.pet_appears_in_owner_detail(pet_name), (
            f"O pet '{pet_name}' deveria aparecer no detalhe do owner "
            "(bloqueado por SPRINGQA-6)."
        )

        # 3. Adicionar visita a esse pet
        pet_page.click_add_visit_for_pet(pet_name)
        visit_page = VisitPage(page)
        visit_page.fill_visit_form(
            date_text="2026/10/03",  # formato confirmado: YYYY/MM/DD
            description=visit_description,
        )
        visit_page.submit()

        assert visit_page.visit_appears_for_pet(visit_description), (
            f"A visita '{visit_description}' deveria aparecer associada "
            f"ao pet '{pet_name}' (bloqueado por SPRINGQA-6)."
        )
