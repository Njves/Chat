from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
import json
from os import path
from model.account import Account, generate_uid, from_json


class AuthWriter:
    AUTH_FILE = "auth.json"
    def __init__(self):
        self.name = ""
        self.email = ""

    def set_name(self, name):
        self.name = name

    def set_email(self, email):
        self.email = email

    def write_data(self):
        account = Account(generate_uid(), self.name, self.email)
        with open(self.AUTH_FILE, "w") as file:
            file.write(account.to_json())


def check_auth():
    return path.exists("auth.json")


def get_account():
    with open("auth.json", "r") as file:
        return from_json(file.read())


class Ui_Auth_MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.auth_writer = AuthWriter()
        self.ui = uic.loadUi("auth.ui")
        self.ui.pushButton_submit.clicked.connect(self.submit)
        self.ui.label_notify.setStyleSheet("color: red;")
        self.ui.show()

    def submit(self):
        name = self.ui.lineEdit_name.text()
        email = self.ui.lineEdit_email.text()
        if not name:
            self.ui.label_notify.setText("Заполните поле имени!")
            return
        if not email:
            self.ui.label_notify.setText("Заполните поле почты!")
            return
        self.ui.label_notify.setText("")
        self.auth_writer.set_name(name)
        self.auth_writer.set_email(email)
        self.auth_writer.write_data()
        self.parent.on_auth()
        self.ui.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Auth_MainWindow(None)
    sys.exit(app.exec_())
