# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spatial_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_sp_int_tbox(object):
    def setupUi(self, sp_int_tbox):
        sp_int_tbox.setObjectName("sp_int_tbox")
        sp_int_tbox.resize(488, 272)
        self.centralwidget = QtWidgets.QWidget(sp_int_tbox)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(0, 29))
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.boxSelectmethod = QtWidgets.QComboBox(self.centralwidget)
        self.boxSelectmethod.setObjectName("boxSelectmethod")
        self.boxSelectmethod.addItem("")
        self.boxSelectmethod.addItem("")
        self.boxSelectmethod.addItem("")
        self.boxSelectmethod.addItem("")
        self.boxSelectmethod.addItem("")
        self.boxSelectmethod.addItem("")
        self.verticalLayout.addWidget(self.boxSelectmethod)
        self.buttonOpenmethod = QtWidgets.QPushButton(self.centralwidget)
        self.buttonOpenmethod.setObjectName("buttonOpenmethod")
        self.verticalLayout.addWidget(self.buttonOpenmethod)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.label_3.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        sp_int_tbox.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(sp_int_tbox)
        self.statusbar.setObjectName("statusbar")
        sp_int_tbox.setStatusBar(self.statusbar)

        self.retranslateUi(sp_int_tbox)
        QtCore.QMetaObject.connectSlotsByName(sp_int_tbox)

    def retranslateUi(self, sp_int_tbox):
        _translate = QtCore.QCoreApplication.translate
        sp_int_tbox.setWindowTitle(_translate("sp_int_tbox", "MainWindow"))
        self.label.setText(_translate("sp_int_tbox", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">The Spatial Interpolation Toolbox</span></p></body></html>"))
        self.label_2.setText(_translate("sp_int_tbox", "Select Interpolation Method:"))
        self.boxSelectmethod.setItemText(0, _translate("sp_int_tbox", "Areal Weighting"))
        self.boxSelectmethod.setItemText(1, _translate("sp_int_tbox", "Binary Method"))
        self.boxSelectmethod.setItemText(2, _translate("sp_int_tbox", "Limiting Variable"))
        self.boxSelectmethod.setItemText(3, _translate("sp_int_tbox", "N-Class"))
        self.boxSelectmethod.setItemText(4, _translate("sp_int_tbox", "Parcel Method"))
        self.boxSelectmethod.setItemText(5, _translate("sp_int_tbox", "Expert System"))
        self.buttonOpenmethod.setText(_translate("sp_int_tbox", "Open"))
        self.label_3.setText(_translate("sp_int_tbox", "<html><head/><body><p><a href=\"https://github.com/mikeRobWard/spatial-interpolation-toolbox\"><span style=\" text-decoration: underline; color:#0000ff;\">Documentation</span></a></p></body></html>"))

