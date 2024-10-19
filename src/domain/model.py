from enum import Enum
from pydoc import plain
from time import sleep
from typing import Dict


class SitePlaned (Enum):
    BROAD = 1
    STARBOARD = 2

class TypeJumper (Enum):
    Jumper = 1
    JumpMaster = 2


class Soldier:
    def __init__ (self, serial, name: str, for_name: str,rank:str):
        self.serial = serial
        self.name: str = name
        self.for_name: str = for_name
        self.rank: str =rank

    def __str__(self):
        return f"{self.serial} {self.name} {self.for_name} {self.rank}"
    def __repr__(self):
        return f"{self.serial} {self.name} {self.for_name} {self.rank}"

    def __eq__(self, other):
        return self.serial == other.serial
    def __hash__(self):
        return hash(self.serial)


class Jumper:
    def __init__ (self, jump_soldier: Soldier):
        self._soldier = jump_soldier
        self._jump_count = 0

    def __str__ (self):
        return f"{self._soldier.serial} {self._jump_count} {self._soldier.name} {self._soldier.for_name} {self._soldier.rank}"

    def __repr__ (self):
        return f"{self._soldier.serial} {self._jump_count} {self._soldier.name} {self._soldier.for_name} {self._soldier.rank}"

    def  __eq__(self, other):
        return self._soldier.serial == other._soldier.serial

    def __hash__(self):
        return hash(self._soldier.serial)


class JumpMaster:
    def __init__ (self, drop_soldier: Soldier):
        self.soldier = drop_soldier
        self.drop_count = 0
        self.jump_count = 0

    def __str__ (self):
        return f"{self._soldier.serial} {self._jump_count} {self._soldier.name} {self._soldier.for_name} {self._soldier.rank}"

    def __repr__ (self):
        return f"{self._soldier.serial} {self._jump_count} {self._soldier.name} {self._soldier.for_name} {self._soldier.rank}"

    def __eq__ (self, other):
        return self._soldier.serial == other._soldier.serial

    def __hash__ (self):
        return hash (self._soldier.serial)


class Plane:
    def __init__ (self, name, serial):
        self._name = name
        self._serial = serial
        self._broad_jumpers = {}
        self._starBoard_jumpers = {}
        self._broad_droppers = {}
        self._starBoard_droppers = {}
        self._plane: Dict[SitePlaned, Dict[TypeJumper, Dict[str, Jumper | JumpMaster]]]= {
            SitePlaned.STARBOARD: {TypeJumper.Jumper: {}, TypeJumper.JumpMaster: {}},
            SitePlaned.BROAD: {TypeJumper.Jumper: {}, TypeJumper.JumpMaster: {}}}

    def add_jumper (self, jumper: Jumper, place_nr: int, site_planed: str):
       self._add(jumper, place_nr, site_planed)

    def add_jump_master (self, jump_master: JumpMaster, place_nr, site_planed: SitePlaned):
        self._add (jump_master, place_nr, site_planed)

    def _add(self, jumper: Jumper, place_nr: int, site_planed: SitePlaned)->None:
        if isinstance (place_nr, int) or place_nr < 0 or place_nr > 30:
           if type(jumper) == Jumper:
               type_jumper = TypeJumper.Jumper
           else:
               type_jumper = TypeJumper.JumpMaster
           self._plane[site_planed][type_jumper][place_nr] = jumper

    def __str__(self):
        return f"{self._name} {self._serial}"
    def __repr__(self):
        return f"{self._name} {self._serial}"

    def cargo(self)->str:
        output = ""
        for i in range(5,30):
            output += f"{self._plane[SitePlaned.STARBOARD][TypeJumper.Jumper][i]} \
                      {self._plane[SitePlaned.BROAD][TypeJumper.Jumper][i]} \n"
        return output

    def starboard_cargo(self) -> {}:
        return self._plane[SitePlaned.STARBOARD]

    def broad_cargo(self):
        return self._plane[SitePlaned.BROAD]



if __name__ == '__main__':
    p=Plane("c-130","h500")

    for c in range(5,30):
        j1 = Jumper (Soldier (name=f"soldier {c}",for_name=f"soldier {c}",rank="master",serial=str(c)))
        p.add_jumper(j1,c, SitePlaned.STARBOARD )

        j2 = Jumper (Soldier (name=f"soldier board j2 {c}", for_name=f"soldier board {c}", rank="master board", serial=str (c+99)))
        p.add_jumper (j2, c, SitePlaned.BROAD)

    jumpers = p.starboard_cargo ()[TypeJumper.Jumper]

    print(p.cargo())

