from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.scum.Game import Game


class init(Method):

    def gdo_trigger(self) -> str:
        return 'scum.init'

    def gdo_parameters(self) -> [GDT]:
        return [
        ]

    def gdo_execute(self) -> GDT:
        game = Game.instance(self._env_channel)
        if game.is_inited():
            return self.err('err_scum_running')
        game.init()
        game.join(self._env_user)
        return self.msg('msg_scum_inited')
