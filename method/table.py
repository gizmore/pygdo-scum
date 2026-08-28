from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.scum.Game import Game


class table(Method):
    """Show the public cards and whose turn it is in the current game."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'scum.table'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'sct'

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_in_private(self) -> bool:
        return False

    async def gdo_execute(self) -> GDT:
        game = Game.instance(self._env_channel)
        if not game._started:
            return self.err('err_scum_not_started')
        return self.msg('msg_scum_table', (game.render_current_state(),))
