from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QSpinBox, QToolBar, QPushButton
from qgis.utils import iface

class AzimuthEditor:
    def __init__(self, iface):
        self.iface = iface
        self.toolbar = None
        self.spin = None

    def initGui(self):
        # vytvoření toolbaru
        self.toolbar = QToolBar("Azimuth Editor")
        self.iface.addToolBar(self.toolbar)

        # tlačítko mínus
        self.btn_minus = QPushButton("–")
        self.btn_minus.setFixedWidth(15)
        self.btn_minus.clicked.connect(self.decrease_azimuth)
        self.toolbar.addWidget(self.btn_minus)

        # číselník (0–360)
        self.spin = QSpinBox()
        self.spin.setRange(0, 360)
        self.spin.setSingleStep(1)
        self.spin.setValue(0)
        self.spin.valueChanged.connect(self.update_azimuth)
        self.toolbar.addWidget(self.spin)

        # tlačítko plus
        self.btn_plus = QPushButton("+")
        self.btn_plus.setFixedWidth(15)
        self.btn_plus.clicked.connect(self.increase_azimuth)
        self.toolbar.addWidget(self.btn_plus)

    def unload(self):
        # odstranění toolbaru při vypnutí pluginu
        if self.toolbar:
            self.iface.mainWindow().removeToolBar(self.toolbar)
            self.toolbar = None

    def update_azimuth(self, value):
        layer = self.iface.activeLayer()
        if not layer:
            return
        if not layer.isEditable():
            self.iface.messageBar().pushWarning("Azimuth Editor", "Vrstva musí být v režimu editace.")
            return

        selected = layer.selectedFeatures()
        if not selected:
            self.iface.messageBar().pushWarning("Azimuth Editor", "Vyberte prvek.")
            return

        fid = selected[0].id()
        idx = layer.fields().indexFromName("azimuth")
        if idx == -1:
            self.iface.messageBar().pushWarning("Azimuth Editor", "Atribut 'azimuth' neexistuje.")
            return

        # změna atributu
        layer.changeAttributeValue(fid, idx, value)

        # refresh mapy
        layer.triggerRepaint()

    def decrease_azimuth(self):
        """Sníží hodnotu o 10°"""
        val = self.spin.value() - 10
        if val < 0:
            val = 350
        self.spin.setValue(val)

    def increase_azimuth(self):
        """Zvýší hodnotu o 10°"""
        val = self.spin.value() + 10
        if val > 360:
            val = 0
        self.spin.setValue(val)
