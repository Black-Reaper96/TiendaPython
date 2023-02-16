from PyQt5 import QtWidgets, uic
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import MySQLdb


class Tienda(QtWidgets.QMainWindow):
    sumatorio = 0.0
    carrito = []
    def __init__(self):
        super(Tienda, self).__init__()
        uic.loadUi('tienda.ui', self)
        self.llenarlista_()
        # Aquí puedes añadir las conexiones de eventos para los widgets
        self.Cancelar.clicked.connect(self.cancelarboton)
        self.Comprar.clicked.connect(self.comprarboton)
        self.Factura.clicked.connect(self.imprimirfactura)
        self.ProductosTabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ProductosTabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ProductosTabla.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ProductosTabla.cellClicked.connect(self.funcionalclickearceldas)


    def funcionalclickearceldas(self):
        rows = self.ProductosTabla.selectedItems()

        if rows:
            fila = [dato.text() for dato in rows]
            print(fila)
        else:
            return
        self.carrito.append(str(''+fila[0]+': '+fila[5]+'€'))
        self.cestaPedido.addItem(str(''+fila[0]+': '+fila[5]+'€'))
        self.sumatorio = self.sumatorio + float(str(fila[5]))
        print(self.carrito)


    def cancelarboton(self):
        self.cestaPedido.clear()
        self.precioFinal.setText('')
        self.sumatorio = 0.0
        self.carrito = []

    def llenarlista_(self):
        # conexion a base de datos mysql existente
        miConexion = MySQLdb.connect(host='localhost', user='root', passwd='CursoDAM_2223', db='tiendavideojuegos')
        cur = miConexion.cursor()
        cur.execute("SELECT nombre, genero, plataforma, pegi, año_de_lanzamiento, precio, imagen FROM videojuego")
        items = []
        for nombre, genero, plataforma, pegi, año_de_lanzamiento, precio, imagen in cur.fetchall():
            var = nombre, genero, plataforma, pegi, año_de_lanzamiento, precio, imagen
            items.append(var)
        #print(items)
        fila = 0
        for item in items:
            #print(item[1])
            self.ProductosTabla.insertRow(fila)
            Nombre = QtWidgets.QTableWidgetItem(str(item[0]))
            Genero = QtWidgets.QTableWidgetItem(str(item[1]))
            Plataforma = QtWidgets.QTableWidgetItem(str(item[2]))
            PEGI = QtWidgets.QTableWidgetItem(str(item[3]))
            Lanzamiento = QtWidgets.QTableWidgetItem(str(item[4]))
            Precio = QtWidgets.QTableWidgetItem(str(item[5]))
            Imagen = QtWidgets.QTableWidgetItem(str(item[6]))
            self.ProductosTabla.setItem(fila, 0, Nombre)
            self.ProductosTabla.setItem(fila, 1, Genero)
            self.ProductosTabla.setItem(fila, 2, Plataforma)
            self.ProductosTabla.setItem(fila, 3, Lanzamiento)
            self.ProductosTabla.setItem(fila, 4, PEGI)
            self.ProductosTabla.setItem(fila, 5, Precio)
            self.ProductosTabla.setItem(fila, 6, Imagen)
            fila = fila + 1
        miConexion.close()

    def comprarboton(self):
        self.precioFinal.setText(str(self.sumatorio)+' €')

    def imprimirfactura(self):
        w, h = A4
        c = canvas.Canvas("factura.pdf", pagesize=A4)
        c.drawImage("Imagenes/comprar.png", 50, h-100, width=50, height=50)
        textImagen = c.beginText(100, h - 100)
        textImagen.setFont("Times-Roman", 20)
        textImagen.textLine('Videojuegos Jericor')
        text = c.beginText(50, h - 150)
        text.setFont("Times-Roman", 12)
        text.textLine('Factura Total:')
        text.textLine('')
        for x in self.carrito:
            text.textLine('     '+str(x))
        text.textLine('')
        text.textLine('     Total: '+str(self.sumatorio)+' €')
        c.drawText(textImagen)
        c.drawText(text)
        c.showPage()
        c.save()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication([sys.argv])
    tienda = Tienda()
    tienda.show()
    sys.exit(app.exec_())
