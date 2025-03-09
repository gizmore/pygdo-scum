from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.scum.Game import Game


class join(Method):

    def gdo_trigger(self) -> str:
        return 'scum.join'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_execute(self) -> GDT:
        game = Game.instance(self._env_channel)
        if not game._inited:
            return self.err('err_scum_no_game')
        if game._started:
            return self.err('err_scum_already_started')
        if self._env_user in game._players:
            return self.err('err_scum_already_in_game')
        if game.is_full():
            return self.err('err_game_full')
        game.join(self._env_user)
        return self.msg('msg_scum_joined')
