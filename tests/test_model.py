import unittest

from src.domain.model import Plane, Jumper, JumpMaster, SitePlane, TypeJumper


class TestPlane(unittest.TestCase):

    def setUp(self):
        self.plane = Plane("Test Plane", "123456")
        self.jumper = Jumper("Test Jumper")
        self.jump_master = JumpMaster("Test Master")

    def test_add_jumper(self):
        """
        Adds a jumper to the plane at the specified position.

        :return: None
        """
        self.plane.add_jumper(self.jumper, 1, SitePlane.STARBOARD)
        self.assertEqual(self.plane.starboard_cargo()[TypeJumper.Jumper][1], self.jumper)

    def test_add_jump_master(self):
        self.plane.add_jump_master(self.jump_master, 1, SitePlane.STARBOARD)
        self.assertEqual(self.plane.starboard_cargo ()[TypeJumper.JumpMaster][1], self.jump_master)

    def test_add_invalid_place(self):
        with self.assertRaises(ValueError):
            self.plane.add_jumper(self.jumper, -1, SitePlane.STARBOARD)

    def test_str_method(self):
        self.assertEqual(str(self.plane), "Test Plane 123456")

    def test_repr_method(self):
        self.assertEqual(repr(self.plane), str(self.plane))



    def test_starboard_cargo_method(self):
        self.plane.add_jumper(self.jumper, 1, SitePlane.STARBOARD)
        starboard_cargo = self.plane.starboard_cargo()
        self.assertTrue(self.jumper in starboard_cargo[TypeJumper.Jumper].values())

    def test_broad_cargo_method(self):
        self.plane.add_jumper(self.jump_master, 1, SitePlane.BROAD)
        broad_cargo = self.plane.broad_cargo()
        self.assertTrue(self.jump_master in broad_cargo[TypeJumper.JumpMaster].values())


if __name__ == '__main__':
    unittest.main()
