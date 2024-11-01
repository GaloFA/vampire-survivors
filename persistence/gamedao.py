"""Interfaz de una clase DAO para reservas"""
from abc import abstractmethod, ABC

class GameDAO(ABC):
    """ Clase abstracta que da los métodos para posibilitar conectarse 
    a una fuente de datos en donde se guarden o modifiquen los mismos """
    @abstractmethod
    def add_game(self, world):
        """Agrega una nueva reserva a la base de datos.
        
        Ejemplo de uso: self.add_reservation('Sala A', inicio, fin)

        Args:
            room_name (str): El nombre de la sala a reservar.
            start_datetime (datetime): La fecha y hora de inicio de la reserva.
            end_datetime (datetime): La fecha y hora de fin de la reserva.

        Returns:
            None: Este método no devuelve ningún valor. Agrega la reserva a la base de datos.
        """

    @abstractmethod
    def remove_game(self, world):
        """Elimina una reserva de la base de datos.
        
        Ejemplo de uso: self.remove_reservation('Sala A', inicio)

        Args:
            room_name (str): El nombre de la sala cuya reserva se desea eliminar.
            start_datetime (datetime): La fecha y hora de inicio de la reserva a eliminar.

        Returns:
            None: Este método no devuelve ningún valor. Elimina la reserva de la base de datos.
        """
