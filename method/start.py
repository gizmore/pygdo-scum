from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.Util import Strings, Arrays
from gdo.scum.Game import Game


class start(Method):

    def gdo_trigger(self) -> str:
        return 'scum.start'

    def gdo_in_private(self) -> bool:
        return False

    async def gdo_execute(self) -> GDT:
        game = Game.instance(self._env_channel)
        if not game._inited:
            return self.err('err_scum_no_game')
        if game._started:
            return self.err('err_scum_already_started')
        if len(game._players) < 2:
            return self.err('err_at_least_2_players')
        await game.start()
        self.msg('msg_scum_started', (Arrays.human_join(game.render_players()),))
        await game.send_status()
        return self.empty()
