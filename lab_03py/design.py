# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\msys64\home\supru\computers_graphics\lab_03py\design.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1082, 609)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 90, 301, 143))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.QDSB_y_start = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.QDSB_y_start.setMinimum(-2000.0)
        self.QDSB_y_start.setMaximum(2000.0)
        self.QDSB_y_start.setObjectName("QDSB_y_start")
        self.gridLayout_2.addWidget(self.QDSB_y_start, 4, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 6, 2, 1, 1)
        self.QDSB_y_end = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.QDSB_y_end.setMinimum(-2000.0)
        self.QDSB_y_end.setMaximum(2000.0)
        self.QDSB_y_end.setObjectName("QDSB_y_end")
        self.gridLayout_2.addWidget(self.QDSB_y_end, 6, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 6, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 4, 2, 1, 1)
        self.QDSB_x_end = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.QDSB_x_end.setMinimum(-2000.0)
        self.QDSB_x_end.setMaximum(2000.0)
        self.QDSB_x_end.setObjectName("QDSB_x_end")
        self.gridLayout_2.addWidget(self.QDSB_x_end, 6, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 4, 0, 1, 1)
        self.QDSB_x_start = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.QDSB_x_start.setMinimum(-2000.0)
        self.QDSB_x_start.setMaximum(2000.0)
        self.QDSB_x_start.setObjectName("QDSB_x_start")
        self.gridLayout_2.addWidget(self.QDSB_x_start, 4, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 3, 1, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 5, 1, 1, 2)
        self.btn_to_draw_line = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btn_to_draw_line.setObjectName("btn_to_draw_line")
        self.gridLayout_2.addWidget(self.btn_to_draw_line, 10, 0, 1, 4)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(19, 250, 301, 121))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.QDSB_angle_step = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.QDSB_angle_step.setMinimum(-200.0)
        self.QDSB_angle_step.setMaximum(200.0)
        self.QDSB_angle_step.setObjectName("QDSB_angle_step")
        self.gridLayout_3.addWidget(self.QDSB_angle_step, 3, 3, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 3, 2, 1, 1)
        self.btn_to_draw_spectrum = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.btn_to_draw_spectrum.setObjectName("btn_to_draw_spectrum")
        self.gridLayout_3.addWidget(self.btn_to_draw_spectrum, 6, 0, 1, 4)
        self.QDSB_radius = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.QDSB_radius.setMinimum(0.0)
        self.QDSB_radius.setMaximum(1000.0)
        self.QDSB_radius.setObjectName("QDSB_radius")
        self.gridLayout_3.addWidget(self.QDSB_radius, 3, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 3, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 1, 1, 1, 2)
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 2, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 0, 1, 1, 2)
        self.QDSB_x_spectrum = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.QDSB_x_spectrum.setMinimum(-2000.0)
        self.QDSB_x_spectrum.setMaximum(2000.0)
        self.QDSB_x_spectrum.setObjectName("QDSB_x_spectrum")
        self.gridLayout_3.addWidget(self.QDSB_x_spectrum, 2, 1, 1, 1)
        self.QDSB_y_spectrum = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.QDSB_y_spectrum.setMinimum(-2000.0)
        self.QDSB_y_spectrum.setMaximum(2000.0)
        self.QDSB_y_spectrum.setObjectName("QDSB_y_spectrum")
        self.gridLayout_3.addWidget(self.QDSB_y_spectrum, 2, 3, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 2, 0, 1, 1)
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(20, 390, 301, 31))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_18 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.gridLayout_4.addWidget(self.label_18, 0, 0, 1, 1)
        self.btn_to_output_efficiency = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.btn_to_output_efficiency.setObjectName("btn_to_output_efficiency")
        self.gridLayout_4.addWidget(self.btn_to_output_efficiency, 0, 1, 1, 1)
        self.gridLayoutWidget_5 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(20, 440, 301, 51))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_19 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.gridLayout_5.addWidget(self.label_19, 0, 0, 1, 2)
        self.btn_to_output_gradation = QtWidgets.QPushButton(self.gridLayoutWidget_5)
        self.btn_to_output_gradation.setObjectName("btn_to_output_gradation")
        self.gridLayout_5.addWidget(self.btn_to_output_gradation, 1, 0, 1, 2)
        self.gridLayoutWidget_6 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_6.setGeometry(QtCore.QRect(90, 510, 151, 31))
        self.gridLayoutWidget_6.setObjectName("gridLayoutWidget_6")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.btn_to_clear = QtWidgets.QPushButton(self.gridLayoutWidget_6)
        self.btn_to_clear.setObjectName("btn_to_clear")
        self.gridLayout_6.addWidget(self.btn_to_clear, 0, 0, 1, 1)
        self.gridLayoutWidget_7 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_7.setGeometry(QtCore.QRect(20, 20, 301, 51))
        self.gridLayoutWidget_7.setObjectName("gridLayoutWidget_7")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.gridLayoutWidget_7)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget_7)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_7.addWidget(self.label_8, 0, 0, 1, 1)
        self.QCBox_method = QtWidgets.QComboBox(self.gridLayoutWidget_7)
        self.QCBox_method.setObjectName("QCBox_method")
        self.QCBox_method.addItem("")
        self.QCBox_method.addItem("")
        self.QCBox_method.addItem("")
        self.QCBox_method.addItem("")
        self.QCBox_method.addItem("")
        self.QCBox_method.addItem("")
        self.gridLayout_7.addWidget(self.QCBox_method, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget_7)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_7.addWidget(self.label_9, 1, 0, 1, 1)
        self.QCBox_color = QtWidgets.QComboBox(self.gridLayoutWidget_7)
        self.QCBox_color.setObjectName("QCBox_color")
        self.QCBox_color.addItem("")
        self.QCBox_color.addItem("")
        self.QCBox_color.addItem("")
        self.QCBox_color.addItem("")
        self.gridLayout_7.addWidget(self.QCBox_color, 1, 1, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(340, 10, 731, 541))
        self.graphicsView.setObjectName("graphicsView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1082, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_5.setText(_translate("MainWindow", "                Y:"))
        self.label_3.setText(_translate("MainWindow", "                X:"))
        self.label.setText(_translate("MainWindow", "Координаты отрезка"))
        self.label_4.setText(_translate("MainWindow", "                Y:"))
        self.label_2.setText(_translate("MainWindow", "                X:"))
        self.label_6.setText(_translate("MainWindow", "Координаты начала"))
        self.label_7.setText(_translate("MainWindow", "Координаты конца"))
        self.btn_to_draw_line.setText(_translate("MainWindow", "ПОСТРОИТЬ ОТРЕЗОК"))
        self.label_15.setText(_translate("MainWindow", "   Шаг угла"))
        self.btn_to_draw_spectrum.setText(_translate("MainWindow", "ПОСТРОИТЬ СПЕКТР"))
        self.label_14.setText(_translate("MainWindow", "     Радиус"))
        self.label_11.setText(_translate("MainWindow", "            Центр"))
        self.label_13.setText(_translate("MainWindow", "                Y:"))
        self.label_10.setText(_translate("MainWindow", "Параментры спектра"))
        self.label_12.setText(_translate("MainWindow", "                X:"))
        self.label_18.setText(_translate("MainWindow", "Результаты эффективности"))
        self.btn_to_output_efficiency.setText(_translate("MainWindow", "ВЫВЕСТИ"))
        self.label_19.setText(_translate("MainWindow", "Исследование ступенчатости отрезка"))
        self.btn_to_output_gradation.setText(_translate("MainWindow", "ВЫВЕСТИ"))
        self.btn_to_clear.setText(_translate("MainWindow", "ОЧИСТИТЬ"))
        self.label_8.setText(_translate("MainWindow", "     Метод"))
        self.QCBox_method.setItemText(0, _translate("MainWindow", "ЦДА"))
        self.QCBox_method.setItemText(1, _translate("MainWindow", "Алгоритм Брезенхема (float)"))
        self.QCBox_method.setItemText(2, _translate("MainWindow", "Алгоритм Брезенхем (int)"))
        self.QCBox_method.setItemText(3, _translate("MainWindow", "Алгоритм Брезенхема с устранением ступенчатости"))
        self.QCBox_method.setItemText(4, _translate("MainWindow", "Алгоритм Ву"))
        self.QCBox_method.setItemText(5, _translate("MainWindow", "Библиотечный алгоритм"))
        self.label_9.setText(_translate("MainWindow", "     Цвет"))
        self.QCBox_color.setItemText(0, _translate("MainWindow", "Белый (фон)"))
        self.QCBox_color.setItemText(1, _translate("MainWindow", "Черный"))
        self.QCBox_color.setItemText(2, _translate("MainWindow", "Красный"))
        self.QCBox_color.setItemText(3, _translate("MainWindow", "Синий"))
