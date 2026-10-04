"""
Testes automatizados do fluxo "Adicionar Specialty" (módulo Specialties).

Usa um sufixo único (timestamp) no nome, porque aqui faz sentido evitar
colisões: ao contrário de Owners/Vets, a lista de Specialties é normalmente
pequena e usada como dropdown noutros formulários (ex: Vets) — manter o
mesmo nome em cada execução iria acumular specialties idênticas e tornar
a lista confusa para quem a vir manualmente mais tarde.
"""

from __future__ import annotations

import time

from playwright.sync_api import Page

from pages.specialty_page import SpecialtyPage


class TestAddSpecialty:
    """Teste do caminho feliz para criar uma nova Specialty."""

    def test_criar_specialty_valida(self, page: Page) -> None:
        """
        Caminho feliz: criar uma specialty com um nome válido e confirmar
        que aparece na lista.

        Fluxo diferente dos outros módulos: não há navegação para uma
        página separada — o formulário aparece embutido na própria lista
        ao clicar "Add" (confirmado em specialty-list.component.ts).
        """
        unique_name = f"cardiology{str(int(time.time() * 1000))[-6:]}"

        specialty_page = SpecialtyPage(page)
        specialty_page.open_specialties_list()
        specialty_page.open_add_form()
        specialty_page.fill_and_submit(unique_name)

        assert specialty_page.specialty_appears_in_list(unique_name), (
            f"A specialty '{unique_name}' deveria aparecer na lista "
            "depois de criada."
        )
