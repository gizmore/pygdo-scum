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
        # The game is keyed by the effective account, but a linked account
        # (for example Gizmore on IRC) must receive its secret hand through
        # the connector identity which actually issued this command.
        reply_to = self._env_reply_to or self._env_user
        # ``notice_enabled`` is the user's private-delivery preference.  Pass
        # the intent through GDO_User.send(); non-IRC connectors simply keep
        # their normal private-message transport.
        await reply_to.send(
            'msg_scum_your_cards',
            (game.render_cards(game._hands[self._env_user.get_id()]),),
            notice=True,
        )
        return self.empty()
