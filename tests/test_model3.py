import unittest
from dataclasses import dataclass
from typing import Dict

from src.domain.model import Plane, SitePlane, TypeJumper, Jumper, JumpMaster, Soldier


class TestPlane(unittest.TestCase):
    def setUp(self):
        self.plane = Plane("Plane", "serial")
        self.jumper = Jumper(Soldier(serial="R" + str(1), name=f"soldier {1} JM", first_name=f"soldier {1}", rank="sm"))
        self.jump_master = JumpMaster(Soldier(serial="R" + str(2+ 99), name=f"soldier board JM {2}",
                                              first_name=f"soldier board {2}",rank="sm"))

    def test_add_jumper(self):
        self.plane.add_jumper(self.jumper, 1, SitePlane.STARBOARD)
        self.assertIn(1, self.plane._plane[SitePlane.STARBOARD][TypeJumper.Jumper])

    def test_add_jump_master(self):
        self.plane.add_jump_master(self.jump_master, 2, SitePlane.STARBOARD)
        self.assertIn(2, self.plane._plane[SitePlane.STARBOARD][TypeJumper.JumpMaster])

    def test_update_jumper(self):
        self.plane.add_jumper(self.jumper, 1, SitePlane.STARBOARD)
        jumper = Jumper(Soldier(serial="R" + str(1), name=f"soldier {1} JM", first_name=f"soldier {1}", rank="sm"))
        self.plane.update_jumper(jumper, 1, SitePlane.STARBOARD)
        self.assertEqual(jumper, self.plane._plane[SitePlane.STARBOARD][TypeJumper.Jumper][1])

    def test_delete_jumper(self):
        self.plane.add_jumper(self.jumper, 1, SitePlane.STARBOARD)
        self.plane.delete_jumper(1, SitePlane.STARBOARD)
        self.assertNotIn(1, self.plane._plane[SitePlane.STARBOARD][TypeJumper.Jumper])

    def test_update_jump_master(self):
        self.plane.add_jump_master(self.jump_master, 1, SitePlane.STARBOARD)
        jump_master = JumpMaster(Soldier(serial="R" + str(2+ 99), name=f"soldier board JM {2}",
                                              first_name=f"soldier board {2}",rank="sm"))
        self.plane.update_jump_master(jump_master, 1, SitePlane.STARBOARD)
        self.assertEqual(jump_master, self.plane._plane[SitePlane.STARBOARD][TypeJumper.JumpMaster][1])

    def test_delete_jump_master(self):
        self.plane.add_jump_master(self.jump_master, 1, SitePlane.STARBOARD)
        self.plane.delete_jump_master(1, SitePlane.STARBOARD)
        self.assertNotIn(1, self.plane._plane[SitePlane.STARBOARD][TypeJumper.JumpMaster])


    def test_starboard_cargo(self):
        starboard_cargo = self.plane.starboard_cargo()
        self.assertIsInstance(starboard_cargo, Dict)

    def test_broad_cargo(self):
        broad_cargo = self.plane.broad_cargo()
        self.assertIsInstance(broad_cargo, Dict)

    def test_jump_masters(self):
        masters = self.plane.jump_masters()
        self.assertIsInstance(masters, Dict)

    def test_jumpers(self):
        jumpers = self.plane.jumpers()
        self.assertIsInstance(jumpers, Dict)


if __name__ == "__main__":
    unittest.main()
