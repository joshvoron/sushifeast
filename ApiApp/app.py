from PyQt5 import QtCore, QtGui, QtWidgets
import requests


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()

        self.setupUi(MainWindow)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_orders)
        self.timer.start(30000)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(40)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(820, 600))
        MainWindow.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        MainWindow.setAcceptDrops(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)

        self.centralwidget = QtWidgets.QScrollArea(MainWindow)
        self.centralwidget.setWidgetResizable(True)
        self.scroll_content = QtWidgets.QWidget()
        self.centralwidget.setWidget(self.scroll_content)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scroll_content)
        self.verticalLayout.setObjectName("verticalLayout")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 21))
        self.menubar.setObjectName("menubar")

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.login = QtWidgets.QAction(MainWindow)
        self.login.setObjectName("login")

        self.logout = QtWidgets.QAction(MainWindow)
        self.logout.setObjectName("logout")

        self.menu.addAction(self.login)
        self.menu.addAction(self.logout)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        try:
            orders = get_order()
            if orders != []:
                for order in orders:

                    item_list = order.get('items', [])
                    user = f"{order.get('user_first_name', '')} {order.get('user_last_name', '')}"

                    order_widget = QtWidgets.QWidget(self.scroll_content)
                    order_widget.setEnabled(True)
                    order_layout = QtWidgets.QFormLayout(order_widget)
                    order_layout.setHorizontalSpacing(0)
                    order_layout.setVerticalSpacing(6)

                    order_list = QtWidgets.QListWidget(order_widget)
                    order_list.setMinimumSize(QtCore.QSize(0, 160))
                    order_list.setMaximumSize(QtCore.QSize(16777215, 16777215))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    order_list.setFont(font)
                    order_list.setMouseTracking(False)
                    order_list.setAcceptDrops(False)

                    end_order = QtWidgets.QPushButton(order_widget)
                    end_order.setMinimumSize(QtCore.QSize(40, 40))
                    font = QtGui.QFont()
                    font.setFamily(
                        "Lucida Sans,Lucida Sans Regular,Lucida Grande,Lucida Sans Unicode,Geneva,Verdana,sans-serif")
                    end_order.setFont(font)
                    end_order.setStyleSheet(
                        "border-radius: 2rem; background-color: green;font-family: \'Lucida Sans\', \'Lucida Sans Regular\', \'Lucida Grande\', \'Lucida Sans Unicode\', Geneva, Verdana, sans-serif;color: white;font-size:30rem;")
                    end_order.setObjectName("end_order")

                    order_title = QtWidgets.QLabel(order_widget)
                    font = QtGui.QFont()
                    font.setPointSize(20)
                    font.setBold(False)
                    font.setWeight(50)
                    order_title.setFont(font)
                    order_title.setStyleSheet("color:brown;")
                    order_title.setMinimumSize(QtCore.QSize(800, 33))
                    order_num = order.get('order')
                    order_title.setText(f"Заказ №{str(order_num)}")
                    order_title.setObjectName("order_title")

                    order_user = QtWidgets.QLabel(order_widget)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    order_user.setFont(font)
                    order_user.setText(f'Заказчик: {user}')
                    order_user.setObjectName("order_user")

                    order_address = QtWidgets.QLabel(order_widget)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    order_address.setFont(font)
                    order_address.setText(f"Адрес: {order.get('user_address', '')}")
                    order_address.setObjectName("order_address")

                    end_order.setStatusTip(_translate("MainWindow", "Далее заказ отправится в доставку"))
                    end_order.setText(_translate("MainWindow", "Завершить заказ"))

                    end_order.clicked.connect(
                        lambda _, order_num=order.get('order', ''): self.complete_order(order_num))

                    order_layout.addRow(order_title)
                    order_layout.addRow(order_user)
                    order_layout.addRow(order_address)
                    order_layout.addRow(order_list)
                    order_layout.addRow(end_order)

                    self.verticalLayout.addWidget(order_widget)

                    for item in item_list:
                        items = item.get('item_list', '')
                        order_list.addItem(items)
            elif orders == []:
                order_widget = QtWidgets.QWidget(self.scroll_content)
                order_widget.setEnabled(True)
                order_widget.setMinimumSize(QtCore.QSize(600, 160))

                order_title = QtWidgets.QLabel(order_widget)
                font = QtGui.QFont()
                font.setPointSize(30)
                font.setBold(False)
                font.setWeight(50)
                order_title.setFont(font)
                order_title.setStyleSheet("color:brown;")
                order_title.setMinimumSize(QtCore.QSize(800, 33))
                order_title.setText(f"--Заказов нет--")
                order_title.setObjectName("order_title")

                self.verticalLayout.addWidget(order_widget)
        except requests.exceptions.ConnectionError:
            order_widget = QtWidgets.QWidget(self.scroll_content)
            order_widget.setEnabled(True)
            order_widget.setMinimumSize(QtCore.QSize(600, 160))

            order_title = QtWidgets.QLabel(order_widget)
            font = QtGui.QFont()
            font.setPointSize(30)
            font.setBold(False)
            font.setWeight(50)
            order_title.setFont(font)
            order_title.setStyleSheet("color:brown;")
            order_title.setMinimumSize(QtCore.QSize(800, 33))
            order_title.setText(f"Error: Сервер недоступен ")
            order_title.setObjectName("order_title")
            self.verticalLayout.addWidget(order_widget)

        self.menu.setTitle(_translate("MainWindow", "Аккаунт"))
        self.login.setText(_translate("MainWindow", "Войти "))
        self.login.setStatusTip(_translate("MainWindow", "Войти в аккаунт"))
        self.login.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.logout.setText(_translate("MainWindow", "Выйти"))
        self.logout.setStatusTip(_translate("MainWindow", "Выйти из аккаунта"))
        self.logout.setShortcut(_translate("MainWindow", "Ctrl+O"))

    def complete_order(self, order_num):
        try:
            url = f"http://localhost:8000/basket/{order_num}"
            requests.post(url)
            self.update_orders()
        except Exception as e:
            pass

    def update_orders(self):
        _translate = QtCore.QCoreApplication.translate
        try:
            orders = get_order()
            for i in reversed(range(self.verticalLayout.count())):
                self.verticalLayout.itemAt(i).widget().setParent(None)

            if orders != []:
                for order in orders:

                    item_list = order.get('items', [])
                    user = f"{order.get('user_first_name', '')} {order.get('user_last_name', '')}"

                    order_widget = QtWidgets.QWidget(self.scroll_content)
                    order_widget.setEnabled(True)
                    order_layout = QtWidgets.QFormLayout(order_widget)
                    order_layout.setHorizontalSpacing(0)
                    order_layout.setVerticalSpacing(6)

                    order_list = QtWidgets.QListWidget(order_widget)
                    order_list.setMinimumSize(QtCore.QSize(0, 160))
                    order_list.setMaximumSize(QtCore.QSize(16777215, 16777215))
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    order_list.setFont(font)
                    order_list.setMouseTracking(False)
                    order_list.setAcceptDrops(False)

                    end_order = QtWidgets.QPushButton(order_widget)
                    end_order.setMinimumSize(QtCore.QSize(40, 40))
                    font = QtGui.QFont()
                    font.setFamily(
                        "Lucida Sans,Lucida Sans Regular,Lucida Grande,Lucida Sans Unicode,Geneva,Verdana,sans-serif")
                    end_order.setFont(font)
                    end_order.setStyleSheet(
                        "border-radius: 2rem; background-color: green;font-family: \'Lucida Sans\', \'Lucida Sans Regular\', \'Lucida Grande\', \'Lucida Sans Unicode\', Geneva, Verdana, sans-serif;color: white;font-size:30rem;")
                    end_order.setObjectName("end_order")

                    order_title = QtWidgets.QLabel(order_widget)
                    font = QtGui.QFont()
                    font.setPointSize(20)
                    font.setBold(False)
                    font.setWeight(50)
                    order_title.setFont(font)
                    order_title.setStyleSheet("color:brown;")
                    order_title.setMinimumSize(QtCore.QSize(800, 33))
                    order_title.setText(f"Заказ №{str(order.get('order', ''))}")
                    order_title.setObjectName("order_title")

                    order_user = QtWidgets.QLabel(order_widget)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    order_user.setFont(font)
                    order_user.setText(f'Заказчик: {user}')
                    order_user.setObjectName("order_user")

                    order_address = QtWidgets.QLabel(order_widget)
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    order_address.setFont(font)
                    order_address.setText(f"Адрес: {order.get('user_address', '')}")
                    order_address.setObjectName("order_address")

                    end_order.setStatusTip(_translate("MainWindow", "Далее заказ отправится в доставку"))
                    end_order.setText(_translate("MainWindow", "Завершить заказ"))
                    end_order.clicked.connect(
                        lambda _, order_num=order.get('order', ''): self.complete_order(order_num))

                    order_layout.addRow(order_title)
                    order_layout.addRow(order_user)
                    order_layout.addRow(order_address)
                    order_layout.addRow(order_list)
                    order_layout.addRow(end_order)

                    self.verticalLayout.addWidget(order_widget)

                    for item in item_list:
                        items = item.get('item_list', '')
                        order_list.addItem(items)
            elif orders == []:
                order_widget = QtWidgets.QWidget(self.scroll_content)
                order_widget.setEnabled(True)
                order_widget.setMinimumSize(QtCore.QSize(600, 160))

                order_title = QtWidgets.QLabel(order_widget)
                font = QtGui.QFont()
                font.setPointSize(30)
                font.setBold(False)
                font.setWeight(50)
                order_title.setFont(font)
                order_title.setStyleSheet("color:brown;")
                order_title.setMinimumSize(QtCore.QSize(800, 33))
                order_title.setText(f"--Заказов нет--")
                order_title.setObjectName("order_title")

                self.verticalLayout.addWidget(order_widget)
        except requests.exceptions.ConnectionError:
            order_widget = QtWidgets.QWidget(self.scroll_content)
            order_widget.setEnabled(True)
            order_widget.setMinimumSize(QtCore.QSize(600, 160))

            order_title = QtWidgets.QLabel(order_widget)
            font = QtGui.QFont()
            font.setPointSize(30)
            font.setBold(False)
            font.setWeight(50)
            order_title.setFont(font)
            order_title.setStyleSheet("color:brown;")
            order_title.setMinimumSize(QtCore.QSize(800, 33))
            order_title.setText(f"Error: Сервер недоступен ")
            order_title.setObjectName("order_title")
            self.verticalLayout.addWidget(order_widget)
        self.timer.start(20000)


def get_order():
    url = "http://localhost:8000/basket/"
    response = requests.get(url)
    orders = response.json()
    return orders


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
