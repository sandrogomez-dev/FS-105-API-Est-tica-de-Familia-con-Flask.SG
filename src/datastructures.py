class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1  # Empezamos en 1 o el valor deseado para los IDs
        # Inicializamos con los 3 miembros requeridos
        self._members = [
            {
                "id": self._generate_id(),
                "first_name": "John",
                "last_name": self.last_name, # Asegúrate de usar self.last_name
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": self._generate_id(),
                "first_name": "Jane",
                "last_name": self.last_name, # Asegúrate de usar self.last_name
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": self._generate_id(),
                "first_name": "Jimmy",
                "last_name": self.last_name, # Asegúrate de usar self.last_name
                "age": 5,
                "lucky_numbers": [1]
            }
        ]

    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        # Si el miembro ya tiene un ID, lo usamos. Si no, generamos uno nuevo.
        # Esto es útil para los tests que a veces proveen un ID.
        if "id" not in member:
            member["id"] = self._generate_id()
        
        # Asegúrate de que el apellido se establezca correctamente
        member["last_name"] = self.last_name
        
        self._members.append(member)
        return member # Retornamos el miembro completo para que Flask lo pueda jsonify

    def delete_member(self, id):
        original_len = len(self._members)
        self._members = [member for member in self._members if member["id"] != id]
        if len(self._members) < original_len:
            return {"done": True}
        return {"done": False} # Si el ID no se encontró, "done" es False

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    def get_all_members(self):
        return self._members