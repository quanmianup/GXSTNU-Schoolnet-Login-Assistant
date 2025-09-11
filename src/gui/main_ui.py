# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QSplitter, QStackedWidget, QTableWidget,
    QTableWidgetItem, QTimeEdit, QVBoxLayout, QWidget)
import window_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(614, 524)
        MainWindow.setMinimumSize(QSize(4, 0))
        MainWindow.setTabletTracking(False)
        icon = QIcon()
        icon.addFile(u":/images/images/network.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"")
        MainWindow.setAnimated(False)
        MainWindow.setDocumentMode(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        MainWindow.setProperty(u"frameless", True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setEnabled(True)
        self.widget.setGeometry(QRect(0, 0, 600, 500))
        self.widget.setStyleSheet(u"#widget {\n"
"	background-color: white;\n"
"	border-radius: 10px;\n"
"	box-shadow: 0px 0px 20px 0px rgba(0, 0, 0, 1);\n"
"}")
        self.frame_main = QFrame(self.widget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setGeometry(QRect(0, 40, 600, 460))
        self.frame_main.setStyleSheet(u"QPushButton:hover {\n"
"	padding-bottom: 8px;\n"
"	padding-left:8px;\n"
"}\n"
"QPushButton:pressed{\n"
"	padding-top:3px;\n"
"	padding-right:3px;\n"
"}\n"
"")
        self.frame_main.setFrameShape(QFrame.StyledPanel)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_main)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_tab = QFrame(self.frame_main)
        self.frame_tab.setObjectName(u"frame_tab")
        self.frame_tab.setMinimumSize(QSize(0, 30))
        self.frame_tab.setStyleSheet(u"QFrame#frame_tab {\n"
"    border: none; \n"
"    border-bottom: 1px solid black; \n"
"}\n"
"QFrame#frame_tab QPushButton {\n"
"    border-top-right-radius: 10px; \n"
"    border: 1px solid #ccc; \n"
"    background-color: #f8f8f8; \n"
"	margin-bottom:0;\n"
"}\n"
"QPushButton:hover{\n"
"	padding-bottom:5px;\n"
"}")
        self.frame_tab.setFrameShape(QFrame.StyledPanel)
        self.frame_tab.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_tab)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_tab_main = QPushButton(self.frame_tab)
        self.pushButton_tab_main.setObjectName(u"pushButton_tab_main")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_tab_main.sizePolicy().hasHeightForWidth())
        self.pushButton_tab_main.setSizePolicy(sizePolicy)
        self.pushButton_tab_main.setMinimumSize(QSize(50, 30))
        self.pushButton_tab_main.setStyleSheet(u"margin-left:5px;")

        self.horizontalLayout.addWidget(self.pushButton_tab_main, 0, Qt.AlignBottom)

        self.pushButton_tab_manege = QPushButton(self.frame_tab)
        self.pushButton_tab_manege.setObjectName(u"pushButton_tab_manege")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_tab_manege.sizePolicy().hasHeightForWidth())
        self.pushButton_tab_manege.setSizePolicy(sizePolicy1)
        self.pushButton_tab_manege.setMinimumSize(QSize(130, 30))
        self.pushButton_tab_manege.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.pushButton_tab_manege, 0, Qt.AlignBottom)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.frame_tab)

        self.stackedWidget_tab = QStackedWidget(self.frame_main)
        self.stackedWidget_tab.setObjectName(u"stackedWidget_tab")
        self.page_main = QWidget()
        self.page_main.setObjectName(u"page_main")
        self.frame = QFrame(self.page_main)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(130, 50, 340, 310))
        self.frame.setStyleSheet(u"*{\n"
"	font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton{\n"
"    border: 1px solid #dcdcdc;\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QLineEdit {\n"
"	background-color: rgb(255, 255, 255);\n"
"    border: 1px solid #dcdcdc;\n"
"\n"
"}\n"
"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.widget1 = QWidget(self.frame)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(0, 0, 342, 325))
        self.verticalLayout_5 = QVBoxLayout(self.widget1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_username = QLineEdit(self.widget1)
        self.lineEdit_username.setObjectName(u"lineEdit_username")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit_username.sizePolicy().hasHeightForWidth())
        self.lineEdit_username.setSizePolicy(sizePolicy2)
        self.lineEdit_username.setMinimumSize(QSize(340, 50))
        self.lineEdit_username.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_5.addWidget(self.lineEdit_username)

        self.lineEdit_password = QLineEdit(self.widget1)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setMinimumSize(QSize(0, 50))
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        self.verticalLayout_5.addWidget(self.lineEdit_password)

        self.checkBox = QCheckBox(self.widget1)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setMinimumSize(QSize(0, 35))
        self.checkBox.setChecked(True)

        self.verticalLayout_5.addWidget(self.checkBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_login = QPushButton(self.widget1)
        self.pushButton_login.setObjectName(u"pushButton_login")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButton_login.sizePolicy().hasHeightForWidth())
        self.pushButton_login.setSizePolicy(sizePolicy3)
        self.pushButton_login.setMinimumSize(QSize(0, 50))
        self.pushButton_login.setMaximumSize(QSize(16777215, 40))
        icon1 = QIcon()
        icon1.addFile(u":/images/images/login.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_login.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.pushButton_login)

        self.pushButton_dislogin = QPushButton(self.widget1)
        self.pushButton_dislogin.setObjectName(u"pushButton_dislogin")
        sizePolicy3.setHeightForWidth(self.pushButton_dislogin.sizePolicy().hasHeightForWidth())
        self.pushButton_dislogin.setSizePolicy(sizePolicy3)
        self.pushButton_dislogin.setMinimumSize(QSize(0, 50))
        self.pushButton_dislogin.setMaximumSize(QSize(16777215, 40))
        icon2 = QIcon()
        icon2.addFile(u":/images/images/logout.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_dislogin.setIcon(icon2)

        self.horizontalLayout_3.addWidget(self.pushButton_dislogin)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.pushButton_login_2 = QPushButton(self.widget1)
        self.pushButton_login_2.setObjectName(u"pushButton_login_2")
        sizePolicy3.setHeightForWidth(self.pushButton_login_2.sizePolicy().hasHeightForWidth())
        self.pushButton_login_2.setSizePolicy(sizePolicy3)
        self.pushButton_login_2.setMinimumSize(QSize(0, 50))
        self.pushButton_login_2.setMaximumSize(QSize(16777215, 40))
        icon3 = QIcon()
        icon3.addFile(u":/images/images/main.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_login_2.setIcon(icon3)

        self.verticalLayout_5.addWidget(self.pushButton_login_2)

        self.stackedWidget_message = QStackedWidget(self.widget1)
        self.stackedWidget_message.setObjectName(u"stackedWidget_message")
        self.stackedWidget_message.setMinimumSize(QSize(0, 0))
        self.stackedWidget_message.setStyleSheet(u"QLabel{\n"
"	font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"}")
        self.black_text = QWidget()
        self.black_text.setObjectName(u"black_text")
        self.black_text.setMinimumSize(QSize(0, 0))
        self.label_black_message = QLabel(self.black_text)
        self.label_black_message.setObjectName(u"label_black_message")
        self.label_black_message.setGeometry(QRect(0, 0, 340, 35))
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_black_message.sizePolicy().hasHeightForWidth())
        self.label_black_message.setSizePolicy(sizePolicy4)
        self.label_black_message.setMinimumSize(QSize(0, 0))
        self.label_black_message.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label_black_message.setAlignment(Qt.AlignCenter)
        self.stackedWidget_message.addWidget(self.black_text)
        self.green_text = QWidget()
        self.green_text.setObjectName(u"green_text")
        sizePolicy4.setHeightForWidth(self.green_text.sizePolicy().hasHeightForWidth())
        self.green_text.setSizePolicy(sizePolicy4)
        self.label_green_message = QLabel(self.green_text)
        self.label_green_message.setObjectName(u"label_green_message")
        self.label_green_message.setGeometry(QRect(0, 0, 340, 35))
        sizePolicy4.setHeightForWidth(self.label_green_message.sizePolicy().hasHeightForWidth())
        self.label_green_message.setSizePolicy(sizePolicy4)
        self.label_green_message.setMinimumSize(QSize(0, 0))
        self.label_green_message.setStyleSheet(u"color: rgb(0, 255, 0);")
        self.label_green_message.setAlignment(Qt.AlignCenter)
        self.stackedWidget_message.addWidget(self.green_text)
        self.red_text = QWidget()
        self.red_text.setObjectName(u"red_text")
        self.label_red_message = QLabel(self.red_text)
        self.label_red_message.setObjectName(u"label_red_message")
        self.label_red_message.setGeometry(QRect(0, 0, 340, 35))
        self.label_red_message.setMinimumSize(QSize(0, 0))
        self.label_red_message.setStyleSheet(u"color:rgb(255, 0, 0);")
        self.label_red_message.setAlignment(Qt.AlignCenter)
        self.stackedWidget_message.addWidget(self.red_text)

        self.verticalLayout_5.addWidget(self.stackedWidget_message)

        self.stackedWidget_tab.addWidget(self.page_main)
        self.page_manege = QWidget()
        self.page_manege.setObjectName(u"page_manege")
        self.frame_2 = QFrame(self.page_manege)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 0, 601, 431))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.splitter = QSplitter(self.frame_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.time_edit = QTimeEdit(self.splitter)
        self.time_edit.setObjectName(u"time_edit")
        self.splitter.addWidget(self.time_edit)
        self.file_path_edit = QLineEdit(self.splitter)
        self.file_path_edit.setObjectName(u"file_path_edit")
        self.splitter.addWidget(self.file_path_edit)
        self.select_file_btn = QPushButton(self.splitter)
        self.select_file_btn.setObjectName(u"select_file_btn")
        self.splitter.addWidget(self.select_file_btn)

        self.verticalLayout_4.addWidget(self.splitter)

        self.task_name_label = QLabel(self.frame_2)
        self.task_name_label.setObjectName(u"task_name_label")
        self.task_name_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.task_name_label)

        self.create_btn = QPushButton(self.frame_2)
        self.create_btn.setObjectName(u"create_btn")

        self.verticalLayout_4.addWidget(self.create_btn)

        self.query_btn = QPushButton(self.frame_2)
        self.query_btn.setObjectName(u"query_btn")

        self.verticalLayout_4.addWidget(self.query_btn)

        self.delete_btn = QPushButton(self.frame_2)
        self.delete_btn.setObjectName(u"delete_btn")

        self.verticalLayout_4.addWidget(self.delete_btn)

        self.task_table = QTableWidget(self.frame_2)
        self.task_table.setObjectName(u"task_table")
        self.task_table.setTabletTracking(True)
        self.task_table.setStyleSheet(u"")
        self.task_table.setFrameShape(QFrame.Box)
        self.task_table.setFrameShadow(QFrame.Raised)
        self.task_table.setLineWidth(1)
        self.task_table.setMidLineWidth(0)
        self.task_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.task_table.setAutoScroll(False)
        self.task_table.setAutoScrollMargin(0)
        self.task_table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.task_table.setProperty(u"showDropIndicator", False)
        self.task_table.setDragDropOverwriteMode(False)
        self.task_table.setAlternatingRowColors(True)
        self.task_table.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_table.setGridStyle(Qt.SolidLine)
        self.task_table.setSortingEnabled(True)
        self.task_table.setCornerButtonEnabled(False)
        self.task_table.setColumnCount(0)
        self.task_table.horizontalHeader().setVisible(False)
        self.task_table.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.task_table.horizontalHeader().setStretchLastSection(True)
        self.task_table.verticalHeader().setVisible(False)

        self.verticalLayout_4.addWidget(self.task_table)

        self.stackedWidget_tab.addWidget(self.page_manege)

        self.verticalLayout.addWidget(self.stackedWidget_tab)

        self.frame_title = QFrame(self.widget)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setGeometry(QRect(0, 0, 600, 40))
        self.frame_title.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.frame_title.setStyleSheet(u"QPushButton{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}\n"
"QPushButton:hover {\n"
"	padding-bottom: 8px;\n"
"	padding-left:8px;\n"
"}\n"
"QPushButton:pressed{\n"
"	padding-top:3px;\n"
"	padding-right:3px;\n"
"}\n"
"#pushButtom_title {\n"
"	font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"    padding: 0;\n"
"}\n"
"#frame_title {\n"
"    border: none; \n"
"	border-top-left-radius: 10px;\n"
"	border-top-right-radius: 10px;\n"
"    border: 1px solid rgb(204, 204, 204); \n"
"}")
        self.frame_title.setFrameShape(QFrame.StyledPanel)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_title)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 3, 8, 0)
        self.pushButtom_title = QPushButton(self.frame_title)
        self.pushButtom_title.setObjectName(u"pushButtom_title")
        self.pushButtom_title.setStyleSheet(u"margin-left: 10px;")
        self.pushButtom_title.setIcon(icon)
        self.pushButtom_title.setIconSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.pushButtom_title)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton_minizing = QPushButton(self.frame_title)
        self.pushButton_minizing.setObjectName(u"pushButton_minizing")
        sizePolicy1.setHeightForWidth(self.pushButton_minizing.sizePolicy().hasHeightForWidth())
        self.pushButton_minizing.setSizePolicy(sizePolicy1)
        self.pushButton_minizing.setMinimumSize(QSize(40, 40))
        icon4 = QIcon()
        icon4.addFile(u":/images/images/minizing.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_minizing.setIcon(icon4)
        self.pushButton_minizing.setIconSize(QSize(25, 25))

        self.horizontalLayout_2.addWidget(self.pushButton_minizing)

        self.pushButton_close = QPushButton(self.frame_title)
        self.pushButton_close.setObjectName(u"pushButton_close")
        sizePolicy1.setHeightForWidth(self.pushButton_close.sizePolicy().hasHeightForWidth())
        self.pushButton_close.setSizePolicy(sizePolicy1)
        self.pushButton_close.setMinimumSize(QSize(40, 40))
        self.pushButton_close.setStyleSheet(u"")
        icon5 = QIcon()
        icon5.addFile(u":/images/images/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_close.setIcon(icon5)
        self.pushButton_close.setIconSize(QSize(27, 27))

        self.horizontalLayout_2.addWidget(self.pushButton_close)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton_close.clicked.connect(MainWindow.close)
        self.pushButton_minizing.clicked.connect(MainWindow.showMinimized)

        self.stackedWidget_tab.setCurrentIndex(0)
        self.stackedWidget_message.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u5e7f\u897f\u79d1\u5e08\u6821\u56ed\u7f51\u767b\u5f55\u52a9\u624b", None))
        self.pushButton_tab_main.setText(QCoreApplication.translate("MainWindow", u"\u9996\u9875", None))
        self.pushButton_tab_manege.setText(QCoreApplication.translate("MainWindow", u"\u5b9a\u65f6\u4efb\u52a1\u7ba1\u7406", None))
        self.lineEdit_username.setText("")
        self.lineEdit_username.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u5b66\u53f7/\u5de5\u53f7", None))
        self.lineEdit_password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u5bc6\u7801", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\u8bb0\u4f4f\u5bc6\u7801", None))
        self.pushButton_login.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5f55", None))
        self.pushButton_dislogin.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u7ebf", None))
        self.pushButton_login_2.setText(QCoreApplication.translate("MainWindow", u"\u6839\u636e\u8d26\u53f7\u5bc6\u7801\u751f\u6210\u4e00\u952e\u767b\u5f55\u6587\u4ef6", None))
        self.label_black_message.setText("")
        self.label_green_message.setText("")
        self.label_red_message.setText("")
        self.time_edit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm:ss", None))
        self.select_file_btn.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.task_name_label.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u540d\uff1a", None))
        self.create_btn.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u4efb\u52a1", None))
        self.query_btn.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2\u4efb\u52a1", None))
        self.delete_btn.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u4efb\u52a1", None))
        self.pushButtom_title.setText(QCoreApplication.translate("MainWindow", u"\u5e7f\u897f\u79d1\u5e08\u6821\u56ed\u7f51\u767b\u5f55\u52a9\u624b", None))
        self.pushButton_minizing.setText("")
        self.pushButton_close.setText("")
    # retranslateUi

