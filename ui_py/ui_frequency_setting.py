# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frequency_setting.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_frequency_setting(object):
    def setupUi(self, frequency_setting):
        if not frequency_setting.objectName():
            frequency_setting.setObjectName(u"frequency_setting")
        frequency_setting.resize(1001, 800)
        self.verticalLayout = QVBoxLayout(frequency_setting)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.line_name_l = QLabel(frequency_setting)
        self.line_name_l.setObjectName(u"line_name_l")
        self.line_name_l.setMinimumSize(QSize(0, 35))
        self.line_name_l.setMaximumSize(QSize(16777215, 35))
        self.line_name_l.setFrameShape(QFrame.Shape.NoFrame)
        self.line_name_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.line_name_l)

        self.setting_f = QFrame(frequency_setting)
        self.setting_f.setObjectName(u"setting_f")
        self.setting_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.setting_f.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.setting_f)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 5, 0, 5)
        self.weekdays_l = QLabel(self.setting_f)
        self.weekdays_l.setObjectName(u"weekdays_l")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.weekdays_l.sizePolicy().hasHeightForWidth())
        self.weekdays_l.setSizePolicy(sizePolicy)
        self.weekdays_l.setMinimumSize(QSize(0, 20))
        self.weekdays_l.setMaximumSize(QSize(16777215, 20))
        self.weekdays_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.weekdays_l, 0, 0, 1, 1)

        self.weekends_l = QLabel(self.setting_f)
        self.weekends_l.setObjectName(u"weekends_l")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.weekends_l.sizePolicy().hasHeightForWidth())
        self.weekends_l.setSizePolicy(sizePolicy1)
        self.weekends_l.setMinimumSize(QSize(0, 20))
        self.weekends_l.setMaximumSize(QSize(16777215, 20))
        self.weekends_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.weekends_l, 0, 1, 1, 1)

        self.weekdays_f = QFrame(self.setting_f)
        self.weekdays_f.setObjectName(u"weekdays_f")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(4)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.weekdays_f.sizePolicy().hasHeightForWidth())
        self.weekdays_f.setSizePolicy(sizePolicy2)
        self.weekdays_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.weekdays_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.weekdays_f)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.morning_peak_f = QFrame(self.weekdays_f)
        self.morning_peak_f.setObjectName(u"morning_peak_f")
        self.morning_peak_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.morning_peak_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.morning_peak_f)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.morning_peak_l = QLabel(self.morning_peak_f)
        self.morning_peak_l.setObjectName(u"morning_peak_l")
        self.morning_peak_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.morning_peak_l)

        self.cycle_f1 = QFrame(self.morning_peak_f)
        self.cycle_f1.setObjectName(u"cycle_f1")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cycle_f1.sizePolicy().hasHeightForWidth())
        self.cycle_f1.setSizePolicy(sizePolicy3)
        self.cycle_f1.setMinimumSize(QSize(0, 30))
        self.cycle_f1.setMaximumSize(QSize(16777215, 30))
        self.cycle_f1.setFrameShape(QFrame.Shape.StyledPanel)
        self.cycle_f1.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.cycle_f1)
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 2, 0, 2)
        self.cycle_l1 = QLabel(self.cycle_f1)
        self.cycle_l1.setObjectName(u"cycle_l1")

        self.horizontalLayout_3.addWidget(self.cycle_l1)

        self.cycle_b1 = QComboBox(self.cycle_f1)
        self.cycle_b1.setObjectName(u"cycle_b1")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.cycle_b1.sizePolicy().hasHeightForWidth())
        self.cycle_b1.setSizePolicy(sizePolicy4)

        self.horizontalLayout_3.addWidget(self.cycle_b1)


        self.verticalLayout_2.addWidget(self.cycle_f1)

        self.morning_peak_table_up = QTableWidget(self.morning_peak_f)
        self.morning_peak_table_up.setObjectName(u"morning_peak_table_up")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(3)
        sizePolicy5.setHeightForWidth(self.morning_peak_table_up.sizePolicy().hasHeightForWidth())
        self.morning_peak_table_up.setSizePolicy(sizePolicy5)
        self.morning_peak_table_up.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_2.addWidget(self.morning_peak_table_up)

        self.total_f1_up = QFrame(self.morning_peak_f)
        self.total_f1_up.setObjectName(u"total_f1_up")
        self.total_f1_up.setFrameShape(QFrame.Shape.StyledPanel)
        self.total_f1_up.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.total_f1_up)
        self.horizontalLayout_15.setSpacing(3)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(4, 4, 4, 4)
        self.total_l1_up = QLabel(self.total_f1_up)
        self.total_l1_up.setObjectName(u"total_l1_up")

        self.horizontalLayout_15.addWidget(self.total_l1_up)

        self.total_b1_up = QLineEdit(self.total_f1_up)
        self.total_b1_up.setObjectName(u"total_b1_up")
        self.total_b1_up.setFrame(False)
        self.total_b1_up.setReadOnly(True)

        self.horizontalLayout_15.addWidget(self.total_b1_up)


        self.verticalLayout_2.addWidget(self.total_f1_up)

        self.morning_peak_table_down = QTableWidget(self.morning_peak_f)
        self.morning_peak_table_down.setObjectName(u"morning_peak_table_down")
        sizePolicy5.setHeightForWidth(self.morning_peak_table_down.sizePolicy().hasHeightForWidth())
        self.morning_peak_table_down.setSizePolicy(sizePolicy5)
        self.morning_peak_table_down.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_2.addWidget(self.morning_peak_table_down)

        self.total_f1_down = QFrame(self.morning_peak_f)
        self.total_f1_down.setObjectName(u"total_f1_down")
        self.total_f1_down.setFrameShape(QFrame.Shape.StyledPanel)
        self.total_f1_down.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.total_f1_down)
        self.horizontalLayout_9.setSpacing(3)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(4, 4, 4, 4)
        self.total_l1_down = QLabel(self.total_f1_down)
        self.total_l1_down.setObjectName(u"total_l1_down")

        self.horizontalLayout_9.addWidget(self.total_l1_down)

        self.total_b1_down = QLineEdit(self.total_f1_down)
        self.total_b1_down.setObjectName(u"total_b1_down")
        self.total_b1_down.setFrame(False)
        self.total_b1_down.setReadOnly(True)

        self.horizontalLayout_9.addWidget(self.total_b1_down)


        self.verticalLayout_2.addWidget(self.total_f1_down)

        self.morning_peak_table_through = QTableWidget(self.morning_peak_f)
        self.morning_peak_table_through.setObjectName(u"morning_peak_table_through")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(2)
        sizePolicy6.setHeightForWidth(self.morning_peak_table_through.sizePolicy().hasHeightForWidth())
        self.morning_peak_table_through.setSizePolicy(sizePolicy6)
        self.morning_peak_table_through.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_2.addWidget(self.morning_peak_table_through)


        self.horizontalLayout.addWidget(self.morning_peak_f)

        self.nignt_peak_f = QFrame(self.weekdays_f)
        self.nignt_peak_f.setObjectName(u"nignt_peak_f")
        self.nignt_peak_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.nignt_peak_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.nignt_peak_f)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.night_peak_l = QLabel(self.nignt_peak_f)
        self.night_peak_l.setObjectName(u"night_peak_l")
        self.night_peak_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.night_peak_l)

        self.cycle_f1_2 = QFrame(self.nignt_peak_f)
        self.cycle_f1_2.setObjectName(u"cycle_f1_2")
        sizePolicy3.setHeightForWidth(self.cycle_f1_2.sizePolicy().hasHeightForWidth())
        self.cycle_f1_2.setSizePolicy(sizePolicy3)
        self.cycle_f1_2.setMinimumSize(QSize(0, 30))
        self.cycle_f1_2.setMaximumSize(QSize(16777215, 30))
        self.cycle_f1_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.cycle_f1_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.cycle_f1_2)
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 2, 0, 2)
        self.cycle_l1_2 = QLabel(self.cycle_f1_2)
        self.cycle_l1_2.setObjectName(u"cycle_l1_2")

        self.horizontalLayout_4.addWidget(self.cycle_l1_2)

        self.cycle_b1_2 = QComboBox(self.cycle_f1_2)
        self.cycle_b1_2.setObjectName(u"cycle_b1_2")
        sizePolicy4.setHeightForWidth(self.cycle_b1_2.sizePolicy().hasHeightForWidth())
        self.cycle_b1_2.setSizePolicy(sizePolicy4)

        self.horizontalLayout_4.addWidget(self.cycle_b1_2)


        self.verticalLayout_3.addWidget(self.cycle_f1_2)

        self.night_peak_table_up = QTableWidget(self.nignt_peak_f)
        self.night_peak_table_up.setObjectName(u"night_peak_table_up")
        sizePolicy5.setHeightForWidth(self.night_peak_table_up.sizePolicy().hasHeightForWidth())
        self.night_peak_table_up.setSizePolicy(sizePolicy5)
        self.night_peak_table_up.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_3.addWidget(self.night_peak_table_up)

        self.total_f2_up = QFrame(self.nignt_peak_f)
        self.total_f2_up.setObjectName(u"total_f2_up")
        self.total_f2_up.setFrameShape(QFrame.Shape.StyledPanel)
        self.total_f2_up.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.total_f2_up)
        self.horizontalLayout_16.setSpacing(3)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(4, 4, 4, 4)
        self.total_l2_up = QLabel(self.total_f2_up)
        self.total_l2_up.setObjectName(u"total_l2_up")

        self.horizontalLayout_16.addWidget(self.total_l2_up)

        self.total_b2 = QLineEdit(self.total_f2_up)
        self.total_b2.setObjectName(u"total_b2")
        self.total_b2.setFrame(False)
        self.total_b2.setReadOnly(True)

        self.horizontalLayout_16.addWidget(self.total_b2)


        self.verticalLayout_3.addWidget(self.total_f2_up)

        self.night_peak_table_down = QTableWidget(self.nignt_peak_f)
        self.night_peak_table_down.setObjectName(u"night_peak_table_down")
        sizePolicy5.setHeightForWidth(self.night_peak_table_down.sizePolicy().hasHeightForWidth())
        self.night_peak_table_down.setSizePolicy(sizePolicy5)
        self.night_peak_table_down.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_3.addWidget(self.night_peak_table_down)

        self.total_f2_down = QFrame(self.nignt_peak_f)
        self.total_f2_down.setObjectName(u"total_f2_down")
        self.total_f2_down.setFrameShape(QFrame.Shape.StyledPanel)
        self.total_f2_down.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.total_f2_down)
        self.horizontalLayout_10.setSpacing(3)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(4, 4, 4, 4)
        self.total_l2_down = QLabel(self.total_f2_down)
        self.total_l2_down.setObjectName(u"total_l2_down")

        self.horizontalLayout_10.addWidget(self.total_l2_down)

        self.total_b2_down = QLineEdit(self.total_f2_down)
        self.total_b2_down.setObjectName(u"total_b2_down")
        self.total_b2_down.setFrame(False)
        self.total_b2_down.setReadOnly(True)

        self.horizontalLayout_10.addWidget(self.total_b2_down)


        self.verticalLayout_3.addWidget(self.total_f2_down)

        self.night_peak_table_through = QTableWidget(self.nignt_peak_f)
        self.night_peak_table_through.setObjectName(u"night_peak_table_through")
        sizePolicy6.setHeightForWidth(self.night_peak_table_through.sizePolicy().hasHeightForWidth())
        self.night_peak_table_through.setSizePolicy(sizePolicy6)
        self.night_peak_table_through.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_3.addWidget(self.night_peak_table_through)


        self.horizontalLayout.addWidget(self.nignt_peak_f)

        self.weekdays_off_peak_f = QFrame(self.weekdays_f)
        self.weekdays_off_peak_f.setObjectName(u"weekdays_off_peak_f")
        self.weekdays_off_peak_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.weekdays_off_peak_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.weekdays_off_peak_f)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.weekdays_off_peak_l = QLabel(self.weekdays_off_peak_f)
        self.weekdays_off_peak_l.setObjectName(u"weekdays_off_peak_l")
        self.weekdays_off_peak_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.weekdays_off_peak_l)

        self.cycle_f1_3 = QFrame(self.weekdays_off_peak_f)
        self.cycle_f1_3.setObjectName(u"cycle_f1_3")
        sizePolicy3.setHeightForWidth(self.cycle_f1_3.sizePolicy().hasHeightForWidth())
        self.cycle_f1_3.setSizePolicy(sizePolicy3)
        self.cycle_f1_3.setMinimumSize(QSize(0, 30))
        self.cycle_f1_3.setMaximumSize(QSize(16777215, 30))
        self.cycle_f1_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.cycle_f1_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.cycle_f1_3)
        self.horizontalLayout_5.setSpacing(3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 2, 0, 2)
        self.cycle_l1_3 = QLabel(self.cycle_f1_3)
        self.cycle_l1_3.setObjectName(u"cycle_l1_3")

        self.horizontalLayout_5.addWidget(self.cycle_l1_3)

        self.cycle_b1_3 = QComboBox(self.cycle_f1_3)
        self.cycle_b1_3.setObjectName(u"cycle_b1_3")
        sizePolicy4.setHeightForWidth(self.cycle_b1_3.sizePolicy().hasHeightForWidth())
        self.cycle_b1_3.setSizePolicy(sizePolicy4)

        self.horizontalLayout_5.addWidget(self.cycle_b1_3)


        self.verticalLayout_4.addWidget(self.cycle_f1_3)

        self.weekdays_off_peak_table_up = QTableWidget(self.weekdays_off_peak_f)
        self.weekdays_off_peak_table_up.setObjectName(u"weekdays_off_peak_table_up")
        sizePolicy5.setHeightForWidth(self.weekdays_off_peak_table_up.sizePolicy().hasHeightForWidth())
        self.weekdays_off_peak_table_up.setSizePolicy(sizePolicy5)
        self.weekdays_off_peak_table_up.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_4.addWidget(self.weekdays_off_peak_table_up)

        self.total_f3_up = QFrame(self.weekdays_off_peak_f)
        self.total_f3_up.setObjectName(u"total_f3_up")
        self.total_f3_up.setFrameShape(QFrame.Shape.StyledPanel)
        self.total_f3_up.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.total_f3_up)
        self.horizontalLayout_17.setSpacing(3)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(4, 4, 4, 4)
        self.total_l3_up = QLabel(self.total_f3_up)
        self.total_l3_up.setObjectName(u"total_l3_up")

        self.horizontalLayout_17.addWidget(self.total_l3_up)

        self.total_b3_up = QLineEdit(self.total_f3_up)
        self.total_b3_up.setObjectName(u"total_b3_up")
        self.total_b3_up.setFrame(False)
        self.total_b3_up.setReadOnly(True)

        self.horizontalLayout_17.addWidget(self.total_b3_up)


        self.verticalLayout_4.addWidget(self.total_f3_up)

        self.weekdays_off_peak_table_down = QTableWidget(self.weekdays_off_peak_f)
        self.weekdays_off_peak_table_down.setObjectName(u"weekdays_off_peak_table_down")
        sizePolicy5.setHeightForWidth(self.weekdays_off_peak_table_down.sizePolicy().hasHeightForWidth())
        self.weekdays_off_peak_table_down.setSizePolicy(sizePolicy5)
        self.weekdays_off_peak_table_down.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_4.addWidget(self.weekdays_off_peak_table_down)

        self.total_f3_down = QFrame(self.weekdays_off_peak_f)
        self.total_f3_down.setObjectName(u"total_f3_down")
        self.total_f3_down.setFrameShape(QFrame.Shape.StyledPanel)
        self.total_f3_down.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.total_f3_down)
        self.horizontalLayout_11.setSpacing(3)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(4, 4, 4, 4)
        self.total_l3_down = QLabel(self.total_f3_down)
        self.total_l3_down.setObjectName(u"total_l3_down")

        self.horizontalLayout_11.addWidget(self.total_l3_down)

        self.total_b3_down = QLineEdit(self.total_f3_down)
        self.total_b3_down.setObjectName(u"total_b3_down")
        self.total_b3_down.setFrame(False)
        self.total_b3_down.setReadOnly(True)

        self.horizontalLayout_11.addWidget(self.total_b3_down)


        self.verticalLayout_4.addWidget(self.total_f3_down)

        self.weekdays_off_peak_table_through = QTableWidget(self.weekdays_off_peak_f)
        self.weekdays_off_peak_table_through.setObjectName(u"weekdays_off_peak_table_through")
        sizePolicy6.setHeightForWidth(self.weekdays_off_peak_table_through.sizePolicy().hasHeightForWidth())
        self.weekdays_off_peak_table_through.setSizePolicy(sizePolicy6)
        self.weekdays_off_peak_table_through.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_4.addWidget(self.weekdays_off_peak_table_through)


        self.horizontalLayout.addWidget(self.weekdays_off_peak_f)

        self.weekdays_late_night_f = QFrame(self.weekdays_f)
        self.weekdays_late_night_f.setObjectName(u"weekdays_late_night_f")
        self.weekdays_late_night_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.weekdays_late_night_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.weekdays_late_night_f)
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(4, 4, 4, 4)
        self.weekdays_late_night_l = QLabel(self.weekdays_late_night_f)
        self.weekdays_late_night_l.setObjectName(u"weekdays_late_night_l")
        self.weekdays_late_night_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.weekdays_late_night_l)

        self.cycle_f1_4 = QFrame(self.weekdays_late_night_f)
        self.cycle_f1_4.setObjectName(u"cycle_f1_4")
        sizePolicy3.setHeightForWidth(self.cycle_f1_4.sizePolicy().hasHeightForWidth())
        self.cycle_f1_4.setSizePolicy(sizePolicy3)
        self.cycle_f1_4.setMinimumSize(QSize(0, 30))
        self.cycle_f1_4.setMaximumSize(QSize(16777215, 30))
        self.cycle_f1_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.cycle_f1_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.cycle_f1_4)
        self.horizontalLayout_6.setSpacing(3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 2, 0, 2)
        self.cycle_l1_4 = QLabel(self.cycle_f1_4)
        self.cycle_l1_4.setObjectName(u"cycle_l1_4")

        self.horizontalLayout_6.addWidget(self.cycle_l1_4)

        self.cycle_b1_4 = QComboBox(self.cycle_f1_4)
        self.cycle_b1_4.setObjectName(u"cycle_b1_4")
        sizePolicy4.setHeightForWidth(self.cycle_b1_4.sizePolicy().hasHeightForWidth())
        self.cycle_b1_4.setSizePolicy(sizePolicy4)

        self.horizontalLayout_6.addWidget(self.cycle_b1_4)


        self.verticalLayout_5.addWidget(self.cycle_f1_4)

        self.weekdays_late_night_table_up = QTableWidget(self.weekdays_late_night_f)
        self.weekdays_late_night_table_up.setObjectName(u"weekdays_late_night_table_up")
        sizePolicy5.setHeightForWidth(self.weekdays_late_night_table_up.sizePolicy().hasHeightForWidth())
        self.weekdays_late_night_table_up.setSizePolicy(sizePolicy5)
        self.weekdays_late_night_table_up.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_5.addWidget(self.weekdays_late_night_table_up)

        self.total_f4_up = QFrame(self.weekdays_late_night_f)
        self.total_f4_up.setObjectName(u"total_f4_up")
        self.total_f4_up.setFrameShape(QFrame.Shape.StyledPanel)
        self.total_f4_up.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.total_f4_up)
        self.horizontalLayout_18.setSpacing(3)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(4, 4, 4, 4)
        self.total_l4_up = QLabel(self.total_f4_up)
        self.total_l4_up.setObjectName(u"total_l4_up")

        self.horizontalLayout_18.addWidget(self.total_l4_up)

        self.total_b4_up = QLineEdit(self.total_f4_up)
        self.total_b4_up.setObjectName(u"total_b4_up")
        self.total_b4_up.setFrame(False)
        self.total_b4_up.setReadOnly(True)

        self.horizontalLayout_18.addWidget(self.total_b4_up)


        self.verticalLayout_5.addWidget(self.total_f4_up)

        self.weekdays_late_night_table_down = QTableWidget(self.weekdays_late_night_f)
        self.weekdays_late_night_table_down.setObjectName(u"weekdays_late_night_table_down")
        sizePolicy5.setHeightForWidth(self.weekdays_late_night_table_down.sizePolicy().hasHeightForWidth())
        self.weekdays_late_night_table_down.setSizePolicy(sizePolicy5)
        self.weekdays_late_night_table_down.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_5.addWidget(self.weekdays_late_night_table_down)

        self.total_f4_down = QFrame(self.weekdays_late_night_f)
        self.total_f4_down.setObjectName(u"total_f4_down")
        self.total_f4_down.setFrameShape(QFrame.Shape.StyledPanel)
        self.total_f4_down.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.total_f4_down)
        self.horizontalLayout_12.setSpacing(3)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(4, 4, 4, 4)
        self.total_l4_down = QLabel(self.total_f4_down)
        self.total_l4_down.setObjectName(u"total_l4_down")

        self.horizontalLayout_12.addWidget(self.total_l4_down)

        self.total_b4_down = QLineEdit(self.total_f4_down)
        self.total_b4_down.setObjectName(u"total_b4_down")
        self.total_b4_down.setFrame(False)
        self.total_b4_down.setReadOnly(True)

        self.horizontalLayout_12.addWidget(self.total_b4_down)


        self.verticalLayout_5.addWidget(self.total_f4_down)

        self.weekdays_late_night_table_through = QTableWidget(self.weekdays_late_night_f)
        self.weekdays_late_night_table_through.setObjectName(u"weekdays_late_night_table_through")
        sizePolicy6.setHeightForWidth(self.weekdays_late_night_table_through.sizePolicy().hasHeightForWidth())
        self.weekdays_late_night_table_through.setSizePolicy(sizePolicy6)
        self.weekdays_late_night_table_through.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_5.addWidget(self.weekdays_late_night_table_through)


        self.horizontalLayout.addWidget(self.weekdays_late_night_f)


        self.gridLayout.addWidget(self.weekdays_f, 1, 0, 1, 1)

        self.weekends_f = QFrame(self.setting_f)
        self.weekends_f.setObjectName(u"weekends_f")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(2)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.weekends_f.sizePolicy().hasHeightForWidth())
        self.weekends_f.setSizePolicy(sizePolicy7)
        self.weekends_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.weekends_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.weekends_f)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.weekends_off_peak_f = QFrame(self.weekends_f)
        self.weekends_off_peak_f.setObjectName(u"weekends_off_peak_f")
        self.weekends_off_peak_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.weekends_off_peak_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.weekends_off_peak_f)
        self.verticalLayout_6.setSpacing(2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(4, 4, 4, 4)
        self.weekends_off_peak_l = QLabel(self.weekends_off_peak_f)
        self.weekends_off_peak_l.setObjectName(u"weekends_off_peak_l")
        self.weekends_off_peak_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.weekends_off_peak_l)

        self.cycle_f1_5 = QFrame(self.weekends_off_peak_f)
        self.cycle_f1_5.setObjectName(u"cycle_f1_5")
        sizePolicy3.setHeightForWidth(self.cycle_f1_5.sizePolicy().hasHeightForWidth())
        self.cycle_f1_5.setSizePolicy(sizePolicy3)
        self.cycle_f1_5.setMinimumSize(QSize(0, 30))
        self.cycle_f1_5.setMaximumSize(QSize(16777215, 30))
        self.cycle_f1_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.cycle_f1_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.cycle_f1_5)
        self.horizontalLayout_7.setSpacing(3)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 2, 0, 2)
        self.cycle_l1_5 = QLabel(self.cycle_f1_5)
        self.cycle_l1_5.setObjectName(u"cycle_l1_5")

        self.horizontalLayout_7.addWidget(self.cycle_l1_5)

        self.cycle_b1_5 = QComboBox(self.cycle_f1_5)
        self.cycle_b1_5.setObjectName(u"cycle_b1_5")
        sizePolicy4.setHeightForWidth(self.cycle_b1_5.sizePolicy().hasHeightForWidth())
        self.cycle_b1_5.setSizePolicy(sizePolicy4)

        self.horizontalLayout_7.addWidget(self.cycle_b1_5)


        self.verticalLayout_6.addWidget(self.cycle_f1_5)

        self.weekends_off_peak_table_up = QTableWidget(self.weekends_off_peak_f)
        self.weekends_off_peak_table_up.setObjectName(u"weekends_off_peak_table_up")
        sizePolicy5.setHeightForWidth(self.weekends_off_peak_table_up.sizePolicy().hasHeightForWidth())
        self.weekends_off_peak_table_up.setSizePolicy(sizePolicy5)
        self.weekends_off_peak_table_up.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_6.addWidget(self.weekends_off_peak_table_up)

        self.total_f5_up = QFrame(self.weekends_off_peak_f)
        self.total_f5_up.setObjectName(u"total_f5_up")
        self.total_f5_up.setFrameShape(QFrame.Shape.StyledPanel)
        self.total_f5_up.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.total_f5_up)
        self.horizontalLayout_19.setSpacing(3)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(4, 4, 4, 4)
        self.total_l5_up = QLabel(self.total_f5_up)
        self.total_l5_up.setObjectName(u"total_l5_up")

        self.horizontalLayout_19.addWidget(self.total_l5_up)

        self.total_b5_up = QLineEdit(self.total_f5_up)
        self.total_b5_up.setObjectName(u"total_b5_up")
        self.total_b5_up.setFrame(False)
        self.total_b5_up.setReadOnly(True)

        self.horizontalLayout_19.addWidget(self.total_b5_up)


        self.verticalLayout_6.addWidget(self.total_f5_up)

        self.weekends_off_peak_table_down = QTableWidget(self.weekends_off_peak_f)
        self.weekends_off_peak_table_down.setObjectName(u"weekends_off_peak_table_down")
        sizePolicy5.setHeightForWidth(self.weekends_off_peak_table_down.sizePolicy().hasHeightForWidth())
        self.weekends_off_peak_table_down.setSizePolicy(sizePolicy5)
        self.weekends_off_peak_table_down.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_6.addWidget(self.weekends_off_peak_table_down)

        self.total_f5_down = QFrame(self.weekends_off_peak_f)
        self.total_f5_down.setObjectName(u"total_f5_down")
        self.total_f5_down.setFrameShape(QFrame.Shape.StyledPanel)
        self.total_f5_down.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.total_f5_down)
        self.horizontalLayout_13.setSpacing(3)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(4, 4, 4, 4)
        self.total_l5_down = QLabel(self.total_f5_down)
        self.total_l5_down.setObjectName(u"total_l5_down")

        self.horizontalLayout_13.addWidget(self.total_l5_down)

        self.total_b5_down = QLineEdit(self.total_f5_down)
        self.total_b5_down.setObjectName(u"total_b5_down")
        self.total_b5_down.setFrame(False)
        self.total_b5_down.setReadOnly(True)

        self.horizontalLayout_13.addWidget(self.total_b5_down)


        self.verticalLayout_6.addWidget(self.total_f5_down)

        self.weekends_off_peak_table_through = QTableWidget(self.weekends_off_peak_f)
        self.weekends_off_peak_table_through.setObjectName(u"weekends_off_peak_table_through")
        sizePolicy6.setHeightForWidth(self.weekends_off_peak_table_through.sizePolicy().hasHeightForWidth())
        self.weekends_off_peak_table_through.setSizePolicy(sizePolicy6)
        self.weekends_off_peak_table_through.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_6.addWidget(self.weekends_off_peak_table_through)


        self.horizontalLayout_2.addWidget(self.weekends_off_peak_f)

        self.weekends_late_night_f = QFrame(self.weekends_f)
        self.weekends_late_night_f.setObjectName(u"weekends_late_night_f")
        self.weekends_late_night_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.weekends_late_night_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.weekends_late_night_f)
        self.verticalLayout_7.setSpacing(2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(4, 4, 4, 4)
        self.weekends_late_night_l = QLabel(self.weekends_late_night_f)
        self.weekends_late_night_l.setObjectName(u"weekends_late_night_l")
        self.weekends_late_night_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.weekends_late_night_l)

        self.cycle_f1_6 = QFrame(self.weekends_late_night_f)
        self.cycle_f1_6.setObjectName(u"cycle_f1_6")
        sizePolicy3.setHeightForWidth(self.cycle_f1_6.sizePolicy().hasHeightForWidth())
        self.cycle_f1_6.setSizePolicy(sizePolicy3)
        self.cycle_f1_6.setMinimumSize(QSize(0, 30))
        self.cycle_f1_6.setMaximumSize(QSize(16777215, 30))
        self.cycle_f1_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.cycle_f1_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.cycle_f1_6)
        self.horizontalLayout_8.setSpacing(3)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 2, 0, 2)
        self.cycle_l1_6 = QLabel(self.cycle_f1_6)
        self.cycle_l1_6.setObjectName(u"cycle_l1_6")

        self.horizontalLayout_8.addWidget(self.cycle_l1_6)

        self.cycle_b1_6 = QComboBox(self.cycle_f1_6)
        self.cycle_b1_6.setObjectName(u"cycle_b1_6")
        sizePolicy4.setHeightForWidth(self.cycle_b1_6.sizePolicy().hasHeightForWidth())
        self.cycle_b1_6.setSizePolicy(sizePolicy4)

        self.horizontalLayout_8.addWidget(self.cycle_b1_6)


        self.verticalLayout_7.addWidget(self.cycle_f1_6)

        self.weekends_late_night_table_up = QTableWidget(self.weekends_late_night_f)
        self.weekends_late_night_table_up.setObjectName(u"weekends_late_night_table_up")
        sizePolicy5.setHeightForWidth(self.weekends_late_night_table_up.sizePolicy().hasHeightForWidth())
        self.weekends_late_night_table_up.setSizePolicy(sizePolicy5)
        self.weekends_late_night_table_up.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_7.addWidget(self.weekends_late_night_table_up)

        self.total_f6_up = QFrame(self.weekends_late_night_f)
        self.total_f6_up.setObjectName(u"total_f6_up")
        self.total_f6_up.setFrameShape(QFrame.Shape.StyledPanel)
        self.total_f6_up.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.total_f6_up)
        self.horizontalLayout_20.setSpacing(3)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(4, 4, 4, 4)
        self.total_l6_up = QLabel(self.total_f6_up)
        self.total_l6_up.setObjectName(u"total_l6_up")

        self.horizontalLayout_20.addWidget(self.total_l6_up)

        self.total_b6_up = QLineEdit(self.total_f6_up)
        self.total_b6_up.setObjectName(u"total_b6_up")
        self.total_b6_up.setFrame(False)
        self.total_b6_up.setReadOnly(True)

        self.horizontalLayout_20.addWidget(self.total_b6_up)


        self.verticalLayout_7.addWidget(self.total_f6_up)

        self.weekends_late_night_table_down = QTableWidget(self.weekends_late_night_f)
        self.weekends_late_night_table_down.setObjectName(u"weekends_late_night_table_down")
        sizePolicy5.setHeightForWidth(self.weekends_late_night_table_down.sizePolicy().hasHeightForWidth())
        self.weekends_late_night_table_down.setSizePolicy(sizePolicy5)
        self.weekends_late_night_table_down.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_7.addWidget(self.weekends_late_night_table_down)

        self.total_f6_down = QFrame(self.weekends_late_night_f)
        self.total_f6_down.setObjectName(u"total_f6_down")
        self.total_f6_down.setFrameShape(QFrame.Shape.StyledPanel)
        self.total_f6_down.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.total_f6_down)
        self.horizontalLayout_14.setSpacing(3)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(4, 4, 4, 4)
        self.total_l6_down = QLabel(self.total_f6_down)
        self.total_l6_down.setObjectName(u"total_l6_down")

        self.horizontalLayout_14.addWidget(self.total_l6_down)

        self.total_b6_down = QLineEdit(self.total_f6_down)
        self.total_b6_down.setObjectName(u"total_b6_down")
        self.total_b6_down.setFrame(False)
        self.total_b6_down.setReadOnly(True)

        self.horizontalLayout_14.addWidget(self.total_b6_down)


        self.verticalLayout_7.addWidget(self.total_f6_down)

        self.weekends_late_night_table_through = QTableWidget(self.weekends_late_night_f)
        self.weekends_late_night_table_through.setObjectName(u"weekends_late_night_table_through")
        sizePolicy6.setHeightForWidth(self.weekends_late_night_table_through.sizePolicy().hasHeightForWidth())
        self.weekends_late_night_table_through.setSizePolicy(sizePolicy6)
        self.weekends_late_night_table_through.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_7.addWidget(self.weekends_late_night_table_through)


        self.horizontalLayout_2.addWidget(self.weekends_late_night_f)


        self.gridLayout.addWidget(self.weekends_f, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.setting_f)


        self.retranslateUi(frequency_setting)

        QMetaObject.connectSlotsByName(frequency_setting)
    # setupUi

    def retranslateUi(self, frequency_setting):
        frequency_setting.setWindowTitle(QCoreApplication.translate("frequency_setting", u"Form", None))
        self.line_name_l.setText(QCoreApplication.translate("frequency_setting", u"line \u767c\u8eca\u983b\u7387\u8a2d\u5b9a", None))
        self.weekdays_l.setText(QCoreApplication.translate("frequency_setting", u"  \u5e73\u65e5", None))
        self.weekends_l.setText(QCoreApplication.translate("frequency_setting", u"  \u5047\u65e5", None))
        self.morning_peak_l.setText(QCoreApplication.translate("frequency_setting", u"\u65e9\u5c16\u5cf0\u6642\u6bb5(7:00~9:00)", None))
        self.cycle_l1.setText(QCoreApplication.translate("frequency_setting", u"\u5faa\u74b0\u6642\u9593", None))
        self.total_l1_up.setText(QCoreApplication.translate("frequency_setting", u"\u6bcf\u5c0f\u6642\u767c\u8eca\u6578:", None))
        self.total_l1_down.setText(QCoreApplication.translate("frequency_setting", u"\u6bcf\u5c0f\u6642\u767c\u8eca\u6578:", None))
        self.night_peak_l.setText(QCoreApplication.translate("frequency_setting", u"\u665a\u5c16\u5cf0\u6642\u6bb5(5:00~8:00)", None))
        self.cycle_l1_2.setText(QCoreApplication.translate("frequency_setting", u"\u5faa\u74b0\u6642\u9593", None))
        self.total_l2_up.setText(QCoreApplication.translate("frequency_setting", u"\u6bcf\u5c0f\u6642\u767c\u8eca\u6578:", None))
        self.total_l2_down.setText(QCoreApplication.translate("frequency_setting", u"\u6bcf\u5c0f\u6642\u767c\u8eca\u6578:", None))
        self.weekdays_off_peak_l.setText(QCoreApplication.translate("frequency_setting", u"\u96e2\u5cf0\u6642\u6bb5", None))
        self.cycle_l1_3.setText(QCoreApplication.translate("frequency_setting", u"\u5faa\u74b0\u6642\u9593", None))
        self.total_l3_up.setText(QCoreApplication.translate("frequency_setting", u"\u6bcf\u5c0f\u6642\u767c\u8eca\u6578:", None))
        self.total_l3_down.setText(QCoreApplication.translate("frequency_setting", u"\u6bcf\u5c0f\u6642\u767c\u8eca\u6578:", None))
        self.weekdays_late_night_l.setText(QCoreApplication.translate("frequency_setting", u"\u6df1\u591c\u6642\u6bb5(11:00~)", None))
        self.cycle_l1_4.setText(QCoreApplication.translate("frequency_setting", u"\u5faa\u74b0\u6642\u9593", None))
        self.total_l4_up.setText(QCoreApplication.translate("frequency_setting", u"\u6bcf\u5c0f\u6642\u767c\u8eca\u6578:", None))
        self.total_l4_down.setText(QCoreApplication.translate("frequency_setting", u"\u6bcf\u5c0f\u6642\u767c\u8eca\u6578:", None))
        self.weekends_off_peak_l.setText(QCoreApplication.translate("frequency_setting", u"\u96e2\u5cf0\u6642\u6bb5", None))
        self.cycle_l1_5.setText(QCoreApplication.translate("frequency_setting", u"\u5faa\u74b0\u6642\u9593", None))
        self.total_l5_up.setText(QCoreApplication.translate("frequency_setting", u"\u6bcf\u5c0f\u6642\u767c\u8eca\u6578:", None))
        self.total_l5_down.setText(QCoreApplication.translate("frequency_setting", u"\u6bcf\u5c0f\u6642\u767c\u8eca\u6578:", None))
        self.weekends_late_night_l.setText(QCoreApplication.translate("frequency_setting", u"\u6df1\u591c\u6642\u6bb5(11:00~)", None))
        self.cycle_l1_6.setText(QCoreApplication.translate("frequency_setting", u"\u5faa\u74b0\u6642\u9593", None))
        self.total_l6_up.setText(QCoreApplication.translate("frequency_setting", u"\u6bcf\u5c0f\u6642\u767c\u8eca\u6578:", None))
        self.total_l6_down.setText(QCoreApplication.translate("frequency_setting", u"\u6bcf\u5c0f\u6642\u767c\u8eca\u6578:", None))
    # retranslateUi

