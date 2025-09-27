# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PswdInput.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractScrollArea, QApplication, QDialog,
    QDialogButtonBox, QFrame, QLabel, QLineEdit,
    QSizePolicy, QTextEdit, QWidget)
import window_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(400, 300)
        Dialog.setMaximumSize(QSize(400, 300))
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)
        self.label_QCimage = QLabel(Dialog)
        self.label_QCimage.setObjectName(u"label_QCimage")
        self.label_QCimage.setGeometry(QRect(155, 70, 90, 120))
        self.label_QCimage.setPixmap(QPixmap(u":/images/images/QC.jpg"))
        self.label_QCimage.setScaledContents(True)
        self.label_QCimage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_QCimage.setWordWrap(False)
        self.label_QCimage.setIndent(0)
        self.label_QCimage.setOpenExternalLinks(False)
        self.textEdit_tipText = QTextEdit(Dialog)
        self.textEdit_tipText.setObjectName(u"textEdit_tipText")
        self.textEdit_tipText.setEnabled(True)
        self.textEdit_tipText.setGeometry(QRect(50, 10, 300, 50))
        self.textEdit_tipText.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.textEdit_tipText.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit_tipText.setFrameShadow(QFrame.Shadow.Sunken)
        self.textEdit_tipText.setLineWidth(0)
        self.textEdit_tipText.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textEdit_tipText.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textEdit_tipText.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.textEdit_tipText.setTabChangesFocus(True)
        self.textEdit_tipText.setReadOnly(True)
        self.lineEdit_pswdInput = QLineEdit(Dialog)
        self.lineEdit_pswdInput.setObjectName(u"lineEdit_pswdInput")
        self.lineEdit_pswdInput.setGeometry(QRect(50, 200, 300, 20))
        self.lineEdit_pswdInput.setFrame(True)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u5bc6\u7801\u9a8c\u8bc1", None))
        self.label_QCimage.setText("")
        self.textEdit_tipText.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u8bf7\u8f93\u5165\u5bc6\u7801\u4ee5\u4f7f\u7528\u7a0b\u5e8f\uff0c\u5bc6\u7801\u8bf7\u4eceQQ\u9891\u9053\uff1a</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u5e7f\u79d1\u5e08\u9891\u9053\uff08\u9891\u9053\u53f7\uff1apd11040870\uff09\u7cbe\u534e\u5e16\u680f\u83b7\u53d6</p></body></html>", None))
        self.lineEdit_pswdInput.setInputMask("")
        self.lineEdit_pswdInput.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u8bf7\u8f93\u5165\u5bc6\u7801", None))
    # retranslateUi

