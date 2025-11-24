
class Body:
    """
    Représente un corps.
    """

    def __init__(self, mass, position, velocity):
        """
        Constructeur du corps.

        mass      float  Masse du corps.
        position  liste  Position du corps
        velocity  liste  Vitesse du corps
        """
        self.mass = mass
        self.position = position
        self.velocity = velocity


class System:
    """
    Représente un ensemble de corps.
    """

    def __init__(self, bodies):
        """
        bodies : liste d'objets Body.
        """
        self.bodies = bodies

    def get_masses(self):
        """
        Retourne la liste des masses des corps.
        """
        return [body.mass for body in self.bodies]

    def get_positions(self):
        """
        Retourne la liste des positions des corps.
        """
        return [body.position for body in self.bodies]

    def get_velocities(self):
        """
        Retourne la liste des vitesses des corps.
        """
        return [body.velocity for body in self.bodies]
