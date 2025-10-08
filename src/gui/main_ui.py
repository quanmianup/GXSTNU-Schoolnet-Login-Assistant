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
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QTableWidget,
    QTableWidgetItem, QTextBrowser, QTextEdit, QTimeEdit,
    QVBoxLayout, QWidget)
import window_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(601, 523)
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
        self.action_clear_log = QAction(MainWindow)
        self.action_clear_log.setObjectName(u"action_clear_log")
        self.action_clear_log.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setEnabled(True)
        self.widget.setGeometry(QRect(0, 0, 600, 500))
        self.widget.setStyleSheet(u"* {\n"
"	font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"}\n"
"QPushButton{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}\n"
"QPushButton:hover {\n"
"	padding-bottom: 5px;\n"
"	padding-left:5px;\n"
"}\n"
"QPushButton:pressed{\n"
"	padding-top:3px;\n"
"	padding-right:3px;\n"
"}\n"
"#widget {\n"
"	background-color: white;\n"
"	border-radius: 5px;\n"
"	border: 1px solid rgb(204, 204, 204); \n"
"}")
        self.frame_main = QFrame(self.widget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setGeometry(QRect(0, 40, 600, 460))
        self.frame_main.setStyleSheet(u"")
        self.frame_main.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
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
"    border-top-left-radius: 10px; \n"
"    border: 1px solid #ccc; \n"
"    background-color: #f8f8f8; \n"
"}\n"
"QPushButton:hover{\n"
"	padding-bottom:5px;\n"
"}")
        self.frame_tab.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_tab.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_tab.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.frame_tab)
        self.horizontalLayout.setSpacing(1)
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

        self.horizontalLayout.addWidget(self.pushButton_tab_main, 0, Qt.AlignmentFlag.AlignBottom)

        self.pushButton_tab_manege = QPushButton(self.frame_tab)
        self.pushButton_tab_manege.setObjectName(u"pushButton_tab_manege")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_tab_manege.sizePolicy().hasHeightForWidth())
        self.pushButton_tab_manege.setSizePolicy(sizePolicy1)
        self.pushButton_tab_manege.setMinimumSize(QSize(100, 30))
        self.pushButton_tab_manege.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.pushButton_tab_manege, 0, Qt.AlignmentFlag.AlignBottom)

        self.pushButton_tab_manege_2 = QPushButton(self.frame_tab)
        self.pushButton_tab_manege_2.setObjectName(u"pushButton_tab_manege_2")
        sizePolicy1.setHeightForWidth(self.pushButton_tab_manege_2.sizePolicy().hasHeightForWidth())
        self.pushButton_tab_manege_2.setSizePolicy(sizePolicy1)
        self.pushButton_tab_manege_2.setMinimumSize(QSize(50, 30))
        self.pushButton_tab_manege_2.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.pushButton_tab_manege_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.frame_tab)

        self.stackedWidget_tab = QStackedWidget(self.frame_main)
        self.stackedWidget_tab.setObjectName(u"stackedWidget_tab")
        self.stackedWidget_tab.setStyleSheet(u"QLineEdit{\n"
"	border-radius:5px;\n"
"	background-color: rgb(255, 255, 255);\n"
"	border: 1px solid #dcdcdc;\n"
"}\n"
"QPushButton{\n"
"	border-radius:5px;\n"
"	border: 1px solid #dcdcdc;\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.page_main = QWidget()
        self.page_main.setObjectName(u"page_main")
        self.frame_main_2 = QFrame(self.page_main)
        self.frame_main_2.setObjectName(u"frame_main_2")
        self.frame_main_2.setGeometry(QRect(0, 0, 600, 430))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_main_2.sizePolicy().hasHeightForWidth())
        self.frame_main_2.setSizePolicy(sizePolicy2)
        self.frame_main_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_main_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_main_2)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.frame_left = QFrame(self.frame_main_2)
        self.frame_left.setObjectName(u"frame_left")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_left.sizePolicy().hasHeightForWidth())
        self.frame_left.setSizePolicy(sizePolicy3)
        self.frame_left.setMinimumSize(QSize(230, 0))
        self.frame_left.setStyleSheet(u"")
        self.frame_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_left.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_left)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.frame_left)
        self.frame.setObjectName(u"frame")
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_lefttop = QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_lefttop)

        self.lineEdit_username = QLineEdit(self.frame)
        self.lineEdit_username.setObjectName(u"lineEdit_username")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineEdit_username.sizePolicy().hasHeightForWidth())
        self.lineEdit_username.setSizePolicy(sizePolicy4)
        self.lineEdit_username.setMinimumSize(QSize(0, 30))
        self.lineEdit_username.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_2.addWidget(self.lineEdit_username)

        self.lineEdit_password = QLineEdit(self.frame)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        sizePolicy4.setHeightForWidth(self.lineEdit_password.sizePolicy().hasHeightForWidth())
        self.lineEdit_password.setSizePolicy(sizePolicy4)
        self.lineEdit_password.setMinimumSize(QSize(0, 30))
        self.lineEdit_password.setMaximumSize(QSize(16777215, 30))
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayout_2.addWidget(self.lineEdit_password)

        self.frame_checkBox = QFrame(self.frame)
        self.frame_checkBox.setObjectName(u"frame_checkBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame_checkBox.sizePolicy().hasHeightForWidth())
        self.frame_checkBox.setSizePolicy(sizePolicy5)
        self.frame_checkBox.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_checkBox.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_checkBox)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.checkBox = QCheckBox(self.frame_checkBox)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setMinimumSize(QSize(0, 0))
        self.checkBox.setChecked(True)

        self.horizontalLayout_6.addWidget(self.checkBox)

        self.stackedWidget_message = QStackedWidget(self.frame_checkBox)
        self.stackedWidget_message.setObjectName(u"stackedWidget_message")
        self.stackedWidget_message.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.stackedWidget_message.sizePolicy().hasHeightForWidth())
        self.stackedWidget_message.setSizePolicy(sizePolicy2)
        self.stackedWidget_message.setMinimumSize(QSize(0, 0))
        self.stackedWidget_message.setMaximumSize(QSize(16777215, 20))
        self.stackedWidget_message.setStyleSheet(u"QLabel{\n"
"	font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"}")
        self.black_text = QWidget()
        self.black_text.setObjectName(u"black_text")
        self.black_text.setMinimumSize(QSize(0, 0))
        self.label_black_message = QLabel(self.black_text)
        self.label_black_message.setObjectName(u"label_black_message")
        self.label_black_message.setGeometry(QRect(0, 0, 140, 20))
        sizePolicy2.setHeightForWidth(self.label_black_message.sizePolicy().hasHeightForWidth())
        self.label_black_message.setSizePolicy(sizePolicy2)
        self.label_black_message.setMinimumSize(QSize(0, 20))
        self.label_black_message.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label_black_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stackedWidget_message.addWidget(self.black_text)
        self.green_text = QWidget()
        self.green_text.setObjectName(u"green_text")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.green_text.sizePolicy().hasHeightForWidth())
        self.green_text.setSizePolicy(sizePolicy6)
        self.label_green_message = QLabel(self.green_text)
        self.label_green_message.setObjectName(u"label_green_message")
        self.label_green_message.setGeometry(QRect(0, 0, 140, 20))
        sizePolicy2.setHeightForWidth(self.label_green_message.sizePolicy().hasHeightForWidth())
        self.label_green_message.setSizePolicy(sizePolicy2)
        self.label_green_message.setMinimumSize(QSize(0, 20))
        self.label_green_message.setStyleSheet(u"color: rgb(0, 255, 0);")
        self.label_green_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stackedWidget_message.addWidget(self.green_text)
        self.red_text = QWidget()
        self.red_text.setObjectName(u"red_text")
        self.label_red_message = QLabel(self.red_text)
        self.label_red_message.setObjectName(u"label_red_message")
        self.label_red_message.setGeometry(QRect(0, 0, 140, 20))
        self.label_red_message.setMinimumSize(QSize(0, 20))
        self.label_red_message.setStyleSheet(u"color:rgb(255, 0, 0);")
        self.label_red_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stackedWidget_message.addWidget(self.red_text)

        self.horizontalLayout_6.addWidget(self.stackedWidget_message)


        self.verticalLayout_2.addWidget(self.frame_checkBox)

        self.frame_login = QFrame(self.frame)
        self.frame_login.setObjectName(u"frame_login")
        self.horizontalLayout_3 = QHBoxLayout(self.frame_login)
        self.horizontalLayout_3.setSpacing(7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_login = QPushButton(self.frame_login)
        self.pushButton_login.setObjectName(u"pushButton_login")
        sizePolicy2.setHeightForWidth(self.pushButton_login.sizePolicy().hasHeightForWidth())
        self.pushButton_login.setSizePolicy(sizePolicy2)
        self.pushButton_login.setMinimumSize(QSize(0, 30))
        self.pushButton_login.setMaximumSize(QSize(16777215, 30))
        icon1 = QIcon()
        icon1.addFile(u":/images/images/login.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_login.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.pushButton_login)

        self.pushButton_dislogin = QPushButton(self.frame_login)
        self.pushButton_dislogin.setObjectName(u"pushButton_dislogin")
        sizePolicy2.setHeightForWidth(self.pushButton_dislogin.sizePolicy().hasHeightForWidth())
        self.pushButton_dislogin.setSizePolicy(sizePolicy2)
        self.pushButton_dislogin.setMinimumSize(QSize(0, 30))
        self.pushButton_dislogin.setMaximumSize(QSize(16777215, 30))
        icon2 = QIcon()
        icon2.addFile(u":/images/images/dislogin.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_dislogin.setIcon(icon2)

        self.horizontalLayout_3.addWidget(self.pushButton_dislogin)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_2.addWidget(self.frame_login)

        self.pushButton_generate = QPushButton(self.frame)
        self.pushButton_generate.setObjectName(u"pushButton_generate")
        sizePolicy2.setHeightForWidth(self.pushButton_generate.sizePolicy().hasHeightForWidth())
        self.pushButton_generate.setSizePolicy(sizePolicy2)
        self.pushButton_generate.setMinimumSize(QSize(120, 30))
        self.pushButton_generate.setMaximumSize(QSize(16777215, 40))
        icon3 = QIcon()
        icon3.addFile(u":/images/images/main.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_generate.setIcon(icon3)

        self.verticalLayout_2.addWidget(self.pushButton_generate)

        self.pushButton_keeplogin = QPushButton(self.frame)
        self.pushButton_keeplogin.setObjectName(u"pushButton_keeplogin")
        sizePolicy2.setHeightForWidth(self.pushButton_keeplogin.sizePolicy().hasHeightForWidth())
        self.pushButton_keeplogin.setSizePolicy(sizePolicy2)
        self.pushButton_keeplogin.setMinimumSize(QSize(0, 30))
        icon4 = QIcon()
        icon4.addFile(u":/images/images/\u5173.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon4.addFile(u":/images/images/\u5f00\u5173.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.pushButton_keeplogin.setIcon(icon4)
        self.pushButton_keeplogin.setIconSize(QSize(25, 25))
        self.pushButton_keeplogin.setCheckable(True)
        self.pushButton_keeplogin.setChecked(False)

        self.verticalLayout_2.addWidget(self.pushButton_keeplogin)

        self.frame_netstatus = QFrame(self.frame)
        self.frame_netstatus.setObjectName(u"frame_netstatus")
        sizePolicy5.setHeightForWidth(self.frame_netstatus.sizePolicy().hasHeightForWidth())
        self.frame_netstatus.setSizePolicy(sizePolicy5)
        self.frame_netstatus.setMinimumSize(QSize(0, 30))
        self.frame_netstatus.setStyleSheet(u"border-radius: 5px;")
        self.frame_netstatus.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_netstatus.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_netstatus)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget_message_netstatus = QStackedWidget(self.frame_netstatus)
        self.stackedWidget_message_netstatus.setObjectName(u"stackedWidget_message_netstatus")
        self.stackedWidget_message_netstatus.setMinimumSize(QSize(0, 0))
        self.stackedWidget_message_netstatus.setMaximumSize(QSize(16777215, 30))
        self.stackedWidget_message_netstatus.setStyleSheet(u"")
        self.black_text_2 = QWidget()
        self.black_text_2.setObjectName(u"black_text_2")
        self.black_text_2.setMinimumSize(QSize(0, 0))
        self.label_black_message_2 = QLabel(self.black_text_2)
        self.label_black_message_2.setObjectName(u"label_black_message_2")
        self.label_black_message_2.setGeometry(QRect(0, 0, 210, 30))
        sizePolicy2.setHeightForWidth(self.label_black_message_2.sizePolicy().hasHeightForWidth())
        self.label_black_message_2.setSizePolicy(sizePolicy2)
        self.label_black_message_2.setMinimumSize(QSize(0, 0))
        self.label_black_message_2.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"font: 11pt \"\u9ed1\u4f53\";")
        self.label_black_message_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labe_netstatus = QLabel(self.black_text_2)
        self.labe_netstatus.setObjectName(u"labe_netstatus")
        self.labe_netstatus.setGeometry(QRect(10, 0, 65, 30))
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(25)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.labe_netstatus.sizePolicy().hasHeightForWidth())
        self.labe_netstatus.setSizePolicy(sizePolicy7)
        self.stackedWidget_message_netstatus.addWidget(self.black_text_2)
        self.green_text_2 = QWidget()
        self.green_text_2.setObjectName(u"green_text_2")
        sizePolicy6.setHeightForWidth(self.green_text_2.sizePolicy().hasHeightForWidth())
        self.green_text_2.setSizePolicy(sizePolicy6)
        self.green_text_2.setStyleSheet(u"background-color: rgb(200, 255, 164);")
        self.label_green_message_2 = QLabel(self.green_text_2)
        self.label_green_message_2.setObjectName(u"label_green_message_2")
        self.label_green_message_2.setGeometry(QRect(0, 0, 210, 30))
        sizePolicy2.setHeightForWidth(self.label_green_message_2.sizePolicy().hasHeightForWidth())
        self.label_green_message_2.setSizePolicy(sizePolicy2)
        self.label_green_message_2.setMinimumSize(QSize(0, 0))
        self.label_green_message_2.setStyleSheet(u"color: rgb(0, 255, 0);\n"
"font: 11pt \"\u9ed1\u4f53\";")
        self.label_green_message_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labe_netstatus_2 = QLabel(self.green_text_2)
        self.labe_netstatus_2.setObjectName(u"labe_netstatus_2")
        self.labe_netstatus_2.setGeometry(QRect(10, 0, 65, 30))
        sizePolicy7.setHeightForWidth(self.labe_netstatus_2.sizePolicy().hasHeightForWidth())
        self.labe_netstatus_2.setSizePolicy(sizePolicy7)
        self.stackedWidget_message_netstatus.addWidget(self.green_text_2)
        self.red_text_2 = QWidget()
        self.red_text_2.setObjectName(u"red_text_2")
        self.red_text_2.setStyleSheet(u"background-color: rgb(255, 190, 191);")
        self.label_red_message_2 = QLabel(self.red_text_2)
        self.label_red_message_2.setObjectName(u"label_red_message_2")
        self.label_red_message_2.setGeometry(QRect(0, 0, 210, 30))
        self.label_red_message_2.setMinimumSize(QSize(0, 0))
        self.label_red_message_2.setStyleSheet(u"color:rgb(255, 0, 0);\n"
"font: 11pt \"\u9ed1\u4f53\";")
        self.label_red_message_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labe_netstatus_3 = QLabel(self.red_text_2)
        self.labe_netstatus_3.setObjectName(u"labe_netstatus_3")
        self.labe_netstatus_3.setGeometry(QRect(10, 0, 65, 30))
        sizePolicy7.setHeightForWidth(self.labe_netstatus_3.sizePolicy().hasHeightForWidth())
        self.labe_netstatus_3.setSizePolicy(sizePolicy7)
        self.stackedWidget_message_netstatus.addWidget(self.red_text_2)

        self.horizontalLayout_7.addWidget(self.stackedWidget_message_netstatus)


        self.verticalLayout_2.addWidget(self.frame_netstatus)

        self.verticalSpacer_leftbottom = QSpacerItem(143, 56, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_leftbottom)


        self.gridLayout_3.addWidget(self.frame, 0, 1, 1, 1)


        self.horizontalLayout_4.addWidget(self.frame_left)

        self.frame_right = QFrame(self.frame_main_2)
        self.frame_right.setObjectName(u"frame_right")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy8.setHorizontalStretch(1)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.frame_right.sizePolicy().hasHeightForWidth())
        self.frame_right.setSizePolicy(sizePolicy8)
        self.frame_right.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_right.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_right)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.textBrowser_log = QTextBrowser(self.frame_right)
        self.textBrowser_log.setObjectName(u"textBrowser_log")
        sizePolicy6.setHeightForWidth(self.textBrowser_log.sizePolicy().hasHeightForWidth())
        self.textBrowser_log.setSizePolicy(sizePolicy6)
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.textBrowser_log.setFont(font)
        self.textBrowser_log.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.textBrowser_log.setStyleSheet(u"#textBrowser_log {\n"
"	background-color: rgb(223, 223, 223);\n"
"	border:2px solid rgb(162, 162, 162);\n"
"	border-radius:5px;\n"
"	font: 10pt \"Consolas\";\n"
"}")
        self.textBrowser_log.setTabChangesFocus(True)
        self.textBrowser_log.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.textBrowser_log.setOpenExternalLinks(True)

        self.gridLayout_2.addWidget(self.textBrowser_log, 0, 0, 1, 1)


        self.horizontalLayout_4.addWidget(self.frame_right)

        self.stackedWidget_tab.addWidget(self.page_main)
        self.page_manege = QWidget()
        self.page_manege.setObjectName(u"page_manege")
        self.frame_manege = QFrame(self.page_manege)
        self.frame_manege.setObjectName(u"frame_manege")
        self.frame_manege.setGeometry(QRect(0, 0, 600, 430))
        self.frame_manege.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_manege.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_manege)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_timefile = QFrame(self.frame_manege)
        self.frame_timefile.setObjectName(u"frame_timefile")
        self.frame_timefile.setMinimumSize(QSize(0, 30))
        self.frame_timefile.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_timefile.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_timefile)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.time_edit = QTimeEdit(self.frame_timefile)
        self.time_edit.setObjectName(u"time_edit")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.time_edit.sizePolicy().hasHeightForWidth())
        self.time_edit.setSizePolicy(sizePolicy9)

        self.horizontalLayout_8.addWidget(self.time_edit)

        self.file_path_edit = QLineEdit(self.frame_timefile)
        self.file_path_edit.setObjectName(u"file_path_edit")
        sizePolicy4.setHeightForWidth(self.file_path_edit.sizePolicy().hasHeightForWidth())
        self.file_path_edit.setSizePolicy(sizePolicy4)

        self.horizontalLayout_8.addWidget(self.file_path_edit)

        self.select_file_btn = QPushButton(self.frame_timefile)
        self.select_file_btn.setObjectName(u"select_file_btn")
        sizePolicy9.setHeightForWidth(self.select_file_btn.sizePolicy().hasHeightForWidth())
        self.select_file_btn.setSizePolicy(sizePolicy9)

        self.horizontalLayout_8.addWidget(self.select_file_btn)

        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 4)
        self.horizontalLayout_8.setStretch(2, 1)

        self.verticalLayout_3.addWidget(self.frame_timefile)

        self.task_name_label = QLabel(self.frame_manege)
        self.task_name_label.setObjectName(u"task_name_label")
        self.task_name_label.setLineWidth(1)
        self.task_name_label.setMidLineWidth(0)
        self.task_name_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.task_name_label.setMargin(0)
        self.task_name_label.setIndent(0)

        self.verticalLayout_3.addWidget(self.task_name_label)

        self.frame_task_btn = QFrame(self.frame_manege)
        self.frame_task_btn.setObjectName(u"frame_task_btn")
        sizePolicy4.setHeightForWidth(self.frame_task_btn.sizePolicy().hasHeightForWidth())
        self.frame_task_btn.setSizePolicy(sizePolicy4)
        self.frame_task_btn.setMinimumSize(QSize(0, 30))
        self.frame_task_btn.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_task_btn.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_task_btn)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.create_btn = QPushButton(self.frame_task_btn)
        self.create_btn.setObjectName(u"create_btn")
        sizePolicy2.setHeightForWidth(self.create_btn.sizePolicy().hasHeightForWidth())
        self.create_btn.setSizePolicy(sizePolicy2)
        self.create_btn.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_5.addWidget(self.create_btn)

        self.delete_btn = QPushButton(self.frame_task_btn)
        self.delete_btn.setObjectName(u"delete_btn")
        sizePolicy2.setHeightForWidth(self.delete_btn.sizePolicy().hasHeightForWidth())
        self.delete_btn.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.delete_btn)

        self.query_btn = QPushButton(self.frame_task_btn)
        self.query_btn.setObjectName(u"query_btn")
        sizePolicy2.setHeightForWidth(self.query_btn.sizePolicy().hasHeightForWidth())
        self.query_btn.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.query_btn)


        self.verticalLayout_3.addWidget(self.frame_task_btn)

        self.task_table = QTableWidget(self.frame_manege)
        self.task_table.setObjectName(u"task_table")
        self.task_table.setTabletTracking(True)
        self.task_table.setStyleSheet(u"")
        self.task_table.setFrameShape(QFrame.Shape.Box)
        self.task_table.setFrameShadow(QFrame.Shadow.Raised)
        self.task_table.setLineWidth(1)
        self.task_table.setMidLineWidth(0)
        self.task_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.task_table.setAutoScroll(False)
        self.task_table.setAutoScrollMargin(0)
        self.task_table.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.task_table.setProperty(u"showDropIndicator", False)
        self.task_table.setDragDropOverwriteMode(False)
        self.task_table.setAlternatingRowColors(True)
        self.task_table.setSelectionMode(QAbstractItemView.SelectionMode.ContiguousSelection)
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.task_table.setGridStyle(Qt.PenStyle.SolidLine)
        self.task_table.setSortingEnabled(True)
        self.task_table.setCornerButtonEnabled(False)
        self.task_table.setColumnCount(0)
        self.task_table.horizontalHeader().setVisible(False)
        self.task_table.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.task_table.horizontalHeader().setStretchLastSection(True)
        self.task_table.verticalHeader().setVisible(False)

        self.verticalLayout_3.addWidget(self.task_table)

        self.stackedWidget_tab.addWidget(self.page_manege)
        self.page_other = QWidget()
        self.page_other.setObjectName(u"page_other")
        self.frame_3 = QFrame(self.page_other)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(0, 0, 600, 430))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(3, 3, 3, 3)
        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.stackedWidget_other = QStackedWidget(self.frame_4)
        self.stackedWidget_other.setObjectName(u"stackedWidget_other")
        self.stackedWidget_other.setGeometry(QRect(0, 0, 481, 420))
        self.page_help = QWidget()
        self.page_help.setObjectName(u"page_help")
        self.frame_help = QFrame(self.page_help)
        self.frame_help.setObjectName(u"frame_help")
        self.frame_help.setGeometry(QRect(0, 0, 480, 410))
        self.frame_help.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_help.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_help.setLineWidth(0)
        self.textBrowser_help = QTextBrowser(self.frame_help)
        self.textBrowser_help.setObjectName(u"textBrowser_help")
        self.textBrowser_help.setGeometry(QRect(10, 0, 470, 400))
        sizePolicy2.setHeightForWidth(self.textBrowser_help.sizePolicy().hasHeightForWidth())
        self.textBrowser_help.setSizePolicy(sizePolicy2)
        self.textBrowser_help.setFrameShape(QFrame.Shape.NoFrame)
        self.textBrowser_help.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.textBrowser_help.setMarkdown(u"**1.\u9996\u9875\u64cd\u4f5c**\n"
"\n"
"**1.1.\u767b\u5f55/\u4e0b\u7ebf\u529f\u80fd**\n"
"\n"
"\u5355\u51fb\u9996\u9875\u6807\u7b7e\uff0c\u5728\u8f93\u5165\u6846\u8f93\u5165\u8d26\u53f7\u5bc6\u7801\uff0c\u70b9\u51fb\u201c\u767b\u5f55\u201d/\u201c\u4e0b\u7ebf\u201d\u6309\u94ae**\u8fde\u63a5/\u4e0b\u7ebf**\u6821\u56ed\u7f51\uff1b\u52fe\u9009\u201c\u8bb0\u4f4f\u5bc6\u7801\u201d\u53ef\u5728\u4e0b\u6b21\u6253\u5f00\u7a0b\u5e8f\u65f6\uff0c\u81ea\u52a8\u8f93\u5165\u8d26\u53f7\u4fe1\u606f\u3002\n"
"\n"
"**1.2.\u751f\u6210\u4e00\u952e\u767b\u5f55\u6587\u4ef6**\n"
"\n"
"\u70b9\u51fb\u201c\u751f\u6210\u4e00\u952e\u767b\u5f55\u6587\u4ef6\u201d\u6309\u94ae\u53ef\u4ee5\u5728***C:\\\\ScheduledTasks***\u6587\u4ef6\u5939\u4e0b\u751f\u6210***AutoLoginScript.exe***\n"
"\u6587\u4ef6\uff0c\u53cc\u51fb\u8fd9\u4e2a\u6587\u4ef6\u53ef\u4ee5\u81ea\u52a8\u767b\u5f55\u6821\u56ed\u7f51\uff08\u8981\u6c42\u81f3\u5c11\u5728\u9996\u9875\u767b\u5f55\u8fc7\u4e00\u6b21\u5e76\u52fe\u9009\u201c\u8bb0\u4f4f\u5bc6\u7801\u201d\u9009\u9879\uff0c\u786e"
                        "\u4fdd\u5728\u6253\u5f00\u7a0b\u5e8f\u65f6\u80fd\u81ea\u52a8\u586b\u5199\u8d26\u53f7\u5bc6\u7801\uff09\u3002\n"
"\n"
"**1.3\u4fdd\u6301\u7f51\u7edc\u5728\u7ebf**\n"
"\n"
"\u7a0b\u5e8f\u4f1a\u6bcf5\u79d2\u81ea\u52a8\u68c0\u6d4b\u7f51\u7edc\u8fde\u63a5\u72b6\u6001\uff0c\u70b9\u51fb\"\u4fdd\u6301\u7f51\u7edc\u5728\u7ebf\"\u6309\u94ae\u53ef\u5f00\u542f\u4fdd\u6301\u7f51\u7edc\u5728\u7ebf\u529f\u80fd\uff0c\u5728**7\uff1a00-24:00**\u65f6\u95f4\u6bb5\u82e5\u68c0\u6d4b\u5230\u7f51\u7edc**\u672a\u8fde\u63a5**\uff0c\u4f1a\u5c1d\u8bd5**\u81ea\u52a8\u767b\u5f55**\n"
"\u6821\u56ed\u7f51\u3002\n"
"\n"
"**1.4\u65e5\u5fd7\u67e5\u770b**\n"
"\n"
"\u53f3\u4fa7\u65e5\u5fd7\u533a\u57df\u663e\u793a\u64cd\u4f5c\u8bb0\u5f55\uff0c\u53f3\u952e\u70b9\u51fb\u53ef\u6253\u5f00\u201c\u6e05\u7a7a\u8f93\u51fa\u201d\u83dc\u5355\u3002\n"
"\n"
"**2.\u5b9a\u65f6\u4efb\u52a1\u7ba1\u7406**\n"
"\n"
"\u5207\u6362\u5230\"\u5b9a\u65f6\u4efb\u52a1\u7ba1\u7406\"\u6807\u7b7e\u9875\uff0c\u53ef\u521b\u5efa\u3001\u5220\u9664\u548c\u67e5\u8be2\u5b9a\u65f6\u4efb"
                        "\u52a1\u3002\n"
"\n"
"**2.1.\u5b9a\u65f6\u4efb\u52a1\u4f7f\u7528\u8bf4\u660e**\n"
"\n"
"2.1.1\u5c06***AutoLoginScript.exe***\u6587\u4ef6\u52a0\u5165\u5b9a\u65f6\u4efb\u52a1\u53ef\u5b9e\u73b0\u5b9a\u65f6\u767b\u5f55\u6821\u56ed\u7f51\u529f\u80fd\u3002\n"
"\n"
"2.1.2\u9996\u5148\u8bbe\u7f6e\u9700\u8981\u5b9a\u65f6\u542f\u52a8\u7684\u65f6\u95f4\uff0c\u968f\u540e\u70b9\u51fb\u201c\u9009\u62e9\u6587\u4ef6\u201d\u6309\u94ae\u9009\u62e9\u9700\u8981\u5b9a\u65f6\u6267\u884c\u7684\u6587\u4ef6\uff0c\u6bd4\u5982\u201c\n"
"***C:\\\\ScheduledTasks\\\\AutoLoginScript.exe***\u201d\uff0c\u70b9\u51fb\u201c\u521b\u5efa\u4efb\u52a1\u201d\u6309\u94ae\u5373\u53ef\u3002\n"
"\n"
"2.1.3\u5220\u9664\u4efb\u52a1\u9700\u8981\u5148\u9009\u4e2d\u4efb\u52a1\uff0c\u518d\u5355\u51fb\u201c\u5220\u9664\u4efb\u52a1\u201d\u6309\u94ae\u5373\u53ef\u3002\n"
"\n"
"**\\**\u5e38\u89c1\u95ee\u9898****\n"
"\n"
"\\- \u767b\u5f55\u5931\u8d25\uff1a\u68c0\u67e5\u8d26\u53f7\u5bc6\u7801\u548c\u7f51\u7edc\u8fde\u63a5\uff0c\u786e\u5b9a\u7f51\u5173ip\u4e3a172.16."
                        "x.x\uff0c\u67e5\u770b\u65e5\u5fd7\u83b7\u53d6\u9519\u8bef\u539f\u56e0\n"
"\n"
"\\- \u4efb\u52a1\u4e0d\u6267\u884c\uff1a\u786e\u8ba4EXE\u6587\u4ef6\u8def\u5f84\u6b63\u786e\uff0c\u68c0\u67e5Windows\u4efb\u52a1\u8ba1\u5212\u7a0b\u5e8f\u8bbe\u7f6e\n"
"\n"
"\u6ce8\u610f\u4e8b\u9879\n"
"\n"
"\\- \u8d26\u53f7\u5bc6\u7801\u4f7f\u7528AES\u52a0\u5bc6\u5b58\u50a8\n"
"\n"
"\\- \u751f\u6210\u7684EXE\u6587\u4ef6\u5305\u542b\u8d26\u53f7\u4fe1\u606f\uff0c\u8bf7\u59a5\u5584\u4fdd\u7ba1\n"
"\n"
"\\- \u65e5\u5fd7\u4fdd\u5b58\u5728c:\\\\ScheduledTasks\\\\logs\u76ee\u5f55\n"
"\n"
"")
        self.stackedWidget_other.addWidget(self.page_help)
        self.page_update = QWidget()
        self.page_update.setObjectName(u"page_update")
        self.progressBar = QProgressBar(self.page_update)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(20, 240, 441, 23))
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)
        self.checkBox_update = QCheckBox(self.page_update)
        self.checkBox_update.setObjectName(u"checkBox_update")
        self.checkBox_update.setGeometry(QRect(330, 280, 121, 31))
        self.checkBox_update.setChecked(True)
        self.checkBox_update.setTristate(False)
        self.stackedWidget_other.addWidget(self.page_update)
        self.page_disclaimer = QWidget()
        self.page_disclaimer.setObjectName(u"page_disclaimer")
        self.textBrowser_disclaimer = QTextBrowser(self.page_disclaimer)
        self.textBrowser_disclaimer.setObjectName(u"textBrowser_disclaimer")
        self.textBrowser_disclaimer.setGeometry(QRect(10, 0, 470, 400))
        sizePolicy2.setHeightForWidth(self.textBrowser_disclaimer.sizePolicy().hasHeightForWidth())
        self.textBrowser_disclaimer.setSizePolicy(sizePolicy2)
        self.textBrowser_disclaimer.setFrameShape(QFrame.Shape.NoFrame)
        self.textBrowser_disclaimer.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.textBrowser_disclaimer.setMarkdown(u"\u514d\u8d23\u58f0\u660e\n"
"\n"
"1\\. \u672c\u8f6f\u4ef6\u4ec5\u7528\u4e8e\u4e2a\u4eba\u5b66\u4e60\u548c\u6d4b\u8bd5\u4f7f\u7528\uff0c\u65e0\u9700\u63d0\u4f9b\u4efb\u4f55\u4ee3\u4ef7\uff0c\u5e76\u4e0d\u53ef\u7528\u4e8e\u4efb\u4f55\u5546\u4e1a\u7528\u9014\u53ca\u76ee\u7684\uff08\u5305\u62ec\u4e8c\u6b21\u5f00\u53d1\uff09\uff1b\n"
"\n"
"2\\. \u5de5\u5177\u4ec5\u7528\u4e8e\u7b80\u5316\u5e7f\u897f\u79d1\u6280\u5e08\u8303\u5b66\u9662\u6821\u56ed\u7f51\u7684\u767b\u5f55/\u6ce8\u9500\u64cd\u4f5c\uff0c\u4e0d\u4f1a\u7834\u89e3\u3001\u7ed5\u8fc7\u6216\u5e72\u6270\u6821\u56ed\u7f51\u7684\u6b63\u5e38\u8ba4\u8bc1\u6d41\u7a0b\uff0c\u6240\u6709\u64cd\u4f5c\u5747\u57fa\u4e8e\u7528\u6237\u4e3b\u52a8\u63d0\u4f9b\u7684\u8d26\u53f7\u4fe1\u606f\uff1b\n"
"\n"
"3\\. \u4f7f\u7528\u672c\u8f6f\u4ef6\u65f6\u8bf7\u9075\u5b88\u76f8\u5173\u6cd5\u5f8b\u6cd5\u89c4\u4ee5\u53ca\u5e7f\u897f\u79d1\u6280\u5e08\u8303\u5b66\u9662\u6821\u56ed\u7f51\u4f7f\u7528\u89c4\u5b9a\uff0c\u4e0d\u5f97\u7528\u4e8e\u4efb\u4f55\u8fdd\u6cd5\u7528\u9014\uff1b\n"
"\n"
""
                        "4\\. \u672c\u5de5\u5177\u63a8\u8350\u4f7f\u7528\u8005\u901a\u8fc7\u5b98\u65b9\u6e20\u9053\u83b7\u53d6\u6821\u56ed\u7f51\u670d\u52a1\uff0c\u4f7f\u7528\u8005\u9700\u9075\u5b88\u5b66\u6821\u7f51\u7edc\u7ba1\u7406\u89c4\u5b9a\uff0c\u82e5\u5b66\u6821\u7981\u6b62\u4f7f\u7528\u7b2c\u4e09\u65b9\u767b\u5f55\u5de5\u5177\uff0c\u8bf7\u7acb\u5373\u505c\u6b62\u5de5\u5177\u7684\u4f7f\u7528\u5e76\u5220\u9664\u5de5\u5177\uff1b\n"
"\n"
"5\\. \u672c\u8f6f\u4ef6\u5f00\u6e90\u514d\u8d39\uff0c\u4f5c\u8005\u4e0d\u5bf9\u4f7f\u7528\u672c\u8f6f\u4ef6\u9020\u6210\u7684\u4efb\u4f55\u76f4\u63a5\u6216\u95f4\u63a5\u635f\u5931\u8d1f\u8d23\uff08\u5305\u62ec\u4f46\u4e0d\u9650\u4e8e\u8d26\u53f7\u5f02\u5e38\u3001\u7f51\u7edc\u4e2d\u65ad\u3001\u6570\u636e\u4e22\u5931\u7b49\uff09\uff1b\n"
"\n"
"6\\. \u4f7f\u7528\u672c\u8f6f\u4ef6\u5373\u8868\u793a\u60a8\u540c\u610f\u672c\u514d\u8d23\u58f0\u660e\u7684\u6240\u6709\u6761\u6b3e\uff1b\n"
"\n"
"7\\. \u82e5\u672c\u5de5\u5177\u6709\u9020\u6210\u4efb\u4f55\u53ef\u80fd\u7684\u4fb5\u6743\u884c\u4e3a\uff0c\u8bf7"
                        "\u8fdb\u884c\u8054\u7cfb\uff0c\u5c06\u4f1a\u7acb\u5373\u505c\u6b62\u53ef\u80fd\u7684\u4fb5\u6743\u884c\u4e3a\uff0c\u5e76\u5173\u95ed\u4ee3\u7801\u4ed3\u5e93\uff1b\n"
"\n"
"8\\. \u672c\u5de5\u5177\u5c06\u6839\u636e\u5e7f\u897f\u79d1\u6280\u5e08\u8303\u5b66\u9662\u6821\u56ed\u7f51\u534f\u8bae\u8fdb\u884c\u6280\u672f\u8c03\u6574\uff0c\u786e\u4fdd\u5408\u6cd5\u5408\u89c4\uff1b\n"
"\n"
"9\\. \u4f5c\u8005\u4fdd\u7559\u5bf9\u672c\u8f6f\u4ef6\u548c\u514d\u8d23\u58f0\u660e\u7684\u6700\u7ec8\u89e3\u91ca\u6743\u3002\n"
"\n"
"")
        self.stackedWidget_other.addWidget(self.page_disclaimer)
        self.page_about = QWidget()
        self.page_about.setObjectName(u"page_about")
        self.textBrowser_about = QTextBrowser(self.page_about)
        self.textBrowser_about.setObjectName(u"textBrowser_about")
        self.textBrowser_about.setGeometry(QRect(30, 0, 430, 400))
        sizePolicy2.setHeightForWidth(self.textBrowser_about.sizePolicy().hasHeightForWidth())
        self.textBrowser_about.setSizePolicy(sizePolicy2)
        self.textBrowser_about.setFrameShape(QFrame.Shape.NoFrame)
        self.textBrowser_about.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.textBrowser_about.setMarkdown(u"\u5e7f\u897f\u79d1\u5e08\u6821\u56ed\u7f51\u767b\u5f55\u52a9\u624b\n"
"\n"
"\u7248\u672c\u53f7\uff1av1.0.0\n"
"\n"
"\u4f5c\u8005\uff1aquanmianup\n"
"\n"
"Gitee\uff1ahttps://gitee.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant\uff08\u4e3b\u63a8\uff09\n"
"\n"
"Github\uff1ahttps://github.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant\n"
"\n"
"\u5f00\u6e90\u534f\u8bae\uff1aMIT License\n"
"\n"
"\u672c\u5de5\u5177\u4ec5\u4f9b\u5b66\u4e60\u4ea4\u6d41\u4f7f\u7528\n"
"\n"
"")
        self.stackedWidget_other.addWidget(self.page_about)

        self.horizontalLayout_9.addWidget(self.frame_4)

        self.frame_other_btnbox = QFrame(self.frame_3)
        self.frame_other_btnbox.setObjectName(u"frame_other_btnbox")
        self.frame_other_btnbox.setMinimumSize(QSize(100, 0))
        self.frame_other_btnbox.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_other_btnbox.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_other_btnbox.setLineWidth(0)
        self.verticalLayout_4 = QVBoxLayout(self.frame_other_btnbox)
        self.verticalLayout_4.setSpacing(17)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.pushButton_help = QPushButton(self.frame_other_btnbox)
        self.pushButton_help.setObjectName(u"pushButton_help")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.pushButton_help.sizePolicy().hasHeightForWidth())
        self.pushButton_help.setSizePolicy(sizePolicy10)
        self.pushButton_help.setMinimumSize(QSize(0, 25))

        self.verticalLayout_4.addWidget(self.pushButton_help)

        self.pushButton_update = QPushButton(self.frame_other_btnbox)
        self.pushButton_update.setObjectName(u"pushButton_update")
        sizePolicy10.setHeightForWidth(self.pushButton_update.sizePolicy().hasHeightForWidth())
        self.pushButton_update.setSizePolicy(sizePolicy10)
        self.pushButton_update.setMinimumSize(QSize(0, 25))

        self.verticalLayout_4.addWidget(self.pushButton_update)

        self.pushButton_disclaimer = QPushButton(self.frame_other_btnbox)
        self.pushButton_disclaimer.setObjectName(u"pushButton_disclaimer")
        sizePolicy10.setHeightForWidth(self.pushButton_disclaimer.sizePolicy().hasHeightForWidth())
        self.pushButton_disclaimer.setSizePolicy(sizePolicy10)
        self.pushButton_disclaimer.setMinimumSize(QSize(0, 25))

        self.verticalLayout_4.addWidget(self.pushButton_disclaimer)

        self.pushButton_about = QPushButton(self.frame_other_btnbox)
        self.pushButton_about.setObjectName(u"pushButton_about")
        sizePolicy2.setHeightForWidth(self.pushButton_about.sizePolicy().hasHeightForWidth())
        self.pushButton_about.setSizePolicy(sizePolicy2)
        self.pushButton_about.setMinimumSize(QSize(0, 25))

        self.verticalLayout_4.addWidget(self.pushButton_about)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.horizontalLayout_9.addWidget(self.frame_other_btnbox)

        self.horizontalLayout_9.setStretch(0, 5)
        self.horizontalLayout_9.setStretch(1, 1)
        self.stackedWidget_tab.addWidget(self.page_other)

        self.verticalLayout.addWidget(self.stackedWidget_tab)

        self.frame_title = QFrame(self.widget)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setGeometry(QRect(0, 0, 600, 30))
        sizePolicy10.setHeightForWidth(self.frame_title.sizePolicy().hasHeightForWidth())
        self.frame_title.setSizePolicy(sizePolicy10)
        self.frame_title.setMinimumSize(QSize(0, 30))
        self.frame_title.setMaximumSize(QSize(16777215, 30))
        self.frame_title.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.frame_title.setStyleSheet(u"\n"
"#pushButtom_title {\n"
"	font: 10pt \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"    padding: 0;\n"
"}\n"
"#frame_title {\n"
"    border: none; \n"
"	border-top-left-radius: 5px;\n"
"	border-top-right-radius: 5px;\n"
"    border: 1px solid rgb(204, 204, 204); \n"
"}")
        self.frame_title.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_title)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 3, 8, 0)
        self.pushButtom_title = QPushButton(self.frame_title)
        self.pushButtom_title.setObjectName(u"pushButtom_title")
        self.pushButtom_title.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButtom_title.sizePolicy().hasHeightForWidth())
        self.pushButtom_title.setSizePolicy(sizePolicy1)
        self.pushButtom_title.setMinimumSize(QSize(0, 25))
        self.pushButtom_title.setMaximumSize(QSize(16777215, 25))
        self.pushButtom_title.setMouseTracking(True)
        self.pushButtom_title.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButtom_title.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.pushButtom_title.setAcceptDrops(True)
        self.pushButtom_title.setStyleSheet(u"margin-left: 10px;")
        self.pushButtom_title.setIcon(icon)
        self.pushButtom_title.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.pushButtom_title)

        self.horizontalSpacer_2 = QSpacerItem(55, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton_minizing = QPushButton(self.frame_title)
        self.pushButton_minizing.setObjectName(u"pushButton_minizing")
        sizePolicy1.setHeightForWidth(self.pushButton_minizing.sizePolicy().hasHeightForWidth())
        self.pushButton_minizing.setSizePolicy(sizePolicy1)
        self.pushButton_minizing.setMinimumSize(QSize(20, 20))
        self.pushButton_minizing.setMaximumSize(QSize(25, 25))
        self.pushButton_minizing.setMouseTracking(True)
        icon5 = QIcon()
        icon5.addFile(u":/images/images/minizing.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_minizing.setIcon(icon5)
        self.pushButton_minizing.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.pushButton_minizing)

        self.pushButton_close = QPushButton(self.frame_title)
        self.pushButton_close.setObjectName(u"pushButton_close")
        sizePolicy1.setHeightForWidth(self.pushButton_close.sizePolicy().hasHeightForWidth())
        self.pushButton_close.setSizePolicy(sizePolicy1)
        self.pushButton_close.setMinimumSize(QSize(20, 20))
        self.pushButton_close.setMaximumSize(QSize(25, 25))
        self.pushButton_close.setMouseTracking(True)
        self.pushButton_close.setStyleSheet(u"")
        icon6 = QIcon()
        icon6.addFile(u":/images/images/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_close.setIcon(icon6)
        self.pushButton_close.setIconSize(QSize(23, 23))

        self.horizontalLayout_2.addWidget(self.pushButton_close)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 601, 22))
        self.menulogMenu = QMenu(self.menuBar)
        self.menulogMenu.setObjectName(u"menulogMenu")
        self.menulogMenu.setTearOffEnabled(False)
        MainWindow.setMenuBar(self.menuBar)
        QWidget.setTabOrder(self.lineEdit_username, self.lineEdit_password)
        QWidget.setTabOrder(self.lineEdit_password, self.checkBox)
        QWidget.setTabOrder(self.checkBox, self.pushButton_login)
        QWidget.setTabOrder(self.pushButton_login, self.pushButton_dislogin)
        QWidget.setTabOrder(self.pushButton_dislogin, self.pushButton_generate)
        QWidget.setTabOrder(self.pushButton_generate, self.pushButton_keeplogin)
        QWidget.setTabOrder(self.pushButton_keeplogin, self.pushButton_tab_main)
        QWidget.setTabOrder(self.pushButton_tab_main, self.pushButton_tab_manege)
        QWidget.setTabOrder(self.pushButton_tab_manege, self.pushButton_tab_manege_2)
        QWidget.setTabOrder(self.pushButton_tab_manege_2, self.pushButton_minizing)
        QWidget.setTabOrder(self.pushButton_minizing, self.pushButton_close)
        QWidget.setTabOrder(self.pushButton_close, self.time_edit)
        QWidget.setTabOrder(self.time_edit, self.file_path_edit)
        QWidget.setTabOrder(self.file_path_edit, self.select_file_btn)
        QWidget.setTabOrder(self.select_file_btn, self.create_btn)
        QWidget.setTabOrder(self.create_btn, self.delete_btn)
        QWidget.setTabOrder(self.delete_btn, self.query_btn)
        QWidget.setTabOrder(self.query_btn, self.textBrowser_log)
        QWidget.setTabOrder(self.textBrowser_log, self.task_table)
        QWidget.setTabOrder(self.task_table, self.pushButtom_title)

        self.menuBar.addAction(self.menulogMenu.menuAction())
        self.menulogMenu.addAction(self.action_clear_log)

        self.retranslateUi(MainWindow)
        self.pushButton_close.clicked.connect(MainWindow.close)
        self.pushButton_minizing.clicked.connect(MainWindow.showMinimized)

        self.stackedWidget_tab.setCurrentIndex(0)
        self.stackedWidget_message.setCurrentIndex(0)
        self.stackedWidget_message_netstatus.setCurrentIndex(0)
        self.stackedWidget_other.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u5e7f\u897f\u79d1\u5e08\u6821\u56ed\u7f51\u767b\u5f55\u52a9\u624b", None))
        self.action_clear_log.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7a7a\u8f93\u51fa", None))
