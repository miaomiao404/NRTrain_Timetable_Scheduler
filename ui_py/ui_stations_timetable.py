# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stations_timetable.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSplitter, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1200, 600)
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(0, 0, 1200, 600))
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.stations_facilities_list_f = QFrame(self.splitter)
        self.stations_facilities_list_f.setObjectName(u"stations_facilities_list_f")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stations_facilities_list_f.sizePolicy().hasHeightForWidth())
        self.stations_facilities_list_f.setSizePolicy(sizePolicy)
        self.stations_facilities_list_f.setMinimumSize(QSize(200, 0))
        self.stations_facilities_list_f.setMaximumSize(QSize(400, 16777215))
        self.stations_facilities_list_f.setFrameShape(QFrame.Shape.Box)
        self.stations_facilities_list_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.stations_facilities_list_f)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.searching_f_2 = QFrame(self.stations_facilities_list_f)
        self.searching_f_2.setObjectName(u"searching_f_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.searching_f_2.sizePolicy().hasHeightForWidth())
        self.searching_f_2.setSizePolicy(sizePolicy1)
        self.searching_f_2.setMinimumSize(QSize(0, 30))
        self.searching_f_2.setMaximumSize(QSize(16777215, 30))
        self.searching_f_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.searching_f_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.searching_f_2)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.searching_bar_2 = QLineEdit(self.searching_f_2)
        self.searching_bar_2.setObjectName(u"searching_bar_2")
        self.searching_bar_2.setMaxLength(200)

        self.horizontalLayout_3.addWidget(self.searching_bar_2)

        self.searching_b_2 = QPushButton(self.searching_f_2)
        self.searching_b_2.setObjectName(u"searching_b_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.searching_b_2.sizePolicy().hasHeightForWidth())
        self.searching_b_2.setSizePolicy(sizePolicy2)
        self.searching_b_2.setMinimumSize(QSize(40, 0))
        self.searching_b_2.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_3.addWidget(self.searching_b_2)


        self.verticalLayout_2.addWidget(self.searching_f_2)

        self.splitter_3 = QSplitter(self.stations_facilities_list_f)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Vertical)
        self.splitter_3.setChildrenCollapsible(False)
        self.stations_list_f_2 = QFrame(self.splitter_3)
        self.stations_list_f_2.setObjectName(u"stations_list_f_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(7)
        sizePolicy3.setHeightForWidth(self.stations_list_f_2.sizePolicy().hasHeightForWidth())
        self.stations_list_f_2.setSizePolicy(sizePolicy3)
        self.stations_list_f_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.stations_list_f_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.stations_list_f_2)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.stations_list_l_2 = QLabel(self.stations_list_f_2)
        self.stations_list_l_2.setObjectName(u"stations_list_l_2")
        self.stations_list_l_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.stations_list_l_2)

        self.stations_list_2 = QTableWidget(self.stations_list_f_2)
        self.stations_list_2.setObjectName(u"stations_list_2")
        self.stations_list_2.setFrameShape(QFrame.Shape.HLine)
        self.stations_list_2.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout_5.addWidget(self.stations_list_2)

        self.empty_frame_1 = QFrame(self.stations_list_f_2)
        self.empty_frame_1.setObjectName(u"empty_frame_1")
        sizePolicy1.setHeightForWidth(self.empty_frame_1.sizePolicy().hasHeightForWidth())
        self.empty_frame_1.setSizePolicy(sizePolicy1)
        self.empty_frame_1.setMinimumSize(QSize(0, 20))
        self.empty_frame_1.setMaximumSize(QSize(16777215, 20))
        self.empty_frame_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.empty_frame_1.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_5.addWidget(self.empty_frame_1)

        self.choose_direction = QTableWidget(self.stations_list_f_2)
        self.choose_direction.setObjectName(u"choose_direction")
        self.choose_direction.setMinimumSize(QSize(0, 60))
        self.choose_direction.setMaximumSize(QSize(16777215, 60))
        self.choose_direction.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_5.addWidget(self.choose_direction)

        self.splitter_3.addWidget(self.stations_list_f_2)

        self.verticalLayout_2.addWidget(self.splitter_3)

        self.splitter.addWidget(self.stations_facilities_list_f)
        self.main_timetable = QTableWidget(self.splitter)
        self.main_timetable.setObjectName(u"main_timetable")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(10)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.main_timetable.sizePolicy().hasHeightForWidth())
        self.main_timetable.setSizePolicy(sizePolicy4)
        self.main_timetable.setFrameShape(QFrame.Shape.NoFrame)
        self.splitter.addWidget(self.main_timetable)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.searching_b_2.setText(QCoreApplication.translate("Form", u"\u641c\u5c0b", None))
        self.stations_list_l_2.setText(QCoreApplication.translate("Form", u"\u8eca\u7ad9\u5217\u8868", None))
    # retranslateUi

