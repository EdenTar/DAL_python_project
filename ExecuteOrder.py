from main import repo
from Order import Order
from Suppliers import Suppliers


idcounter = 1


def execute(location, topping):
    global idcounter
    supplier = repo.hats.update(topping)
    suppliername = repo.suppliers.find(supplier).name
    order = Order(idcounter, location, topping)
    idcounter = idcounter + 1
    repo.orders.insert(order)
    repo.conn.commit()
    f = open("output.txt", "a")
    f.write(topping + "," + suppliername+ "," + location+'\n')
    f.close()