#if QT_CONFIG(tooltip)
        self.action_clear_log.setToolTip(QCoreApplication.translate("MainWindow", u"\u6e05\u7a7a\u65e5\u5fd7\u7ec4\u4ef6\u5185\u5bb9", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_tab_main.setText(QCoreApplication.translate("MainWindow", u"\u9996\u9875", None))
        self.pushButton_tab_manege.setText(QCoreApplication.translate("MainWindow", u"\u5b9a\u65f6\u4efb\u52a1\u7ba1\u7406", None))
        self.pushButton_tab_manege_2.setText(QCoreApplication.translate("MainWindow", u"\u5176\u5b83", None))
        self.lineEdit_username.setText("")
        self.lineEdit_username.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u5b66\u53f7/\u5de5\u53f7", None))
        self.lineEdit_password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u5bc6\u7801", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\u8bb0\u4f4f\u5bc6\u7801", None))
        self.label_black_message.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5f55\u4e2d...", None))
        self.label_green_message.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5f55\u6210\u529f\uff01", None))
        self.label_red_message.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5f55\u5931\u8d25\uff01", None))
        self.pushButton_login.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5f55", None))
        self.pushButton_dislogin.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u7ebf", None))
        self.pushButton_generate.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u4e00\u952e\u767b\u5f55\u6587\u4ef6", None))
        self.pushButton_keeplogin.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u6301\u7f51\u7edc\u5728\u7ebf", None))
        self.label_black_message_2.setText(QCoreApplication.translate("MainWindow", u"   \u68c0\u6d4b\u4e2d...", None))
        self.labe_netstatus.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc\u72b6\u6001\uff1a", None))
        self.label_green_message_2.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u5728\u7ebf", None))
        self.labe_netstatus_2.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc\u72b6\u6001\uff1a", None))
        self.label_red_message_2.setText(QCoreApplication.translate("MainWindow", u"\u79bb\u7ebf\u4e2d", None))
        self.labe_netstatus_3.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u7edc\u72b6\u6001\uff1a", None))
        self.textBrowser_log.setDocumentTitle("")
        self.textBrowser_log.setMarkdown("")
        self.textBrowser_log.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Consolas'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.time_edit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm:ss", None))
        self.select_file_btn.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.task_name_label.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u540d\uff1a", None))
        self.create_btn.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u4efb\u52a1", None))
        self.delete_btn.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u4efb\u52a1", None))
        self.query_btn.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2\u4efb\u52a1", None))
        self.textBrowser_help.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\u5fae\u8f6f\u96c5\u9ed1'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:700;\">1.\u9996\u9875\u64cd\u4f5c</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">1.1.\u767b\u5f55/\u4e0b\u7ebf\u529f\u80fd</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:"
                        "0px; -qt-block-indent:0; text-indent:0px;\">\u5355\u51fb\u9996\u9875\u6807\u7b7e\uff0c\u5728\u8f93\u5165\u6846\u8f93\u5165\u8d26\u53f7\u5bc6\u7801\uff0c\u70b9\u51fb\u201c\u767b\u5f55\u201d/\u201c\u4e0b\u7ebf\u201d\u6309\u94ae<span style=\" font-weight:700;\">\u8fde\u63a5/\u4e0b\u7ebf</span>\u6821\u56ed\u7f51\uff1b\u52fe\u9009\u201c\u8bb0\u4f4f\u5bc6\u7801\u201d\u53ef\u5728\u4e0b\u6b21\u6253\u5f00\u7a0b\u5e8f\u65f6\uff0c\u81ea\u52a8\u8f93\u5165\u8d26\u53f7\u4fe1\u606f\u3002</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">1.2.\u751f\u6210\u4e00\u952e\u767b\u5f55\u6587\u4ef6</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u70b9\u51fb\u201c\u751f\u6210\u4e00\u952e\u767b\u5f55\u6587\u4ef6\u201d\u6309\u94ae\u53ef\u4ee5\u5728<span style=\" font-weight:700; font-style:italic;\">C:\\ScheduledTasks</span>\u6587\u4ef6"
                        "\u5939\u4e0b\u751f\u6210<span style=\" font-weight:700; font-style:italic;\">AutoLoginScript.exe</span>\u6587\u4ef6\uff0c\u53cc\u51fb\u8fd9\u4e2a\u6587\u4ef6\u53ef\u4ee5\u81ea\u52a8\u767b\u5f55\u6821\u56ed\u7f51\uff08\u8981\u6c42\u81f3\u5c11\u5728\u9996\u9875\u767b\u5f55\u8fc7\u4e00\u6b21\u5e76\u52fe\u9009\u201c\u8bb0\u4f4f\u5bc6\u7801\u201d\u9009\u9879\uff0c\u786e\u4fdd\u5728\u6253\u5f00\u7a0b\u5e8f\u65f6\u80fd\u81ea\u52a8\u586b\u5199\u8d26\u53f7\u5bc6\u7801\uff09\u3002</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">1.3\u4fdd\u6301\u7f51\u7edc\u5728\u7ebf</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u7a0b\u5e8f\u4f1a\u6bcf5\u79d2\u81ea\u52a8\u68c0\u6d4b\u7f51\u7edc\u8fde\u63a5\u72b6\u6001\uff0c\u70b9\u51fb&quot;\u4fdd\u6301\u7f51\u7edc\u5728\u7ebf&quot;\u6309\u94ae\u53ef\u5f00\u542f\u4fdd\u6301\u7f51\u7edc"
                        "\u5728\u7ebf\u529f\u80fd\uff0c\u5728<span style=\" font-weight:700;\">7\uff1a00-24:00</span>\u65f6\u95f4\u6bb5\u82e5\u68c0\u6d4b\u5230\u7f51\u7edc<span style=\" font-weight:700;\">\u672a\u8fde\u63a5</span>\uff0c\u4f1a\u5c1d\u8bd5<span style=\" font-weight:700;\">\u81ea\u52a8\u767b\u5f55</span>\u6821\u56ed\u7f51\u3002</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">1.4\u65e5\u5fd7\u67e5\u770b</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u53f3\u4fa7\u65e5\u5fd7\u533a\u57df\u663e\u793a\u64cd\u4f5c\u8bb0\u5f55\uff0c\u53f3\u952e\u70b9\u51fb\u53ef\u6253\u5f00\u201c\u6e05\u7a7a\u8f93\u51fa\u201d\u83dc\u5355\u3002</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:700;\">2.\u5b9a\u65f6\u4efb"
                        "\u52a1\u7ba1\u7406</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u5207\u6362\u5230&quot;\u5b9a\u65f6\u4efb\u52a1\u7ba1\u7406&quot;\u6807\u7b7e\u9875\uff0c\u53ef\u521b\u5efa\u3001\u5220\u9664\u548c\u67e5\u8be2\u5b9a\u65f6\u4efb\u52a1\u3002</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">2.1.\u5b9a\u65f6\u4efb\u52a1\u4f7f\u7528\u8bf4\u660e</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2.1.1\u5c06<span style=\" font-weight:700; font-style:italic;\">AutoLoginScript.exe</span>\u6587\u4ef6\u52a0\u5165\u5b9a\u65f6\u4efb\u52a1\u53ef\u5b9e\u73b0\u5b9a\u65f6\u767b\u5f55\u6821\u56ed\u7f51\u529f\u80fd\u3002</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-ind"
                        "ent:0px;\">2.1.2\u9996\u5148\u8bbe\u7f6e\u9700\u8981\u5b9a\u65f6\u542f\u52a8\u7684\u65f6\u95f4\uff0c\u968f\u540e\u70b9\u51fb\u201c\u9009\u62e9\u6587\u4ef6\u201d\u6309\u94ae\u9009\u62e9\u9700\u8981\u5b9a\u65f6\u6267\u884c\u7684\u6587\u4ef6\uff0c\u6bd4\u5982\u201c<span style=\" font-weight:700; font-style:italic;\">C:\\ScheduledTasks\\AutoLoginScript.exe</span>\u201d\uff0c\u70b9\u51fb\u201c\u521b\u5efa\u4efb\u52a1\u201d\u6309\u94ae\u5373\u53ef\u3002</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2.1.3\u5220\u9664\u4efb\u52a1\u9700\u8981\u5148\u9009\u4e2d\u4efb\u52a1\uff0c\u518d\u5355\u51fb\u201c\u5220\u9664\u4efb\u52a1\u201d\u6309\u94ae\u5373\u53ef\u3002</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:700;\">**\u5e38\u89c1\u95ee\u9898**</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin"
                        "-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- \u767b\u5f55\u5931\u8d25\uff1a\u68c0\u67e5\u8d26\u53f7\u5bc6\u7801\u548c\u7f51\u7edc\u8fde\u63a5\uff0c\u786e\u5b9a\u7f51\u5173ip\u4e3a172.16.x.x\uff0c\u67e5\u770b\u65e5\u5fd7\u83b7\u53d6\u9519\u8bef\u539f\u56e0</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- \u4efb\u52a1\u4e0d\u6267\u884c\uff1a\u786e\u8ba4EXE\u6587\u4ef6\u8def\u5f84\u6b63\u786e\uff0c\u68c0\u67e5Windows\u4efb\u52a1\u8ba1\u5212\u7a0b\u5e8f\u8bbe\u7f6e</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u6ce8\u610f\u4e8b\u9879</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- \u8d26\u53f7\u5bc6\u7801\u4f7f\u7528AES\u52a0\u5bc6\u5b58\u50a8</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-b"
                        "lock-indent:0; text-indent:0px;\">- \u751f\u6210\u7684EXE\u6587\u4ef6\u5305\u542b\u8d26\u53f7\u4fe1\u606f\uff0c\u8bf7\u59a5\u5584\u4fdd\u7ba1</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- \u65e5\u5fd7\u4fdd\u5b58\u5728c:\\ScheduledTasks\\logs\u76ee\u5f55</p></body></html>", None))
        self.checkBox_update.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8\u65f6\u68c0\u67e5\u66f4\u65b0", None))
        self.textBrowser_disclaimer.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\u5fae\u8f6f\u96c5\u9ed1'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u514d\u8d23\u58f0\u660e</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. \u672c\u8f6f\u4ef6\u4ec5\u7528\u4e8e\u4e2a\u4eba\u5b66\u4e60\u548c\u6d4b"
                        "\u8bd5\u4f7f\u7528\uff0c\u65e0\u9700\u63d0\u4f9b\u4efb\u4f55\u4ee3\u4ef7\uff0c\u5e76\u4e0d\u53ef\u7528\u4e8e\u4efb\u4f55\u5546\u4e1a\u7528\u9014\u53ca\u76ee\u7684\uff08\u5305\u62ec\u4e8c\u6b21\u5f00\u53d1\uff09\uff1b</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. \u5de5\u5177\u4ec5\u7528\u4e8e\u7b80\u5316\u5e7f\u897f\u79d1\u6280\u5e08\u8303\u5b66\u9662\u6821\u56ed\u7f51\u7684\u767b\u5f55/\u6ce8\u9500\u64cd\u4f5c\uff0c\u4e0d\u4f1a\u7834\u89e3\u3001\u7ed5\u8fc7\u6216\u5e72\u6270\u6821\u56ed\u7f51\u7684\u6b63\u5e38\u8ba4\u8bc1\u6d41\u7a0b\uff0c\u6240\u6709\u64cd\u4f5c\u5747\u57fa\u4e8e\u7528\u6237\u4e3b\u52a8\u63d0\u4f9b\u7684\u8d26\u53f7\u4fe1\u606f\uff1b</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -q"
                        "t-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. \u4f7f\u7528\u672c\u8f6f\u4ef6\u65f6\u8bf7\u9075\u5b88\u76f8\u5173\u6cd5\u5f8b\u6cd5\u89c4\u4ee5\u53ca\u5e7f\u897f\u79d1\u6280\u5e08\u8303\u5b66\u9662\u6821\u56ed\u7f51\u4f7f\u7528\u89c4\u5b9a\uff0c\u4e0d\u5f97\u7528\u4e8e\u4efb\u4f55\u8fdd\u6cd5\u7528\u9014\uff1b</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4. \u672c\u5de5\u5177\u63a8\u8350\u4f7f\u7528\u8005\u901a\u8fc7\u5b98\u65b9\u6e20\u9053\u83b7\u53d6\u6821\u56ed\u7f51\u670d\u52a1\uff0c\u4f7f\u7528\u8005\u9700\u9075\u5b88\u5b66\u6821\u7f51\u7edc\u7ba1\u7406\u89c4\u5b9a\uff0c\u82e5\u5b66\u6821\u7981\u6b62\u4f7f\u7528\u7b2c\u4e09\u65b9\u767b\u5f55"
                        "\u5de5\u5177\uff0c\u8bf7\u7acb\u5373\u505c\u6b62\u5de5\u5177\u7684\u4f7f\u7528\u5e76\u5220\u9664\u5de5\u5177\uff1b</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5. \u672c\u8f6f\u4ef6\u5f00\u6e90\u514d\u8d39\uff0c\u4f5c\u8005\u4e0d\u5bf9\u4f7f\u7528\u672c\u8f6f\u4ef6\u9020\u6210\u7684\u4efb\u4f55\u76f4\u63a5\u6216\u95f4\u63a5\u635f\u5931\u8d1f\u8d23\uff08\u5305\u62ec\u4f46\u4e0d\u9650\u4e8e\u8d26\u53f7\u5f02\u5e38\u3001\u7f51\u7edc\u4e2d\u65ad\u3001\u6570\u636e\u4e22\u5931\u7b49\uff09\uff1b</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px"
                        ";\">6. \u4f7f\u7528\u672c\u8f6f\u4ef6\u5373\u8868\u793a\u60a8\u540c\u610f\u672c\u514d\u8d23\u58f0\u660e\u7684\u6240\u6709\u6761\u6b3e\uff1b</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">7. \u82e5\u672c\u5de5\u5177\u6709\u9020\u6210\u4efb\u4f55\u53ef\u80fd\u7684\u4fb5\u6743\u884c\u4e3a\uff0c\u8bf7\u8fdb\u884c\u8054\u7cfb\uff0c\u5c06\u4f1a\u7acb\u5373\u505c\u6b62\u53ef\u80fd\u7684\u4fb5\u6743\u884c\u4e3a\uff0c\u5e76\u5173\u95ed\u4ee3\u7801\u4ed3\u5e93\uff1b</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">8. \u672c\u5de5\u5177\u5c06\u6839"
                        "\u636e\u5e7f\u897f\u79d1\u6280\u5e08\u8303\u5b66\u9662\u6821\u56ed\u7f51\u534f\u8bae\u8fdb\u884c\u6280\u672f\u8c03\u6574\uff0c\u786e\u4fdd\u5408\u6cd5\u5408\u89c4\uff1b</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">9. \u4f5c\u8005\u4fdd\u7559\u5bf9\u672c\u8f6f\u4ef6\u548c\u514d\u8d23\u58f0\u660e\u7684\u6700\u7ec8\u89e3\u91ca\u6743\u3002</p></body></html>", None))
        self.textBrowser_about.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\u5fae\u8f6f\u96c5\u9ed1'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0p"
                        "x; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u5e7f\u897f\u79d1\u5e08\u6821\u56ed\u7f51\u767b\u5f55\u52a9\u624b</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u7248\u672c\u53f7\uff1av1.0.0</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u4f5c\u8005\uff1aquanmianup</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Gitee\uff1ahttps://gitee.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant\uff08\u4e3b\u63a8\uff09"
                        "</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Github\uff1ahttps://github.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u5f00\u6e90\u534f\u8bae\uff1aMIT License</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u672c\u5de5\u5177\u4ec5\u4f9b\u5b66\u4e60\u4ea4\u6d41\u4f7f\u7528</p></body></html>", None))
        self.pushButton_help.setText(QCoreApplication.translate("MainWindow", u"\u4f7f\u7528\u5e2e\u52a9", None))
        self.pushButton_update.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u67e5\u66f4\u65b0", None))
        self.pushButton_disclaimer.setText(QCoreApplication.translate("MainWindow", u"\u514d\u8d23\u58f0\u660e", None))
        self.pushButton_about.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.pushButtom_title.setText(QCoreApplication.translate("MainWindow", u"\u5e7f\u897f\u79d1\u5e08\u6821\u56ed\u7f51\u767b\u5f55\u52a9\u624b", None))
        self.pushButton_minizing.setText("")
        self.pushButton_close.setText("")
        self.menulogMenu.setTitle(QCoreApplication.translate("MainWindow", u"logMenu", None))
    # retranslateUi

