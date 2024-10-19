import unittest

from src.domain.model import Plane, JumpMaster, SitePlane, TypeJumper


class TestModel(unittest.TestCase):

    def setUp(self):
        self.plane = Plane('TestPlane', '1234')

    def test_jump_masters(self):
        jm1 = JumpMaster('JM1')
        jm2 = JumpMaster('JM2')

        # add jump masters to the plane
        self.plane.add_jump_master(jm1, 1, SitePlane.STARBOARD)
        self.plane.add_jump_master(jm2, 2, SitePlane.STARBOARD)

        # testing jump masters
        jump_masters = self.plane.jump_masters()
        self.assertEqual(len(jump_masters), 2)
        self.assertIn(1, jump_masters)
        self.assertIn(2, jump_masters)
        self.assertEqual(jump_masters[1], jm1)
        self.assertEqual(jump_masters[2], jm2)

    def test_jump_masters_empty(self):
        # testing with no jump masters
        jump_masters = self.plane.jump_masters()
        self.assertEqual(len(jump_masters), 0)

    def test_jump_masters_partial(self):
        jm1 = JumpMaster('JM1')

        # add jump master to the slot 1
        self.plane.add_jump_master(jm1, 1, SitePlane.STARBOARD)

        # testing jump masters
        jump_masters = self.plane.jump_masters()
        self.assertEqual(len(jump_masters), 1)
        self.assertIn(1, jump_masters)
        self.assertEqual(jump_masters[1], jm1)

        # testing if there is no jump master at slot 2
        self.assertNotIn(2, jump_masters)


if __name__ == '__main__':
    unittest.main()
