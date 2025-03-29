from gdo.base.GDO import GDO
from gdo.base.Query import Query
from gdo.base.Render import Mode
from gdo.base.Trans import t
from gdo.core.GDO_User import GDO_User
from gdo.core.GDO_UserSetting import GDO_UserSetting
from gdo.table.MethodQueryTable import MethodQueryTable


class stats(MethodQueryTable):

    def gdo_trigger(self) -> str:
        return "scum.stats"

    def gdo_table_query(self) -> Query:
        return (GDO_UserSetting.table().
                select('uset_user_t.*').
                fetch_as(GDO_User.table()).
                where("uset_key='scum_points'").
                join_object('uset_user').
                order('uset_val DESC').
                limit(10, 10 * (self.get_page_num() - 1)))

    def render_gdo(self, gdo: GDO_User, mode: Mode):
        return t('scum_stat', (gdo.render_name(), gdo.get_setting_val('scum_points')))
