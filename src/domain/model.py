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
    """
    Represents a Soldier with a unique serial number, name, first name, and rank.

    Attributes:
        serial (str): The unique serial number of the soldier.
        name (str): The last name of the soldier.
        first_name (str): The first name of the soldier.
        rank (str): The rank of the soldier.

    Methods:
        __str__(): Returns a string representation of the Soldier object.
        __repr__(): Returns a string representation of the Soldier object.
        __eq__(other): Checks if another Soldier object is equal to this one based on the serial number.
        __hash__(): Returns the hash of the Soldier's serial number.
    """
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
    """
    A class to represent a Jumper.

    Attributes:
        soldier (Soldier): The soldier associated with this jumper.
        jump_count (int): The number of jumps the jumper has performed. Defaults to 0.

    Methods:
        __str__(): Returns a string representation of the jumper in the format
            "<serial> <jump_count> <name> <first_name> <rank>".
        __repr__(): Returns the same string representation as __str__().
        __hash__(): Returns a hash value based on the soldier's serial number.
    """
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
    """
        Represents an aircraft with capabilities to manage jumpers and jump masters on board.

        :param name: The name of the plane.
        :type name: str
        :param serial: The serial number of the plane.
        :type serial: str
        :param _plane: Dictionary representing the layout and occupants of the plane.
        :type _plane: Dict[SitePlane, Dict[TypeJumper, Dict[int, Jumper | JumpMaster]]]

        :ivar name: The name of the plane.
        :ivar serial: The serial number of the plane.
        :ivar _plane: Internal dictionary to track the occupants on the plane.
    """
    name: str
    serial: str
    _plane: Dict[SitePlane, Dict[TypeJumper, Dict[int, Jumper | JumpMaster]]] = None

    def __post_init__ (self):
        self._plane = {
            SitePlane.STARBOARD: {TypeJumper.Jumper: {}, TypeJumper.JumpMaster: {}},
            SitePlane.BROAD: {TypeJumper.Jumper: {}, TypeJumper.JumpMaster: {}}
        }

    def add_jumper (self, jumper: Jumper, place_nr: int, site_planed: SitePlane):
        """
        :param jumper: An instance of Jumper that needs to be added.
        :param place_nr: The place number where the jumper will be added.
        :param site_planed: The site plane where the jumper will be placed.
        :return: None.
        """
        self._add (jumper, place_nr, site_planed)

    def add_jump_master (self, jump_master: JumpMaster, place_nr: int, site_planed: SitePlane):
        """
        :param jump_master: Instance of JumpMaster to be added.
        :param place_nr: Integer indicating the place number.
        :param site_planed: Instance of SitePlane indicating the planned site.
        :return: None
        """
        self._add (jump_master, place_nr, site_planed)

    def update_jumper (self, jumper: Jumper, place_nr: int, site_planed: SitePlane):
        """
        :param jumper: Jumper object to place at the specified location
        :param place_nr: Index indicating the location within the site plane where the jumper should be placed
        :param site_planed: SitePlane object representing the plane where the jumper will be placed
        :return: None
        """
        self._plane[site_planed][TypeJumper.Jumper][place_nr] = jumper

    def delete_jumper (self, place_nr: int, site_planed: SitePlane):
        """
        :param place_nr: The numerical identifier for the jumper to be deleted.
        :param site_planed: An instance of SitePlane representing the location from which the jumper should be removed.
        :return: None
        """
        del self._plane[site_planed][TypeJumper.Jumper][place_nr]

    def delete_jump_master (self, place_nr: int, site_planed: SitePlane):
        """
        :param place_nr: The index number of the JumpMaster to be deleted.
        :param site_planed: The SitePlane instance from which the JumpMaster is to be removed.
        :return: None
        """
        del self._plane[site_planed][TypeJumper.JumpMaster][place_nr]

    def update_jump_master (self, jump_master: JumpMaster, place_nr: int, site_planed: SitePlane):
        """
        :param jump_master: Instance of JumpMaster to be assigned.
        :param place_nr: Integer representing the place number in the plane.
        :param site_planed: SitePlane object specifying the plane to update.
        :return: None
        """
        self._plane[site_planed][TypeJumper.JumpMaster][place_nr] = jump_master


    def _add (self, participant: Jumper, place_nr: int, site_planed: SitePlane) -> None:
        """
        :param participant: The jumper or jump master to be added to the plane.
        :type participant: Jumper
        :param place_nr: The designated place number for the participant.
        :type place_nr: int
        :param site_planed: The plane site where the participant will be added.
        :type site_planed: SitePlane
        :return: None
        :raises ValueError: If the place number is not within the valid range (1-30).
        """
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
        """
        :return: A formatted string containing the details of Aircraft cargo, including Jumpers and Jump Masters. The string lists each seat and the serial number of the soldier occupying it, for both starboard and broad sides of the plane.
        """
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
        """
        :return: The cargo on the starboard side of the plane.
        :rtype: Dict
        """
        return self._plane[SitePlane.STARBOARD]

    def broad_cargo (self):
        """
        :return: The broad cargo data from the plane.
        """
        return self._plane[SitePlane.BROAD]

    def jump_masters(self)->Dict[int, JumpMaster]:
        """
        :return: A dictionary where keys are integers and values are JumpMaster instances representing the jump masters on the starboard side of the plane.
        """
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
