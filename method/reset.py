from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.date.Time import Time
from gdo.scum.Game import Game


class reset(Method):

    def gdo_trigger(self) -> str:
        return 'scum.reset'

    def gdo_execute(self) -> GDT:
        game = Game.instance(self._env_channel)
        if game.can_reset():
            game.reset()
            return self.msg('msg_scum_reset')
        return self.err('err_scum_reset_timeout', (Time.human_duration(game.get_reset_timeout()),))
