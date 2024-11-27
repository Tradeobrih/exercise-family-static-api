
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = []

    # Método privado para generar IDs únicos
    def _generateId(self):
        return randint(0, 99999999)

    # Agregar un miembro a la familia
    def add_member(self, member):
        if "id" not in member:
            member["id"] = self._generateId()
        self._members.append(member)
        return member

    # Eliminar un miembro de la familia por ID
    def delete_member(self, id):
        for member in self._members:
            if member["id"] == id:
                self._members.remove(member)
                return True
        return False

    # Obtener un miembro específico por ID
    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    # Obtener todos los miembros de la familia
    def get_all_members(self):
        return self._members