import os
import random
import unittest

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
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

        out = cli_plug(gizmore, '$scum 9')
        self.assertIn('peter{1}\'s turn', out, 'gizmore cannot play 9.')
        out = cli_plug(peter, '$scum 9')
        self.assertIn('higher cards than', out, 'peter can play low cards.')
        out = cli_plug(peter, '$scum 10')
        self.assertIn('gizmore{1}\'s turn', out, 'peter cannot play 10.')
        out = cli_plug(gizmore, '$scum K K')
        self.assertIn('same number of cards', out, 'gizmore can play K K.')
        out = cli_plug(gizmore, '$scum A')
        self.assertIn('wins this round', out, 'gizmore cannot play A.')
        out = cli_plug(gizmore, '$scum K K')
        self.assertIn('gizmore{1} plays', out, 'gizmore cannot play K K.')
        out = cli_plug(peter, '$scum pass')
        self.assertIn('peter{1} passes', out, 'peter cannot pass.')
        out = cli_plug(gizmore, '$scum pass')
        self.assertIn('gizmore{1} passes', out, 'all cannot pass.')
        out = cli_plug(peter, '$scum 10')
        self.assertIn('not have the right cards', out, 'peter can play 10.')
        out = cli_plug(peter, '$scum 7')
        self.assertIn('plays', out, 'peter cannot play 7.')
        out = cli_plug(gizmore, '$scum 8')
        self.assertIn('gizmore{1} plays', out, 'gizmore cannot play 8.')
        out = cli_plug(gizmore, '$scum.cards')
        self.assertIn('our cards', out, 'gizmore cannot see cards.')
        out = cli_plug(peter, '$scum pass')
        self.assertIn('peter{1} passes', out, 'peter cannot pass.')
        out = cli_plug(gizmore, '$scum 10')
        self.assertIn('gizmore{1} plays', out, 'gizmore cannot play 10.')
        out = cli_plug(peter, '$scum pass')
        self.assertIn('peter{1} passes', out, 'peter cannot pass.')
        out = cli_plug(gizmore, '$scum J')
        self.assertIn('gizmore{1} plays', out, 'gizmore cannot play J.')
        out = cli_plug(peter, '$scum pass')
        self.assertIn('peter{1} passes', out, 'peter cannot pass.')
        out = cli_plug(gizmore, '$scum Q')
        self.assertIn('and finishes with rank', out, 'gizmore cannot play Q.')


if __name__ == '__main__':
    unittest.main()
