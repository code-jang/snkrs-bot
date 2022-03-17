import sys
import json
from collections import OrderedDict
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from nike import Ui_MainWindow
import account

class AccountWindow(QDialog):
    def __init__(self, mode, row):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.account_ui = account.Ui_Dialog()
        self.account_ui.setupUi(self)
        
        if mode == 'edit':
            with open('./account_data.json', 'r', encoding="utf-8") as fp:
                account_data = json.load(fp)

            self.account_ui.account_name.setText(account_data[row]["name"])
            self.account_ui.account_id.setText(account_data[row]["id"])
            self.account_ui.account_password.setText(account_data[row]["password"])
            self.account_ui.confirm_btn.setText("수정")
            

        self.account_ui.confirm_btn.clicked.connect(lambda: self.create_account(mode, row))
        self.account_ui.cancel_btn.clicked.connect(self.close)

        self.show()



    def create_account(self, mode, row):
        name = self.account_ui.account_name.text()
        id = self.account_ui.account_id.text()
        password = self.account_ui.account_password.text()

        if mode == 'create':
            account_info = dict()
            account_info["name"] = name
            account_info["id"] = id
            account_info["password"] = password

            try:
                with open('./account_data.json', 'r', encoding="utf-8") as fp:
                    account_data = json.load(fp)
                    account_data.append(account_info)

                with open('./account_data.json', 'w', encoding="utf-8") as fp:
                    json.dump(account_data, fp, indent='\t')

            except FileNotFoundError:
                with open('./account_data.json', 'w', encoding="utf-8") as fp:
                    Accounts = list()
                    Accounts.append(account_info)
                    json.dump(Accounts, fp, indent='\t')

            self.close()
        else:
            with open('./account_data.json', 'r', encoding="utf-8") as fp:
                    account_data = json.load(fp)
                    account_data[row]["name"] = name
                    account_data[row]["id"] = id
                    account_data[row]["password"] = password

            with open('./account_data.json', 'w', encoding="utf-8") as fp:
                    json.dump(account_data, fp, indent='\t')
                    
            self.close()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.show_center()
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)

        self.menu_btn_dic = {'home_btn':'home_page', 'account_btn':'account_page', 'settings_btn':'settings_page'}
        self.used_btn = 'home_btn'

        QSizeGrip(self.main_ui.window_size_grip)
        self.main_ui.close_btn.clicked.connect(lambda: self.close())
        self.main_ui.size_btn.clicked.connect(self.change_window_size)
        self.main_ui.restore_btn.clicked.connect(lambda: self.showMinimized())
        self.main_ui.header.mouseMoveEvent = self.move_window
        self.main_ui.menu_btn.clicked.connect(lambda: self.slide_menu(self.main_ui))
        self.main_ui.home_btn.clicked.connect(lambda: self.change_page('home_btn'))
        self.main_ui.account_btn.clicked.connect(lambda: self.change_page('account_btn'))
        self.main_ui.settings_btn.clicked.connect(lambda: self.change_page('settings_btn'))

        account_table = self.main_ui.account_table
        account_table.verticalHeader().setVisible(False)
        account_table.setColumnWidth(0, int(self.width()*1/20))
        account_table.setColumnWidth(1, int(self.width()*3/20))
        account_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        account_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        
        self.show_account_table()
        self.main_ui.account_create_btn.clicked.connect(self.create_account_window)
        self.main_ui.account_delete_btn.clicked.connect(self.delete_account)
        self.main_ui.account_edit_btn.clicked.connect(self.edit_account)
        self.main_ui.account_table.clicked.connect(self.active_account_btns)
        
        




    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()


    def move_window(self, event):
        if self.isMaximized() == False:
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()


    def show_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def change_window_size(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()


    def show_account_table(self):
        self.main_ui.account_edit_btn.setEnabled(False)
        self.main_ui.account_delete_btn.setEnabled(False)

        try:
            with open('./account_data.json', 'r', encoding="utf-8") as fp:
                account_data = json.load(fp)
                rows = len(account_data)

            table = self.main_ui.account_table
            table.setRowCount(rows)
            
            for row in range(rows):
                account_info_list = list(account_data[row].values())
                account_info_list.insert(0, str(row + 1))

                for column in range(table.columnCount()):
                    table.setItem(row, column, QTableWidgetItem(account_info_list[column]))
                    table.item(row, column).setTextAlignment(Qt.AlignCenter)
            
            self.set_rows_height()

        except FileNotFoundError:
            print('hi')
    
    def set_rows_height(self):
        table = self.main_ui.account_table
        for row in range(table.rowCount()):
            table.setRowHeight(row, int(self.width()*7/100))
            
        
    def slide_menu(self, main_ui):
        width = self.main_ui.side_bar.width()

        if width == 55:
            new_width = 150
        else:
            new_width = 55

        self.animation = QPropertyAnimation(main_ui.side_bar, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.start()

    def change_page(self, change_btn):
        if change_btn != self.used_btn:
            if self.menu_btn_dic.get(change_btn):
                used_btn_style = eval(f'self.main_ui.{self.used_btn}.styleSheet()')
                style_list = used_btn_style.split('}')                
                del style_list[len(style_list) - 2:]
                used_btn_style = "}".join(style_list) + "}"
                eval(f'self.main_ui.{self.used_btn}.setStyleSheet(used_btn_style)')

                #change btn
                
                current_btn_style = eval(f'self.main_ui.{change_btn}.styleSheet()')
                clicked_btn_style = current_btn_style + 'QPushButton{background-color: rgb(33, 37, 43);border-left: 15px solid rgb(33, 37, 43);}'
                eval(f'self.main_ui.{change_btn}.setStyleSheet(clicked_btn_style)')
                self.main_ui.stackedWidget.setCurrentWidget(eval(f'self.main_ui.{self.menu_btn_dic[change_btn]}'))
                self.used_btn = change_btn

    def active_account_btns(self):
        self.main_ui.account_delete_btn.setEnabled(True)
        self.main_ui.account_edit_btn.setEnabled(True)
        

    
    def disable_account_btns(self):
        self.main_ui.account_delete_btn.setEnabled(False)
        self.main_ui.account_edit_btn.setEnabled(False)


    def create_account_window(self):
        account_window = AccountWindow('create', 0)
        account_window.exec_()
        self.show_account_table()


    def delete_account(self):
        row = self.main_ui.account_table.currentRow()
        with open('./account_data.json', 'r', encoding="utf-8") as fp:
            account_data = json.load(fp)
            del account_data[row]
        
        with open('./account_data.json', 'w', encoding="utf-8") as fp:
            json.dump(account_data, fp, indent='\t')

        self.main_ui.account_table.removeRow(row)
        

    def edit_account(self):
        row = self.main_ui.account_table.currentRow()
        account_window = AccountWindow('edit', row)
        account_window.exec_()
        self.show_account_table()


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())