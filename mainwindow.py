from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox,QTableWidgetItem, QGraphicsScene
from PySide2.QtGui import QPen, QColor, QTransform
from PySide2.QtCore import Slot
from random import randint
from ui_mainwindow import Ui_MainWindow
from AlmacenP import AlmacenDeParticulas
from Particulas import Particula
from pprint import pprint, pformat
from collections import deque


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.AlmacenP = AlmacenDeParticulas()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.AgregarFinal.clicked.connect(self.click_agregar)
        self.ui.AgregarInicio.clicked.connect(self.click_agregarInicio)
        self.ui.Mostrar.clicked.connect(self.click_mostrar)

        self.ui.actionAbrir.triggered.connect(self.action_abrir_archivo)
        self.ui.actionGuardar.triggered.connect(self.action_guardar_archivo)

        self.ui.Mostrar_Tabla_Boton.clicked.connect(self.mostrar_tabla)
        self.ui.Buscar_Boton.clicked.connect(self.buscar_id)

        self.ui.Dibujar.clicked.connect(self.dibujar)
        self.ui.Limpiar.clicked.connect(self.limpiar)

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        self.ui.OrdId.clicked.connect(self.ordId)
        self.ui.OrdDistancia.clicked.connect(self.ordDistancia)
        self.ui.OrdVelocidad.clicked.connect(self.ordVelocidad)

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.Scene = QGraphicsScene()
        self.ui.GrafoF_graphicsView.setScene(self.Scene)
        self.ui.Mostrar_pushButton.clicked.connect(self.MostrarGrafo)
        self.ui.Limpiar_pushButton.clicked.connect(self.limpiarGrafo)

        self.ui.Recorrer.clicked.connect(self.Profundidad_Amplitud)

    @Slot()
    def Profundidad_Amplitud(self):
        self.ui.Recorrido_plainTextEdit.clear()
        grafo = dict()
        for Particulas in self.AlmacenP:
            OX = str(Particulas.OrigenX).upper()
            OY = str(Particulas.OrigenY).upper()
            DX = str(Particulas.DestinoX).upper()
            DY = str(Particulas.DestinoY).upper()
            Origen = OX, OY
            Destino = DX, DY

            if Origen in grafo:
                grafo[Origen].append(Destino)
            else:
                grafo[Origen] = [Destino]
            if Destino in grafo:
                grafo[Destino].append(Origen)
            else:
                grafo[Destino] = [Origen]

        UbicX = self.ui.BusquedaX_spinBox.value()
        UbicY = self.ui.BusquedaY_spinBox.value()
        UbicacionX = str(UbicX).upper()
        UbicacionY = str(UbicY).upper()
        Ubicacion = UbicacionX, UbicacionY
        if Ubicacion in grafo:
            adyacencia = Ubicacion
            visitados = []
            pila = deque()
            recorrido = []

            visitados.append(adyacencia)
            pila.append(adyacencia)
            while len(pila) != 0:
                vertice = pila[-1]
                recorrido.append(vertice)
                pila.pop()
                for ady in grafo[vertice]:
                    if ady not in visitados:
                        visitados.append(ady)
                        pila.append(ady)

            self.ui.Recorrido_plainTextEdit.insertPlainText('Profundidad\n')
            for parte in recorrido:
                self.ui.Recorrido_plainTextEdit.insertPlainText(str(parte))
                self.ui.Recorrido_plainTextEdit.insertPlainText('\n')
            self.ui.Recorrido_plainTextEdit.insertPlainText('\n\n')
            adyacencia2 = Ubicacion
            visitados2 = []
            cola = deque()
            recorrido2 = []
            visitados2.append(adyacencia2)
            cola.append(adyacencia2)
            while len(cola) != 0:
                vertice2 = cola[0]
                recorrido2.append(vertice2)
                cola.popleft()
                for ady2 in grafo[vertice2]:
                    if ady2 not in visitados2:
                        visitados2.append(ady2)
                        cola.append(ady2)
            self.ui.Recorrido_plainTextEdit.insertPlainText('Amplitud\n')
            for parte in recorrido2:
                self.ui.Recorrido_plainTextEdit.insertPlainText(str(parte))
                self.ui.Recorrido_plainTextEdit.insertPlainText('\n')
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Esta ubicacion no se encuentra en el grafo"
            )

    @Slot()
    def MostrarGrafo(self):
        grafo = dict()
        for Particulas in self.AlmacenP:
            OX = str(Particulas.OrigenX).upper()
            OY = str(Particulas.OrigenY).upper()
            DX = str(Particulas.DestinoX).upper()
            DY = str(Particulas.DestinoY).upper()
            DI = int(Particulas.Distancia)
            Origen = OX, OY
            Destino = DX, DY

            AristaOD = (DX, DY, DI)
            AristaDO = (OX, OY, DI)

            if Origen in grafo:
                grafo[Origen].append(AristaOD)
            else:
                grafo[Origen] = [AristaOD]
            if Destino in grafo:
                grafo[Destino].append(AristaDO)
            else:
                grafo[Destino] = [AristaDO]

        strn = pformat(grafo, width = 40, indent = 1)
        pprint(grafo, width = 40)
        for Particulas in self.AlmacenP:
            pen = QPen()
            pen.setWidth(2)
            color = QColor(Particulas.Red, Particulas.Green, Particulas.Blue)
            pen.setColor(color)
            self.Scene.addEllipse(Particulas.OrigenX, Particulas.OrigenY, 3, 3, pen)
            self.Scene.addEllipse(Particulas.DestinoX, Particulas.DestinoY, 3, 3, pen)
            self.Scene.addLine(Particulas.OrigenX + 3, Particulas.OrigenY + 3, Particulas.DestinoX, Particulas.DestinoY, pen)
        self.ui.Grafo_plainTextEdit.clear()
        self.ui.Grafo_plainTextEdit.insertPlainText(strn)

    @Slot()
    def limpiarGrafo(self):
        self.Scene.clear()
        self.ui.Grafo_plainTextEdit.clear()

    # def sort_by_Distancia(self.__lista):
    #     return self.__particulas.Distancia

    @Slot()
    def ordId(self):
        self.AlmacenP.ordenar()
    
    @Slot()
    def ordDistancia(self):
        self.AlmacenP.ordenarD()


    @Slot()
    def ordVelocidad(self):
        self.AlmacenP.ordenarV()

    @Slot()
    def dibujar(self):
        pen = QPen()
        pen.setWidth(3)
        for Particulas in self.AlmacenP:
            r = float(Particulas.Red)
            g = float(Particulas.Green)
            b = float(Particulas.Blue)
            # origen_x = randint(0, 500)
            # origen_y = randint(0, 500)
            # destino_x = randint(0, 500)
            # destino_y = randint(0, 500)
            color = QColor(r,g,b)
            pen.setColor(color)
            self.scene.addEllipse(float(Particulas.OrigenX) , float(Particulas.OrigenY), 3, 3, pen)
            self.scene.addEllipse(float(Particulas.DestinoX), float(Particulas.DestinoY), 3, 3, pen)
            self.scene.addLine(float(Particulas.OrigenX)+3, float(Particulas.OrigenY)+3, float(Particulas.DestinoX), float(Particulas.DestinoY), pen)

    def wheelEvent(self, event):
        if event.delta() > 0:
            self.ui.graphicsView.scale(1.2, 1.2)
        else:
            self.ui.graphicsView.scale(0.8, 0.8)
        if event.delta() > 0:
            self.ui.GrafoF_graphicsView.scale(1.2, 1.2)
        else:
            self.ui.GrafoF_graphicsView.scale(0.8, 0.8) 

    @Slot()
    def limpiar(self):
        self.scene.clear()

    @Slot()
    def buscar_id(self):
        Id = self.ui.Buscar.text()
        encontrado = False
        for Particulas in self.AlmacenP:
            if Id == str(Particulas.Id):
                self.ui.tableWidget.clear()
                self.ui.tableWidget.setRowCount(1)

                Id_widget = QTableWidgetItem(str(Particulas.Id))
                OrigenX_widget = QTableWidgetItem(str(Particulas.OrigenX))
                OrigenY_widget = QTableWidgetItem(str(Particulas.OrigenY))
                DestinoX_widget = QTableWidgetItem(str(Particulas.DestinoX))
                DestinoY_widget = QTableWidgetItem(str(Particulas.DestinoY))
                Velocidad_widget = QTableWidgetItem(str(Particulas.Velocidad))
                Red_widget = QTableWidgetItem(str(Particulas.Red))
                Green_widget = QTableWidgetItem(str(Particulas.Green))
                Blue_widget = QTableWidgetItem(str(Particulas.Blue))
                Distancia_widget = QTableWidgetItem(str(Particulas.Distancia))

                self.ui.tableWidget.setItem(0, 0, Id_widget)
                self.ui.tableWidget.setItem(0, 1, OrigenX_widget)
                self.ui.tableWidget.setItem(0, 2, OrigenY_widget)
                self.ui.tableWidget.setItem(0, 3, DestinoX_widget)
                self.ui.tableWidget.setItem(0, 4, DestinoY_widget)
                self.ui.tableWidget.setItem(0, 5, Velocidad_widget)
                self.ui.tableWidget.setItem(0, 6, Red_widget)
                self.ui.tableWidget.setItem(0, 7, Green_widget)
                self.ui.tableWidget.setItem(0, 8, Blue_widget)
                self.ui.tableWidget.setItem(0, 9, Distancia_widget)
                encontrado = True
                return
        if not encontrado:
            QMessageBox.warning(
                self,
                'Atencion',
                f'La particula con el Id "{Id}" no fue encontrado'
            )
                

    @Slot()
    def mostrar_tabla(self):
        #print('mostrar_tabla')
        self.ui.tableWidget.setColumnCount(10)
        headers = ["Id", "OrigenX", "OrigenY", "DestinoX","DestinoY", "Velocidad", "Red", "Green", "Blue", "Distancia"]
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)

        self.ui.tableWidget.setRowCount(len(self.AlmacenP))
        row = 0
        for Particulas in self.AlmacenP:
            Id_widget = QTableWidgetItem(str(Particulas.Id))
            OrigenX_widget = QTableWidgetItem(str(Particulas.OrigenX))
            OrigenY_widget = QTableWidgetItem(str(Particulas.OrigenY))
            DestinoX_widget = QTableWidgetItem(str(Particulas.DestinoX))
            DestinoY_widget = QTableWidgetItem(str(Particulas.DestinoY))
            Velocidad_widget = QTableWidgetItem(str(Particulas.Velocidad))
            Red_widget = QTableWidgetItem(str(Particulas.Red))
            Green_widget = QTableWidgetItem(str(Particulas.Green))
            Blue_widget = QTableWidgetItem(str(Particulas.Blue))
            Distancia_widget = QTableWidgetItem(str(Particulas.Distancia))

            self.ui.tableWidget.setItem(row, 0, Id_widget)
            self.ui.tableWidget.setItem(row, 1, OrigenX_widget)
            self.ui.tableWidget.setItem(row, 2, OrigenY_widget)
            self.ui.tableWidget.setItem(row, 3, DestinoX_widget)
            self.ui.tableWidget.setItem(row, 4, DestinoY_widget)
            self.ui.tableWidget.setItem(row, 5, Velocidad_widget)
            self.ui.tableWidget.setItem(row, 6, Red_widget)
            self.ui.tableWidget.setItem(row, 7, Green_widget)
            self.ui.tableWidget.setItem(row, 8, Blue_widget)
            self.ui.tableWidget.setItem(row, 9, Distancia_widget)

            row += 1
    
    @Slot()
    def action_abrir_archivo(self):
        #print('abrir_archivo')
        ubication = QFileDialog.getOpenFileName(
            self,
            'Abrir Archivo',
            '.',
            'JSON (*.json)'
        )[0]
        if self.AlmacenP.abrir(ubication):
            QMessageBox.information(
                self,
                "Exito",
                "Se abrio el archivo " + ubication
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Eror al abrir el archivo" + ubication
            )

    @Slot()
    def action_guardar_archivo(self):
        #print('Guardar_archivo')
        ubication = QFileDialog.getSaveFileName(
            self,
            'Guardar Archivo',
            '.',
            'JSON (*.json)'
        )[0]
        print(ubication)
        if self.AlmacenP.guardar(ubication):
            QMessageBox.information(
                self,
                "Exito",
                "Se pudo crear el archivo" + ubication
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo crear el archivo" + ubication
            )


    @Slot()
    def click_mostrar(self):
        #self.AlmacenP.mostrar()
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.insertPlainText(str(self.AlmacenP))
    
    @Slot()
    def click_agregar(self):
        Id = self.ui.Id_spinBox.value()
        OrigenX = self.ui.OrigenX_spinBox.value()
        OrigenY = self.ui.OrigenY_spinBox.value()
        DestinoX = self.ui.DestinoX_spinBox.value()
        DestinoY = self.ui.DestinoY_spinBox.value()
        Velocidad = self.ui.Velocidad_spinBox.value()
        Red = self.ui.Red_spinBox.value()
        Green = self.ui.Green_spinBox.value()
        Blue = self.ui.Blue_spinBox.value()
        Distancia = self.ui.Distancia_spinBox.value()

        Particulas = Particula(Id, OrigenX, OrigenY, DestinoX, DestinoY, Velocidad, Red, Green, Blue)
        self.AlmacenP.agregar_final(Particulas)

        # print(Id, OrigenX, OrigenY, DestinoX, DestinoY, Velocidad, Red, Green, Blue)
        # self.ui.plainTextEdit.insertPlainText(str(Id) + str(OrigenX) + str(OrigenY) + str(DestinoX) + str(DestinoY) + str(Velocidad) + str(Red) + str(Green) + str(Blue))
        
    @Slot()
    def click_agregarInicio(self):
        Id = self.ui.Id_spinBox.value()
        OrigenX = self.ui.OrigenX_spinBox.value()
        OrigenY = self.ui.OrigenY_spinBox.value()
        DestinoX = self.ui.DestinoX_spinBox.value()
        DestinoY = self.ui.DestinoY_spinBox.value()
        Velocidad = self.ui.Velocidad_spinBox.value()
        Red = self.ui.Red_spinBox.value()
        Green = self.ui.Green_spinBox.value()
        Blue = self.ui.Blue_spinBox.value()
        Distancia = self.ui.Distancia_spinBox.value()

        Particulas = Particula(Id, OrigenX, OrigenY, DestinoX, DestinoY, Velocidad, Red, Green, Blue)
        self.AlmacenP.agregar_inicio(Particulas)