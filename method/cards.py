from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.scum.Game import Game


class cards(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'scum.cards'

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_in_private(self) -> bool:
        return False

    async def gdo_execute(self) -> GDT:
        game = Game.instance(self._env_channel)
        # A hand is secret game state. Deliver it through the connector's
        # private-user path (Discord DM, IRC query, TCP client, …), never the
        # table's channel.
        await self._env_user.send('msg_scum_your_cards', (game.render_cards(game._hands[self._env_user.get_id()]),))
        return self.empty()
