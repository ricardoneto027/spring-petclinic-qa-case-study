"""
Testes automatizados do fluxo "Criar Owner" (TC-OWN-01 e caso relacionado
com o bug conhecido SPRINGQA-3).

Fluxo escolhido como exemplo crítico em substituição de "Login", já que a
app não tem autenticação ativa. "Criar Owner" é o fluxo mais usado em todo
o sistema (pets, visitas, etc. dependem de um Owner existir primeiro).
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page

from pages.owner_page import OwnerPage


class TestCreateOwner:
    """Testes para a criação de Owners através do formulário "New Owner"."""

    def test_criar_owner_valido(self, page: Page) -> None:
        """
        TC-OWN-01 — Caminho feliz: criar um owner com todos os dados válidos.

        Espera-se que o owner seja criado com sucesso e apareça na lista.
        """
        owner_page = OwnerPage(page)
        owner_page.open_new_owner_form()

        owner_page.fill_owner_form(
            first_name="Maria",
            last_name="Silva",
            address="Rua das Flores, 123",
            city="Lisboa",
            telephone="9123456789",  # 10 dígitos — regra confirmada do backend
        )
        owner_page.submit()

        assert owner_page.owner_appears_in_list("Maria Silva"), (
            "O owner 'Maria Silva' deveria aparecer na lista após a criação "
            "com dados válidos."
        )

    @pytest.mark.xfail(
        reason=(
            "Bug conhecido (SPRINGQA-3; relacionado: SPRINGQA-2): o backend rejeita corretamente "
            "telefones com 9 dígitos (regra exige exatamente 10), mas a "
            "Angular UI não mostra nenhum erro ao utilizador — falha "
            "silenciosa. Este teste documenta o bug; remover o xfail quando "
            "o bug for corrigido."
        ),
        strict=False,
    )
    def test_criar_owner_telefone_9_digitos_bug_conhecido(self, page: Page) -> None:
        """
        Caso relacionado com SPRINGQA-TC-9 — telefone com 9 dígitos.

        Comportamento correto esperado: o sistema deveria rejeitar a
        submissão E mostrar um erro visível ao utilizador. Atualmente, a
        submissão falha "silenciosamente" (o owner não é criado, mas também
        não há nenhuma mensagem de erro na UI) — daí o `xfail`.
        """
        owner_page = OwnerPage(page)
        owner_page.open_new_owner_form()

        owner_page.fill_owner_form(
            first_name="Joao",
            last_name="TesteDigitos",
            address="Rua Teste, 1",
            city="Porto",
            telephone="123456789",  # 9 dígitos — deveria ser inválido
        )
        owner_page.submit()

        # Comportamento CORRETO esperado (ainda não implementado na app):
        # o owner não deve ser criado, e deve existir uma mensagem de erro
        # visível. Hoje a app só cumpre a primeira parte, silenciosamente.
        assert not owner_page.owner_appears_in_list("Joao TesteDigitos"), (
            "O owner não deveria ter sido criado com um telefone inválido."
        )
        # A UI ainda não mostra nenhuma mensagem (ver o motivo do xfail acima).
        owner_page.assert_visible("text=must be exactly 10 digits")
