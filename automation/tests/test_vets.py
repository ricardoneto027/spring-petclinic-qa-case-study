"""
Testes automatizados do fluxo "Adicionar Veterinário" (módulo Vets).
"""

from __future__ import annotations

import time

from playwright.sync_api import Page

from pages.specialty_page import SpecialtyPage
from pages.vet_page import VetPage


class TestAddVet:
    """Teste do caminho feliz para criar um veterinário."""

    def test_criar_vet_com_especialidade(self, page: Page) -> None:
        """
        Caminho feliz: criar um vet válido associado a uma especialidade
        existente, e confirmar que aparece na lista de veterinários.

        O teste cria a sua própria Specialty antes de criar o Vet, em vez
        de assumir que já existem specialties no sistema (dados de seed
        como "radiology" podem já não existir — por exemplo, se foram
        apagadas durante testes manuais anteriores). Isto torna o teste
        independente do estado atual da base de dados.
        """
        unique_specialty = f"dermatology{str(int(time.time() * 1000))[-6:]}"
        specialty_page = SpecialtyPage(page)
        specialty_page.open_specialties_list()
        specialty_page.open_add_form()
        specialty_page.fill_and_submit(unique_specialty)
        assert specialty_page.specialty_appears_in_list(unique_specialty), (
            f"Pré-condição falhou: a specialty '{unique_specialty}' não foi "
            "criada, não é possível continuar para o teste de Vets."
        )

        vet_page = VetPage(page)
        vet_page.open_new_vet_form()
        vet_page.fill_vet_form(first_name="Carlos", last_name="Mendes", specialty_name=unique_specialty)
        vet_page.submit()

        assert vet_page.vet_appears_in_list("Carlos Mendes"), (
            "O vet 'Carlos Mendes' deveria aparecer na lista de "
            "veterinários após a criação com dados válidos."
        )

    def test_criar_vet_sem_especialidade(self, page: Page) -> None:
        """
        Caminho feliz alternativo: o campo Specialty não é obrigatório
        (sem `required` no select, confirmado em vet-add.component.html),
        por isso um vet sem especialidade também deve ser aceite.
        """
        vet_page = VetPage(page)
        vet_page.open_new_vet_form()
        vet_page.fill_vet_form(first_name="Ines", last_name="Barros")  # sem specialty_name
        vet_page.submit()

        assert vet_page.vet_appears_in_list("Ines Barros"), (
            "O vet 'Ines Barros' deveria aparecer na lista mesmo sem "
            "especialidade associada."
        )
