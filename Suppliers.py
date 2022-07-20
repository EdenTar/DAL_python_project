from Supplier import Supplier


class Suppliers:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, supplierDTO):  # insert Student DTO
        self.conn.execute("""
               INSERT INTO suppliers (id, name) VALUES (?, ?)
           """, [supplierDTO.id, supplierDTO.name])

    def find(self, id):  # retrieve Student DTO
        c = self.conn.cursor()
        c.execute("""
            SELECT id, name FROM suppliers WHERE id = ?
        """, [id])
        return Supplier(*c.fetchone())
