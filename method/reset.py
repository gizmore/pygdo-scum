from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.date.Time import Time
from gdo.scum.Game import Game


class reset(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'scum.reset'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_execute(self) -> GDT:
        game = Game.instance(self._env_channel)
        if time_left := game.can_reset():
            return self.err('err_scum_reset_timeout', (Time.human_duration(time_left),))
        game.reset()
        return self.msg('msg_scum_reset')
