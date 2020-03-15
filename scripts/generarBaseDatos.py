from sqlite3 import dbapi2

try:
    bd = dbapi2.connect("base.dat")
    cursor = bd.cursor()

    cursor.execute("DROP TABLE productos")
    cursor.execute("DROP TABLE clientes")

    cursor.execute("CREATE TABLE productos(id INTEGER PRIMARY KEY, name TEXT , desc TEXT, precio NUMBER, stock NUMBER, cliente NUMBER)")

    cursor.execute("INSERT INTO productos(name, desc, precio, stock, cliente) VALUES('Gafas de sol','Gafas de sol de marca Rayban', 300, 2, 1)")
    cursor.execute("INSERT INTO productos(name, desc, precio, stock, cliente) VALUES('Bufanda','Bufanda de marca Zara', 50, 6, 1)")
    cursor.execute("INSERT INTO productos(name, desc, precio, stock, cliente) VALUES('Pantalón','Pantalón vaquero', 40, 16, 2)")
    cursor.execute("INSERT INTO productos(name, desc, precio, stock, cliente) VALUES('Plátano','Plátano de canarias', 2, 11, 3)")
    cursor.execute("INSERT INTO productos(name, desc, precio, stock, cliente) VALUES('Jamón ibérico','Jamón ibérico de bellota de marca Argal', 500, 1, 4)")

    cursor.execute("CREATE TABLE clientes(id INTEGER PRIMARY KEY, dni TEXT, name TEXT, apel1 TEXT, apel2 TEXT, tlf NUMBER)")

    cursor.execute("INSERT INTO clientes(dni, name, apel1, apel2, tlf) VALUES('123456789A', 'Pedro', 'Sánchez', 'Rajoy', 987643210)")
    cursor.execute("INSERT INTO clientes(dni, name, apel1, apel2, tlf) VALUES('123456789B', 'Ana', 'Miras', 'Luque', 987643211)")
    cursor.execute("INSERT INTO clientes(dni, name, apel1, apel2, tlf) VALUES('123456789C', 'Alberto', 'Fernandez', 'Fernandez', 987643212)")
    cursor.execute("INSERT INTO clientes(dni, name, apel1, apel2, tlf) VALUES('123456789D', 'Ana', 'Domínguez', 'Navarrete', 987643213)")
    cursor.execute("INSERT INTO clientes(dni, name, apel1, apel2, tlf) VALUES('123456789E', 'Gabriel', 'Fernandez', 'Fernandez', 987643214)")
    cursor.execute("INSERT INTO clientes(dni, name, apel1, apel2, tlf) VALUES('123456789F', 'Pepe', 'Fernandez', 'Fernandez', 987643215)")
    cursor.execute("INSERT INTO clientes(dni, name, apel1, apel2, tlf) VALUES('123456789G', 'María', 'Fernandez', 'Fernandez', 987643216)")
    cursor.execute("INSERT INTO clientes(dni, name, apel1, apel2, tlf) VALUES('123456789H', 'Eustaquio', 'Fernandez', 'Fernandez', 987643217)")
    cursor.execute("INSERT INTO clientes(dni, name, apel1, apel2, tlf) VALUES('123456789J', 'Susana', 'Fernandez', 'Fernandez', 987643218)")
    cursor.execute("INSERT INTO clientes(dni, name, apel1, apel2, tlf) VALUES('123456789K', 'Antía', 'Fernandez', 'Fernandez', 987643219)")

    bd.commit()

    print("\nproductos(id INTEGER PRIMARY KEY, name TEXT , desc TEXT, precio NUMBER, stock NUMBER, cliente NUMBER)")
    productos = cursor.execute("SELECT * FROM productos")
    for producto in productos:
        print(producto)

    print("\nclientes(id INTEGER PRIMARY KEY, dni TEXT, name TEXT, apel1 TEXT, apel2 TEXT, tlf NUMBER)")
    clientes = cursor.execute("SELECT * FROM clientes")
    for cliente in clientes:
        print(cliente)

except(dbapi2.DatabaseError) as error:
    print(error)

finally:
    cursor.close()
    bd.close()
