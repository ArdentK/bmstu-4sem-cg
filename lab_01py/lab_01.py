# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\msys64\home\supru\computers_graphics\lab_01py\lab_01.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1093, 707)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.QCanvas = QtWidgets.QGraphicsView(self.centralwidget)
        self.QCanvas.setGeometry(QtCore.QRect(230, 10, 841, 641))
        self.QCanvas.setObjectName("QCanvas")
        self.btn_add_point = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_point.setGeometry(QtCore.QRect(60, 130, 111, 23))
        self.btn_add_point.setObjectName("btn_add_point")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setEnabled(True)
        self.listWidget.setGeometry(QtCore.QRect(20, 231, 191, 121))
        self.listWidget.setObjectName("listWidget")
        self.btn_edit_point = QtWidgets.QPushButton(self.centralwidget)
        self.btn_edit_point.setGeometry(QtCore.QRect(60, 150, 111, 23))
        self.btn_edit_point.setObjectName("btn_edit_point")
        self.btn_del_point = QtWidgets.QPushButton(self.centralwidget)
        self.btn_del_point.setGeometry(QtCore.QRect(60, 170, 111, 23))
        self.btn_del_point.setObjectName("btn_del_point")
        self.btn_task = QtWidgets.QPushButton(self.centralwidget)
        self.btn_task.setGeometry(QtCore.QRect(60, 390, 101, 23))
        self.btn_task.setObjectName("btn_task")
        self.btn_run_app = QtWidgets.QPushButton(self.centralwidget)
        self.btn_run_app.setGeometry(QtCore.QRect(60, 360, 101, 23))
        self.btn_run_app.setObjectName("btn_run_app")
        self.text_answer = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_answer.setGeometry(QtCore.QRect(20, 440, 191, 211))
        self.text_answer.setObjectName("text_answer")
        self.lbl_answer = QtWidgets.QLabel(self.centralwidget)
        self.lbl_answer.setGeometry(QtCore.QRect(90, 420, 47, 13))
        self.lbl_answer.setObjectName("lbl_answer")
        self.btn_del_all = QtWidgets.QPushButton(self.centralwidget)
        self.btn_del_all.setGeometry(QtCore.QRect(60, 200, 111, 23))
        self.btn_del_all.setObjectName("btn_del_all")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 10, 191, 71))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 80, 31, 16))
        self.label.setObjectName("label")
        self.coordinate = QtWidgets.QLineEdit(self.centralwidget)
        self.coordinate.setGeometry(QtCore.QRect(40, 100, 151, 20))
        self.coordinate.setObjectName("coordinate")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1093, 21))
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
        self.btn_add_point.setText(_translate("MainWindow", "Добавить"))
        self.btn_edit_point.setText(_translate("MainWindow", "Редактировать"))
        self.btn_del_point.setText(_translate("MainWindow", "Удалить"))
        self.btn_task.setText(_translate("MainWindow", "Справка"))
        self.btn_run_app.setText(_translate("MainWindow", "Запустить"))
        self.lbl_answer.setText(_translate("MainWindow", "Ответ"))
        self.btn_del_all.setText(_translate("MainWindow", "Удалить все"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Введите кооддинаты точки через запятую.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Пример:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                        5.789, -9</p></body></html>"))
        self.label.setText(_translate("MainWindow", "x, y"))
