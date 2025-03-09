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
        out = cli_plug(peter, '$scum.join')
        self.assertIn('ou joined', out, 'Cannot join scum game.')
        out = cli_plug(gizmore, '$scum.start')
        self.assertIn('started', out, 'Cannot start scum game.')


if __name__ == '__main__':
    unittest.main()
