import os
import random
import unittest

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.scum.method.cards import cards
from gdo.scum.method.init import init
from gdo.scum.method.join import join
from gdo.scum.method.play import play
from gdo.scum.method.pass_ import pass_
from gdo.scum.method.reset import reset
from gdo.scum.method.scum import scum
from gdo.scum.method.start import start
from gdo.scum.method.stats import stats
from gdo.scum.method.table import table
from gdotest.TestUtil import reinstall_module, WebPlug, GDOTestCase, cli_plug, cli_gizmore, cli_user


class ScumTest(GDOTestCase):

    def setUp(self):
        super().setUp()
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        loader = ModuleLoader.instance()
        loader.load_modules_db(True)
        reinstall_module('scum')
        loader.init_modules(True, True)
        Application.init_cli()
        loader.init_cli()
        WebPlug.COOKIES = {}

    def test_00_play_scum(self):
        random.seed(1337)
        peter = cli_user('peter')
        gizmore = cli_gizmore()
        out = cli_plug(gizmore, '$scum')
        self.assertIn('https://en.wikipedia.org/wiki/President_(card_game)', out)
        out = cli_plug(gizmore, '$scum.init')
        self.assertIn('has been initiated', out, 'Cannot init scum game.')
        out = cli_plug(gizmore, '$scum.start')
        self.assertIn('at least 2 players.', out, 'Can start single player.')
        out = cli_plug(peter, '$scum.join')
        self.assertIn('ou joined', out, 'Cannot join scum game.')
        out = cli_plug(gizmore, '$scum.start')
        self.assertIn('started', out, 'Cannot start scum game.')
        self.assertIn('our cards', out, 'Cannot start with scum game cards.')
        self.assertIn('come out fresh', out, 'Cannot get start state msg.')

        out = cli_plug(gizmore, '$scum.play 9')
        self.assertIn(peter.render_name(), out, 'gizmore cannot play 9.')
        out = cli_plug(gizmore, '$scum.table')
        self.assertIn('Cards on table', out, 'Cannot show the Scum table.')
        out = cli_plug(peter, '$scum.play 9')
        self.assertIn('higher cards than', out, 'peter can play low cards.')
        out = cli_plug(peter, '$scum.play 10')
        self.assertIn(gizmore.render_name(), out, 'peter cannot play 10.')
        out = cli_plug(gizmore, '$scum.play K K')
        self.assertIn('same number of cards', out, 'gizmore can play K K.')
        out = cli_plug(gizmore, '$scum.play A')
        self.assertIn('wins this round', out, 'gizmore cannot play A.')
        out = cli_plug(gizmore, '$scum.play K K')
        self.assertIn(f'{gizmore.render_name()} plays', out, 'gizmore cannot play K K.')
        out = cli_plug(peter, '$scum.pass')
        self.assertIn(f'{peter.render_name()} passes', out, 'peter cannot pass.')
        self.assertIn(f'{gizmore.render_name()} wins this round', out,
                      'All other players passing must award the trick immediately.')
        self.assertIn(f'It is {gizmore.render_name()}\'s turn', out,
                      'The trick winner must lead the next round.')
        out = cli_plug(gizmore, '$scum.cards')
        self.assertIn('our cards', out, 'gizmore cannot see cards.')
        out = cli_plug(gizmore, '$scum.stats')
        self.assertIn('Scum Stats', out, 'gizmore cannot show stats.')

    def test_01_command_entrypoint_hides_game_commands(self):
        self.assertEqual('scum', scum.gdo_trigger())
        self.assertEqual('scp', play.gdo_trig())
        self.assertTrue(all(command().gdo_method_hidden()
                            for command in (cards, init, join, pass_, play, reset, start, stats, table)))



if __name__ == '__main__':
    unittest.main()
