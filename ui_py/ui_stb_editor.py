# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stb_editor.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_STB_Widget(object):
    def setupUi(self, STB_Widget):
        if not STB_Widget.objectName():
            STB_Widget.setObjectName(u"STB_Widget")
        STB_Widget.resize(525, 352)
        self.verticalLayout = QVBoxLayout(STB_Widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.upper_frame = QFrame(STB_Widget)
        self.upper_frame.setObjectName(u"upper_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upper_frame.sizePolicy().hasHeightForWidth())
        self.upper_frame.setSizePolicy(sizePolicy)
        self.upper_frame.setMinimumSize(QSize(0, 40))
        self.upper_frame.setMaximumSize(QSize(16777215, 40))
        self.upper_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.upper_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.upper_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.add_station_b = QPushButton(self.upper_frame)
        self.add_station_b.setObjectName(u"add_station_b")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.add_station_b.sizePolicy().hasHeightForWidth())
        self.add_station_b.setSizePolicy(sizePolicy1)
        self.add_station_b.setMinimumSize(QSize(80, 0))
        self.add_station_b.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.add_station_b)

        self.move_up_b = QPushButton(self.upper_frame)
        self.move_up_b.setObjectName(u"move_up_b")
        sizePolicy1.setHeightForWidth(self.move_up_b.sizePolicy().hasHeightForWidth())
        self.move_up_b.setSizePolicy(sizePolicy1)
        self.move_up_b.setMinimumSize(QSize(20, 20))
        self.move_up_b.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.move_up_b)

        self.move_down_b = QPushButton(self.upper_frame)
        self.move_down_b.setObjectName(u"move_down_b")
        sizePolicy1.setHeightForWidth(self.move_down_b.sizePolicy().hasHeightForWidth())
        self.move_down_b.setSizePolicy(sizePolicy1)
        self.move_down_b.setMinimumSize(QSize(20, 20))
        self.move_down_b.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.move_down_b)

        self.move_left_b = QPushButton(self.upper_frame)
        self.move_left_b.setObjectName(u"move_left_b")
        sizePolicy1.setHeightForWidth(self.move_left_b.sizePolicy().hasHeightForWidth())
        self.move_left_b.setSizePolicy(sizePolicy1)
        self.move_left_b.setMinimumSize(QSize(20, 20))
        self.move_left_b.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.move_left_b)

        self.move_right_b = QPushButton(self.upper_frame)
        self.move_right_b.setObjectName(u"move_right_b")
        sizePolicy1.setHeightForWidth(self.move_right_b.sizePolicy().hasHeightForWidth())
        self.move_right_b.setSizePolicy(sizePolicy1)
        self.move_right_b.setMinimumSize(QSize(20, 20))
        self.move_right_b.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.move_right_b)

        self.delete_b = QPushButton(self.upper_frame)
        self.delete_b.setObjectName(u"delete_b")
        sizePolicy1.setHeightForWidth(self.delete_b.sizePolicy().hasHeightForWidth())
        self.delete_b.setSizePolicy(sizePolicy1)
        self.delete_b.setMinimumSize(QSize(20, 20))
        self.delete_b.setMaximumSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.delete_b)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.upper_frame)

        self.main_table = QTableWidget(STB_Widget)
        self.main_table.setObjectName(u"main_table")
        self.main_table.setAlternatingRowColors(True)

        self.verticalLayout.addWidget(self.main_table)


        self.retranslateUi(STB_Widget)

        QMetaObject.connectSlotsByName(STB_Widget)
    # setupUi

    def retranslateUi(self, STB_Widget):
        STB_Widget.setWindowTitle(QCoreApplication.translate("STB_Widget", u"Form", None))
#if QT_CONFIG(tooltip)
        self.add_station_b.setToolTip(QCoreApplication.translate("STB_Widget", u"\u65b0\u589e\u8eca\u7ad9", None))
#endif // QT_CONFIG(tooltip)
        self.add_station_b.setText(QCoreApplication.translate("STB_Widget", u"\u65b0\u589e\u8eca\u7ad9", None))
#if QT_CONFIG(tooltip)
        self.move_up_b.setToolTip(QCoreApplication.translate("STB_Widget", u"\u4e0a\u79fb", None))
#endif // QT_CONFIG(tooltip)
        self.move_up_b.setText("")
#if QT_CONFIG(tooltip)
        self.move_down_b.setToolTip(QCoreApplication.translate("STB_Widget", u"\u4e0b\u79fb", None))
#endif // QT_CONFIG(tooltip)
        self.move_down_b.setText("")
#if QT_CONFIG(tooltip)
        self.move_left_b.setToolTip(QCoreApplication.translate("STB_Widget", u"\u5de6\u79fb", None))
#endif // QT_CONFIG(tooltip)
        self.move_left_b.setText("")
#if QT_CONFIG(tooltip)
        self.move_right_b.setToolTip(QCoreApplication.translate("STB_Widget", u"\u53f3\u79fb", None))
#endif // QT_CONFIG(tooltip)
        self.move_right_b.setText("")
#if QT_CONFIG(tooltip)
        self.delete_b.setToolTip(QCoreApplication.translate("STB_Widget", u"\u522a\u9664", None))
#endif // QT_CONFIG(tooltip)
        self.delete_b.setText("")
    # retranslateUi

