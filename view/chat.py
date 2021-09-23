# -*- coding: utf-8 -*-
import sys
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QListWidgetItem

from client import Client
from model.account import Account, generate_uid
from model.message import Message
import datetime
from model.protocol import Protocol
from view.auth import check_auth, Ui_Auth_MainWindow, get_account


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("chat.ui")
        self.ui.show()
        self.account = None
        self.auth_ui = None
        self.load_account()

        self.ui.pushButton_send.clicked.connect(self.on_click_send)
        self.ui.pushButton_reconnect.clicked.connect(self.on_click_reconnect)

        self.client = Client(self)
        self.client.init()

        QtCore.QMetaObject.connectSlotsByName(self)

    def load_account(self):
        try:
            self.account = get_account()
        except FileNotFoundError:
            self.auth_ui = Ui_Auth_MainWindow(self)
            self.ui.hide()
        self.ui.label_account.setText(str(self.account))


    def on_click_send(self):
        text = self.ui.lineEdit_text.text()
        msg = Message(text, sender=self.account)
        protocol = Protocol(Protocol.LIST, [msg])

        self.client.send_message(protocol)
        self.on_message(msg, True)

    def on_click_reconnect(self):
        self.client.connect()

    def on_connected(self):
        self.ui.label_state.setText("Подключен")
        self.ui.pushButton_send.setEnabled(True)
        protocol = Protocol(Protocol.ON_CONNECT, [Message("Я подключился!", self.account.name)])
        self.client.send_message(protocol)
        self.ui.pushButton_send.setStyleSheet("background-color: #1976D2; border-radius: 5px; color: white;")

    def on_message(self, message: Message, is_owner=False):
        print("Пришло сообщение!", message)
        print(message)
        if is_owner:
            message.sender.name = "Вы!"

        self.ui.listWidget.addItem(
            f"Отправитель: {message.sender} \nВремя: {datetime.datetime.fromtimestamp(message.date)} \nСообщение: {message.text}")

    def on_failed(self, error):
        print(error)
        self.ui.label_state.setText("Не подключён")
        self.ui.pushButton_send.setEnabled(False)
        self.ui.pushButton_send.setStyleSheet("background-color: #fff")

    def on_disconnect(self):
        disconnect_message = Protocol(Protocol.DISCONNECT, Message("Я отключился", self.account))
        self.client.send_message(disconnect_message)
        self.client = None

    def on_auth(self):
        self.ui.show()
        # Подгружаем аккаунт при авторизации
        self.load_account()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    sys.exit(app.exec_())
