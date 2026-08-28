from gdo.base.GDO import GDO
from gdo.base.Query import Query
from gdo.base.Render import Mode
from gdo.base.Trans import t
from gdo.core.GDO_User import GDO_User
from gdo.table.MethodQueryTable import MethodQueryTable


class stats(MethodQueryTable):

    @classmethod
    def gdo_trigger(cls) -> str:
        return "scum.stats"

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_table(self) -> GDO:
        return GDO_User.table()

    def gdo_table_query(self) -> Query:
        return (GDO_User.table().
                select().
                join('JOIN gdo_usersetting ON gdo_usersetting.uset_user=gdo_user.user_id').
                where("gdo_usersetting.uset_key='scum_points'").
                order('gdo_usersetting.uset_val DESC').
                limit(10, 10 * (self.get_page_num() - 1)))

    def render_gdo(self, gdo: GDO_User, mode: Mode):
        return t('scum_stat', (gdo.render_name(), gdo.get_setting_val('scum_points')))
