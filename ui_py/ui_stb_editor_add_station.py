# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stb_editor_add_station.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QHBoxLayout, QHeaderView, QLineEdit,
    QPushButton, QSizePolicy, QTableView, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 350)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 0)
        self.searching_f = QFrame(Dialog)
        self.searching_f.setObjectName(u"searching_f")
        self.searching_f.setMinimumSize(QSize(0, 30))
        self.searching_f.setMaximumSize(QSize(16777215, 30))
        self.searching_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.searching_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.searching_f)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.searching_editor = QLineEdit(self.searching_f)
        self.searching_editor.setObjectName(u"searching_editor")

        self.horizontalLayout.addWidget(self.searching_editor)

        self.searching_b = QPushButton(self.searching_f)
        self.searching_b.setObjectName(u"searching_b")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searching_b.sizePolicy().hasHeightForWidth())
        self.searching_b.setSizePolicy(sizePolicy)
        self.searching_b.setMinimumSize(QSize(70, 0))
        self.searching_b.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout.addWidget(self.searching_b)


        self.verticalLayout.addWidget(self.searching_f)

        self.station_list = QTableView(Dialog)
        self.station_list.setObjectName(u"station_list")
        self.station_list.setFrameShape(QFrame.Shape.NoFrame)
        self.station_list.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout.addWidget(self.station_list)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(0, 40))
        self.buttonBox.setMaximumSize(QSize(16777215, 40))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.searching_b.setText(QCoreApplication.translate("Dialog", u"\u641c\u5c0b", None))
    # retranslateUi

