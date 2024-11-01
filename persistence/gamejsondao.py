""" Módulo que contiene el DAO para la Reserva usando JSON """
import json
import os
from business.mydatetime import DateTime
from persistence.reservation.reservationdao import ReservationDAO

class GameJsonDAO(GameDAO):
    """ Maneja la conexión con el archivo JSON para reservas """
    def __init__(self, json_path='data/json/reservations.json'):
        self.json_path = json_path
        self._initialize_file()

    def _initialize_file(self):
        if not os.path.exists(self.json_path):
            with open(self.json_path, 'w', encoding='utf-8') as file:
                json.dump([], file)

    def add_reservation(self, room_name, start_datetime: DateTime, end_datetime: DateTime):

        reservation = {
            'room_name': room_name,
            'start_datetime': str(start_datetime),
            'end_datetime': str(end_datetime)
        }
        reservations = self.list_reservations()
        reservations.append(reservation)

        with open(self.json_path, 'w', encoding='utf-8') as file:
            json.dump(reservations, file)

    def remove_reservation(self, room_name, start_datetime: DateTime):

        reservations = self.list_reservations()
        reservations = [res for res in reservations if not (res['room_name'] == room_name and res['start_datetime'] == str(start_datetime))]

        with open(self.json_path, 'w', encoding='utf-8') as file:
            json.dump(reservations, file)

    def list_reservations(self):

        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                data = file.read().strip()
                if not data:
                    return []

                reservations = json.loads(data)
                return [{"room_name": res["room_name"], "start_datetime": res["start_datetime"], "end_datetime": res["end_datetime"]}
                        for res in reservations]
        except (json.JSONDecodeError, KeyError):
            return []