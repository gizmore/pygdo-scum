from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.scum.Game import Game


class cards(Method):

    def gdo_trigger(self) -> str:
        return 'scum.cards'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_execute(self) -> GDT:
        game = Game.instance(self._env_channel)
        return self.msg('msg_scum_your_cards', (game.render_cards(game._hand[self._env_user.get_id()]),))
