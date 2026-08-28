from gdo.base.GDT import GDT
from gdo.base.Method import Method


class scum(Method):
    """Show the compact command overview for the Scum card game."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'scum'

    def gdo_execute(self) -> GDT:
        return self.reply('msg_scum_commands')
