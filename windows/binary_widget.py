# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'binary_widget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Binary_Method(object):
    def setupUi(self, Binary_Method):
        Binary_Method.setObjectName("Binary_Method")
        Binary_Method.resize(555, 420)
        self.label = QtWidgets.QLabel(Binary_Method)
        self.label.setGeometry(QtCore.QRect(20, 10, 491, 20))
        self.label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Binary_Method)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 40, 491, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setMouseTracking(False)
        self.label_2.setAcceptDrops(False)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.binary_source_lineedit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.binary_source_lineedit.setObjectName("binary_source_lineedit")
        self.horizontalLayout.addWidget(self.binary_source_lineedit)
        self.binary_source_browse = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.binary_source_browse.setObjectName("binary_source_browse")
        self.horizontalLayout.addWidget(self.binary_source_browse)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Binary_Method)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 80, 491, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.binary_anc_lineedit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.binary_anc_lineedit.setObjectName("binary_anc_lineedit")
        self.horizontalLayout_2.addWidget(self.binary_anc_lineedit)
        self.binary_anc_browse = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.binary_anc_browse.setObjectName("binary_anc_browse")
        self.horizontalLayout_2.addWidget(self.binary_anc_browse)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Binary_Method)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(20, 120, 491, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.binary_exclude_field = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.binary_exclude_field.setText("")
        self.binary_exclude_field.setObjectName("binary_exclude_field")
        self.horizontalLayout_3.addWidget(self.binary_exclude_field)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(Binary_Method)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(20, 160, 491, 41))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.binary_exclude_vals = QtWidgets.QLineEdit(self.horizontalLayoutWidget_4)
        self.binary_exclude_vals.setObjectName("binary_exclude_vals")
        self.horizontalLayout_5.addWidget(self.binary_exclude_vals)
        self.frame = QtWidgets.QFrame(Binary_Method)
        self.frame.setGeometry(QtCore.QRect(10, 30, 511, 301))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(10, 250, 491, 41))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.binary_save_lineedit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_5)
        self.binary_save_lineedit.setObjectName("binary_save_lineedit")
        self.horizontalLayout_6.addWidget(self.binary_save_lineedit)
        self.binary_save_browse = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        self.binary_save_browse.setObjectName("binary_save_browse")
        self.horizontalLayout_6.addWidget(self.binary_save_browse)
        self.horizontalLayoutWidget_7 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_7.setGeometry(QtCore.QRect(10, 210, 491, 41))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.binary_output_suffix = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        self.binary_output_suffix.setObjectName("binary_output_suffix")
        self.horizontalLayout_8.addWidget(self.binary_output_suffix)
        self.horizontalLayoutWidget_8 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_8.setGeometry(QtCore.QRect(10, 170, 491, 41))
        self.horizontalLayoutWidget_8.setObjectName("horizontalLayoutWidget_8")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_8)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_9 = QtWidgets.QLabel(self.horizontalLayoutWidget_8)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_9.addWidget(self.label_9)
        self.binary_intp_fields = QtWidgets.QLineEdit(self.horizontalLayoutWidget_8)
        self.binary_intp_fields.setObjectName("binary_intp_fields")
        self.horizontalLayout_9.addWidget(self.binary_intp_fields)
        self.horizontalLayoutWidget_6 = QtWidgets.QWidget(Binary_Method)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(10, 340, 511, 41))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.binary_progressBar = QtWidgets.QProgressBar(self.horizontalLayoutWidget_6)
        self.binary_progressBar.setProperty("value", 0)
        self.binary_progressBar.setObjectName("binary_progressBar")
        self.horizontalLayout_7.addWidget(self.binary_progressBar)
        self.binary_run_prog = QtWidgets.QPushButton(self.horizontalLayoutWidget_6)
        self.binary_run_prog.setObjectName("binary_run_prog")
        self.horizontalLayout_7.addWidget(self.binary_run_prog)
        self.binary_cancel_prog = QtWidgets.QPushButton(self.horizontalLayoutWidget_6)
        self.binary_cancel_prog.setObjectName("binary_cancel_prog")
        self.horizontalLayout_7.addWidget(self.binary_cancel_prog)
        self.frame.raise_()
        self.label.raise_()
        self.horizontalLayoutWidget.raise_()
        self.horizontalLayoutWidget_2.raise_()
        self.horizontalLayoutWidget_3.raise_()
        self.horizontalLayoutWidget_4.raise_()
        self.horizontalLayoutWidget_6.raise_()

        self.retranslateUi(Binary_Method)
        QtCore.QMetaObject.connectSlotsByName(Binary_Method)
        Binary_Method.setTabOrder(self.binary_source_lineedit, self.binary_source_browse)
        Binary_Method.setTabOrder(self.binary_source_browse, self.binary_anc_lineedit)
        Binary_Method.setTabOrder(self.binary_anc_lineedit, self.binary_anc_browse)
        Binary_Method.setTabOrder(self.binary_anc_browse, self.binary_exclude_field)
        Binary_Method.setTabOrder(self.binary_exclude_field, self.binary_exclude_vals)
        Binary_Method.setTabOrder(self.binary_exclude_vals, self.binary_intp_fields)
        Binary_Method.setTabOrder(self.binary_intp_fields, self.binary_output_suffix)
        Binary_Method.setTabOrder(self.binary_output_suffix, self.binary_save_lineedit)
        Binary_Method.setTabOrder(self.binary_save_lineedit, self.binary_save_browse)
        Binary_Method.setTabOrder(self.binary_save_browse, self.binary_run_prog)
        Binary_Method.setTabOrder(self.binary_run_prog, self.binary_cancel_prog)

    def retranslateUi(self, Binary_Method):
        _translate = QtCore.QCoreApplication.translate
        Binary_Method.setWindowTitle(_translate("Binary_Method", "Form"))
        self.label.setText(_translate("Binary_Method", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Binary Method</span></p></body></html>"))
        self.label_2.setText(_translate("Binary_Method", "Source Shapefile:"))
        self.binary_source_lineedit.setPlaceholderText(_translate("Binary_Method", "filepath and name of the source shapefile"))
        self.binary_source_browse.setText(_translate("Binary_Method", "Browse"))
        self.label_3.setText(_translate("Binary_Method", "Ancillary Shapefile:"))
        self.binary_anc_lineedit.setPlaceholderText(_translate("Binary_Method", "filepath and name of the ancillary shapefile"))
        self.binary_anc_browse.setText(_translate("Binary_Method", "Browse"))
        self.label_4.setText(_translate("Binary_Method", "Exclusion Field:"))
        self.binary_exclude_field.setPlaceholderText(_translate("Binary_Method", "Name of field containing values to exclude"))
        self.label_6.setText(_translate("Binary_Method", "Exclusion Value(s):"))
        self.binary_exclude_vals.setPlaceholderText(_translate("Binary_Method", "values to exclude, space separated ex: 1 12 3 45"))
        self.label_7.setText(_translate("Binary_Method", "Save as:"))
        self.binary_save_lineedit.setPlaceholderText(_translate("Binary_Method", "filepath and name of output shapefile"))
        self.binary_save_browse.setText(_translate("Binary_Method", "Browse"))
        self.label_8.setText(_translate("Binary_Method", "Output Field Suffix:"))
        self.binary_output_suffix.setPlaceholderText(_translate("Binary_Method", "ex: _intp (population would become population_intp)"))
        self.label_9.setText(_translate("Binary_Method", "Interpolation Field(s):"))
        self.binary_intp_fields.setPlaceholderText(_translate("Binary_Method", "Name(s) of field(s) to interpolated, space separated"))
        self.binary_run_prog.setText(_translate("Binary_Method", "Run"))
        self.binary_cancel_prog.setText(_translate("Binary_Method", "Cancel"))

