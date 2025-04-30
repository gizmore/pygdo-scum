from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_RestOfText import GDT_RestOfText
from gdo.scum.Game import Game


class play(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'scum'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_RestOfText('cards').not_null(),
        ]

    async def gdo_execute(self) -> GDT:
        game = Game.instance(self._env_channel)
        if self.param_val('cards')[0] == 'p':
            return self.scum_pass(game)
        user = self._env_user
        if not game._started:
            return self.err('err_scum_not_started')
        if user not in game._players:
            return self.err('err_scum_player_not_in_game')
        if game.current_player() != self._env_user:
            return self.err('err_scum_not_your_turn')
        hand = game._hands[user.get_id()]
        cards = self.param_value('cards').split(' ')
        c = cards[0]
        cards2 = []
        for card in cards:
            if card != c:
                return self.err('err_scum_need_same_cards')
        count = 0
        for card in hand:
            if card[1:] == c:
                cards2.append(card)
                count += 1
                if count == len(cards):
                    break
        if count < len(cards):
            return self.err('err_scum_not_right_cards')
        if game._table:
            if game.CARD_ORDER[c] <= game.CARD_ORDER[game._table[0][1:]]:
                return self.err('err_scum_need_higher_cards', (game.render_cards(game._table),))
            if len(cards2) != len(game._table):
                return self.err('err_scum_need_amt_cards')
        game.play(user, cards2)
        if cards2[0][1] == 'A':
            self.msg('msg_scum_wins_round', (user.render_name(), game.render_cards(cards2), game.render_current_state()))
        elif user in game._finished:
            self.msg('msg_scum_played_cards_finished', (user.render_name(), game.render_cards(cards2), game.get_rank(user), game.get_points(user), game.render_current_state()))
            if game.is_over():
                await game.over()
        else:
            self.msg('msg_scum_played_cards', (user.render_name(), game.render_cards(cards2), len(game._hands[user.get_id()]), game.render_current_state()))
        return self.empty()

    def scum_pass(self, game: Game):
        game.passed(self._env_user)
        if game.all_passed():
            return self.msg('msg_scum_all_passed', (self._env_user.render_name(), game.current_player().render_name(), game.render_current_state()))
        return self.msg('msg_scum_passed', (self._env_user.render_name(), game.render_current_state()))
