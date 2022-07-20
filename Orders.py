from Order import Order


class Orders:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, orderDTO):  # insert Student DTO
        self.conn.execute("""
               INSERT INTO orders (id, location, hat) VALUES (?, ?, ?)
           """, [orderDTO.id, orderDTO.location, orderDTO.hat])

    def find(self, id):  # retrieve Student DTO
        c = self.conn.cursor()
        c.execute("""
            SELECT id, location, hat FROM orders WHERE id = ?
        """, [id, ])
        return Order(*c.fetchone())
