from dataclasses import dataclass
from enum import Enum
from typing import Dict


class SitePlane (Enum):
    BROAD = 1
    STARBOARD = 2


class TypeJumper (Enum):
    Jumper = 1
    JumpMaster = 2


@dataclass
class Soldier:
    serial: str
    name: str
    first_name: str
    rank: str

    def __str__ (self):
        return f"{self.serial} {self.name} {self.first_name} {self.rank}"

    def __repr__ (self):
        return str (self)

    def __eq__ (self, other):
        return self.serial == other.serial

    def __hash__ (self):
        return hash (self.serial)


@dataclass
class Jumper:
    soldier: Soldier
    jump_count: int = 0

    def __str__ (self):
        return f"{self.soldier.serial} {self.jump_count} {self.soldier.name} {self.soldier.first_name} {self.soldier.rank}"

    def __repr__ (self):
        return str (self)


    def __hash__ (self):
        return hash (self.soldier.serial)


@dataclass
class JumpMaster (Jumper):
    drop_count: int = 0


@dataclass
class Plane:
    name: str
    serial: str
    _plane: Dict[SitePlane, Dict[TypeJumper, Dict[int, Jumper | JumpMaster]]] = None

    def __post_init__ (self):
        self._plane = {
            SitePlane.STARBOARD: {TypeJumper.Jumper: {}, TypeJumper.JumpMaster: {}},
            SitePlane.BROAD: {TypeJumper.Jumper: {}, TypeJumper.JumpMaster: {}}
        }

    def add_jumper (self, jumper: Jumper, place_nr: int, site_planed: SitePlane):
        self._add (jumper, place_nr, site_planed)

    def add_jump_master (self, jump_master: JumpMaster, place_nr: int, site_planed: SitePlane):
        self._add (jump_master, place_nr, site_planed)

    def update_jumper (self, jumper: Jumper, place_nr: int, site_planed: SitePlane):
        self._plane[site_planed][TypeJumper.Jumper][place_nr] = jumper

    def delete_jumper (self, place_nr: int, site_planed: SitePlane):
        del self._plane[site_planed][TypeJumper.Jumper][place_nr]

    def delete_jump_master (self, place_nr: int, site_planed: SitePlane):
        del self._plane[site_planed][TypeJumper.JumpMaster][place_nr]

    def update_jump_master (self, jump_master: JumpMaster, place_nr: int, site_planed: SitePlane):
        self._plane[site_planed][TypeJumper.JumpMaster][place_nr] = jump_master


    def _add (self, participant: Jumper, place_nr: int, site_planed: SitePlane) -> None:
        if isinstance (place_nr, int) and 1 <= place_nr <= 30:
            type_jumper = TypeJumper.Jumper if isinstance (participant, Jumper) and not isinstance (participant,
                                                                                                    JumpMaster) else TypeJumper.JumpMaster
            self._plane[site_planed][type_jumper][place_nr] = participant
        else:
            raise ValueError ("Invalid place number")


    def __str__ (self):
        return f"{self.name} {self.serial}"

    def __repr__ (self):
        return str (self)

    def cargo (self) -> str:
        output = "Aircraft cargo Jumpers and jump masters:\n"
        starboard_jump_masters = self._plane[SitePlane.STARBOARD][TypeJumper.JumpMaster]
        broad_jumper_masters = self._plane[SitePlane.BROAD][TypeJumper.JumpMaster]
        starboard_jumpers = self._plane[SitePlane.STARBOARD][TypeJumper.Jumper]
        broad_jumpers = self._plane[SitePlane.BROAD][TypeJumper.Jumper]
        for i in range (1,6):
            output += f"* Seat {i} : {starboard_jump_masters.get(i, '').soldier.serial} ** Seat {i} : {broad_jumper_masters.get(i, '').soldier.serial} * \n"
        for i in range (6, 31):
            output += f"* Seat {i} : {starboard_jumpers.get (i, '').soldier.serial} ** Seat {i} : {broad_jumpers.get (i, '').soldier.serial} * \n"
        return output

    def starboard_cargo (self) -> Dict:
        return self._plane[SitePlane.STARBOARD]

    def broad_cargo (self):
        return self._plane[SitePlane.BROAD]

    def jump_masters(self)->Dict[int, JumpMaster]:
        return self._plane[SitePlane.STARBOARD][TypeJumper.JumpMaster]

    def jumpers(self)->Dict[int, Jumper]:
        return self._plane[SitePlane.STARBOARD][TypeJumper.Jumper]



if __name__ == '__main__':
    p = Plane ("c-130", "h500")
    for c in range (1,6):
        jm1 = JumpMaster(Soldier(serial="R" + str(c), name=f"soldier {c} JM", first_name=f"soldier {c}", rank="sm"))
        p.add_jumper(jm1, c, SitePlane.STARBOARD)
        jm2 = JumpMaster(Soldier(serial="R" + str(c + 99), name=f"soldier board JM {c}", first_name=f"soldier board {c}",
                            rank="sm"))
        p.add_jumper(jm2, c, SitePlane.BROAD)
    for c in range (6, 31):
        j1 = Jumper (Soldier (serial="R"+str (c), name=f"soldier {c}", first_name=f"soldier {c}", rank="sm"))
        p.add_jumper (j1, c, SitePlane.STARBOARD)
        j2 = Jumper (Soldier (serial="R"+str (c + 99), name=f"soldier board j2 {c}", first_name=f"soldier board {c}",
                              rank="sm"))
        p.add_jumper (j2, c, SitePlane.BROAD)
    jumpers = p.starboard_cargo ()[TypeJumper.Jumper]
    print (p.cargo ())

    for t in jumpers.values ():
        print (t)
