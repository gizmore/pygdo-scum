from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.core.GDT_UInt import GDT_UInt


class module_scum(GDO_Module):

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_UInt('max_players').initial('8').not_null(),
            GDT_UInt('scum_games').initial('0').not_null(),
        ]

    def cfg_max_players(self) -> int:
        return self.get_config_value('max_players')

    def gdo_user_config(self) -> list[GDT]:
        return [
            GDT_UInt('scum_played').not_null().initial('0'),
            GDT_UInt('scum_points').not_null().initial('0'),
            GDT_UInt('scum_won').not_null().initial('0'),
        ]
