from gdo.base.GDT import GDT
from gdo.scum.Game import Game
from gdo.scum.method.play import play


class pass_(play):
    """Pass the current Scum round without using a magic card argument."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'scum.pass'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'scpass'

    def gdo_parameters(self) -> list[GDT]:
        return []

    async def gdo_execute(self) -> GDT:
        return self.scum_pass(Game.instance(self._env_channel))
