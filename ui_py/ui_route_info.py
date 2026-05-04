# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'route_info.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDateTimeEdit,
    QDialog, QDialogButtonBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTimeEdit, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 470)
        Dialog.setMinimumSize(QSize(400, 470))
        Dialog.setMaximumSize(QSize(416, 470))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.blank_1 = QFrame(Dialog)
        self.blank_1.setObjectName(u"blank_1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blank_1.sizePolicy().hasHeightForWidth())
        self.blank_1.setSizePolicy(sizePolicy)
        self.blank_1.setMinimumSize(QSize(400, 10))
        self.blank_1.setMaximumSize(QSize(400, 10))
        self.blank_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.blank_1.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.blank_1)

        self.frame_1 = QFrame(Dialog)
        self.frame_1.setObjectName(u"frame_1")
        sizePolicy.setHeightForWidth(self.frame_1.sizePolicy().hasHeightForWidth())
        self.frame_1.setSizePolicy(sizePolicy)
        self.frame_1.setMinimumSize(QSize(400, 60))
        self.frame_1.setMaximumSize(QSize(400, 60))
        self.frame_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_1.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_1)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.line_name_f = QFrame(self.frame_1)
        self.line_name_f.setObjectName(u"line_name_f")
        sizePolicy.setHeightForWidth(self.line_name_f.sizePolicy().hasHeightForWidth())
        self.line_name_f.setSizePolicy(sizePolicy)
        self.line_name_f.setMinimumSize(QSize(200, 30))
        self.line_name_f.setMaximumSize(QSize(200, 30))
        self.line_name_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_name_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.line_name_f)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 1, 5, 1)
        self.line_name_l = QLabel(self.line_name_f)
        self.line_name_l.setObjectName(u"line_name_l")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_name_l.sizePolicy().hasHeightForWidth())
        self.line_name_l.setSizePolicy(sizePolicy1)
        self.line_name_l.setMinimumSize(QSize(75, 0))
        self.line_name_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout.addWidget(self.line_name_l)

        self.line_name_i = QLineEdit(self.line_name_f)
        self.line_name_i.setObjectName(u"line_name_i")
        self.line_name_i.setFrame(True)

        self.horizontalLayout.addWidget(self.line_name_i)


        self.gridLayout.addWidget(self.line_name_f, 0, 0, 1, 1)

        self.line_id_f = QFrame(self.frame_1)
        self.line_id_f.setObjectName(u"line_id_f")
        sizePolicy.setHeightForWidth(self.line_id_f.sizePolicy().hasHeightForWidth())
        self.line_id_f.setSizePolicy(sizePolicy)
        self.line_id_f.setMinimumSize(QSize(200, 30))
        self.line_id_f.setMaximumSize(QSize(200, 30))
        self.line_id_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_id_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.line_id_f)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 1, 10, 1)
        self.line_id_l = QLabel(self.line_id_f)
        self.line_id_l.setObjectName(u"line_id_l")
        sizePolicy1.setHeightForWidth(self.line_id_l.sizePolicy().hasHeightForWidth())
        self.line_id_l.setSizePolicy(sizePolicy1)
        self.line_id_l.setMinimumSize(QSize(75, 0))
        self.line_id_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_2.addWidget(self.line_id_l)

        self.line_id_i = QLineEdit(self.line_id_f)
        self.line_id_i.setObjectName(u"line_id_i")

        self.horizontalLayout_2.addWidget(self.line_id_i)


        self.gridLayout.addWidget(self.line_id_f, 0, 1, 1, 1)

        self.line_color_f = QFrame(self.frame_1)
        self.line_color_f.setObjectName(u"line_color_f")
        sizePolicy.setHeightForWidth(self.line_color_f.sizePolicy().hasHeightForWidth())
        self.line_color_f.setSizePolicy(sizePolicy)
        self.line_color_f.setMinimumSize(QSize(200, 30))
        self.line_color_f.setMaximumSize(QSize(200, 30))
        self.line_color_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_color_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.line_color_f)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(10, 1, 5, 1)
        self.line_color_l = QLabel(self.line_color_f)
        self.line_color_l.setObjectName(u"line_color_l")
        sizePolicy1.setHeightForWidth(self.line_color_l.sizePolicy().hasHeightForWidth())
        self.line_color_l.setSizePolicy(sizePolicy1)
        self.line_color_l.setMinimumSize(QSize(75, 0))
        self.line_color_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_4.addWidget(self.line_color_l)

        self.line_color_i = QLineEdit(self.line_color_f)
        self.line_color_i.setObjectName(u"line_color_i")
        self.line_color_i.setMaxLength(7)
        self.line_color_i.setFrame(True)

        self.horizontalLayout_4.addWidget(self.line_color_i)

        self.line_color_c = QPushButton(self.line_color_f)
        self.line_color_c.setObjectName(u"line_color_c")
        sizePolicy.setHeightForWidth(self.line_color_c.sizePolicy().hasHeightForWidth())
        self.line_color_c.setSizePolicy(sizePolicy)
        self.line_color_c.setMinimumSize(QSize(24, 24))
        self.line_color_c.setMaximumSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.line_color_c)


        self.gridLayout.addWidget(self.line_color_f, 1, 0, 1, 1)

        self.empty_frame_1 = QFrame(self.frame_1)
        self.empty_frame_1.setObjectName(u"empty_frame_1")
        sizePolicy.setHeightForWidth(self.empty_frame_1.sizePolicy().hasHeightForWidth())
        self.empty_frame_1.setSizePolicy(sizePolicy)
        self.empty_frame_1.setMinimumSize(QSize(200, 30))
        self.empty_frame_1.setMaximumSize(QSize(200, 30))
        self.empty_frame_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.empty_frame_1.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.empty_frame_1)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(5, 1, 10, 1)

        self.gridLayout.addWidget(self.empty_frame_1, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_1)

        self.blank_2 = QFrame(Dialog)
        self.blank_2.setObjectName(u"blank_2")
        sizePolicy.setHeightForWidth(self.blank_2.sizePolicy().hasHeightForWidth())
        self.blank_2.setSizePolicy(sizePolicy)
        self.blank_2.setMinimumSize(QSize(400, 10))
        self.blank_2.setMaximumSize(QSize(400, 10))
        self.blank_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.blank_2.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.blank_2)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QSize(400, 90))
        self.frame_2.setMaximumSize(QSize(400, 90))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.line_country_f = QFrame(self.frame_2)
        self.line_country_f.setObjectName(u"line_country_f")
        sizePolicy.setHeightForWidth(self.line_country_f.sizePolicy().hasHeightForWidth())
        self.line_country_f.setSizePolicy(sizePolicy)
        self.line_country_f.setMinimumSize(QSize(200, 30))
        self.line_country_f.setMaximumSize(QSize(200, 30))
        self.line_country_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_country_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.line_country_f)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(10, 1, 5, 1)
        self.line_country_l = QLabel(self.line_country_f)
        self.line_country_l.setObjectName(u"line_country_l")
        sizePolicy1.setHeightForWidth(self.line_country_l.sizePolicy().hasHeightForWidth())
        self.line_country_l.setSizePolicy(sizePolicy1)
        self.line_country_l.setMinimumSize(QSize(75, 0))
        self.line_country_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_6.addWidget(self.line_country_l)

        self.line_country_i = QLineEdit(self.line_country_f)
        self.line_country_i.setObjectName(u"line_country_i")

        self.horizontalLayout_6.addWidget(self.line_country_i)


        self.gridLayout_2.addWidget(self.line_country_f, 1, 0, 1, 1)

        self.line_type_f = QFrame(self.frame_2)
        self.line_type_f.setObjectName(u"line_type_f")
        sizePolicy.setHeightForWidth(self.line_type_f.sizePolicy().hasHeightForWidth())
        self.line_type_f.setSizePolicy(sizePolicy)
        self.line_type_f.setMinimumSize(QSize(200, 30))
        self.line_type_f.setMaximumSize(QSize(200, 30))
        self.line_type_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_type_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.line_type_f)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(10, 1, 5, 1)
        self.line_type_l = QLabel(self.line_type_f)
        self.line_type_l.setObjectName(u"line_type_l")
        sizePolicy1.setHeightForWidth(self.line_type_l.sizePolicy().hasHeightForWidth())
        self.line_type_l.setSizePolicy(sizePolicy1)
        self.line_type_l.setMinimumSize(QSize(75, 0))
        self.line_type_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_5.addWidget(self.line_type_l)

        self.line_type_i = QLineEdit(self.line_type_f)
        self.line_type_i.setObjectName(u"line_type_i")
        self.line_type_i.setFrame(True)

        self.horizontalLayout_5.addWidget(self.line_type_i)


        self.gridLayout_2.addWidget(self.line_type_f, 0, 0, 1, 1)

        self.line_city_f = QFrame(self.frame_2)
        self.line_city_f.setObjectName(u"line_city_f")
        sizePolicy.setHeightForWidth(self.line_city_f.sizePolicy().hasHeightForWidth())
        self.line_city_f.setSizePolicy(sizePolicy)
        self.line_city_f.setMinimumSize(QSize(200, 30))
        self.line_city_f.setMaximumSize(QSize(200, 30))
        self.line_city_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_city_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.line_city_f)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(5, 1, 10, 1)
        self.line_city_l = QLabel(self.line_city_f)
        self.line_city_l.setObjectName(u"line_city_l")
        sizePolicy1.setHeightForWidth(self.line_city_l.sizePolicy().hasHeightForWidth())
        self.line_city_l.setSizePolicy(sizePolicy1)
        self.line_city_l.setMinimumSize(QSize(75, 0))
        self.line_city_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_7.addWidget(self.line_city_l)

        self.line_city_i = QLineEdit(self.line_city_f)
        self.line_city_i.setObjectName(u"line_city_i")
        self.line_city_i.setFrame(True)

        self.horizontalLayout_7.addWidget(self.line_city_i)


        self.gridLayout_2.addWidget(self.line_city_f, 1, 1, 1, 1)

        self.line_owner_f = QFrame(self.frame_2)
        self.line_owner_f.setObjectName(u"line_owner_f")
        sizePolicy.setHeightForWidth(self.line_owner_f.sizePolicy().hasHeightForWidth())
        self.line_owner_f.setSizePolicy(sizePolicy)
        self.line_owner_f.setMinimumSize(QSize(200, 30))
        self.line_owner_f.setMaximumSize(QSize(200, 30))
        self.line_owner_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_owner_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.line_owner_f)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(10, 1, 5, 1)
        self.line_owner_l = QLabel(self.line_owner_f)
        self.line_owner_l.setObjectName(u"line_owner_l")
        sizePolicy1.setHeightForWidth(self.line_owner_l.sizePolicy().hasHeightForWidth())
        self.line_owner_l.setSizePolicy(sizePolicy1)
        self.line_owner_l.setMinimumSize(QSize(75, 0))
        self.line_owner_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_9.addWidget(self.line_owner_l)

        self.line_owner_i = QLineEdit(self.line_owner_f)
        self.line_owner_i.setObjectName(u"line_owner_i")
        self.line_owner_i.setFrame(True)

        self.horizontalLayout_9.addWidget(self.line_owner_i)


        self.gridLayout_2.addWidget(self.line_owner_f, 2, 0, 1, 1)

        self.line_operator_f = QFrame(self.frame_2)
        self.line_operator_f.setObjectName(u"line_operator_f")
        sizePolicy.setHeightForWidth(self.line_operator_f.sizePolicy().hasHeightForWidth())
        self.line_operator_f.setSizePolicy(sizePolicy)
        self.line_operator_f.setMinimumSize(QSize(200, 30))
        self.line_operator_f.setMaximumSize(QSize(200, 30))
        self.line_operator_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_operator_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.line_operator_f)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(5, 1, 10, 1)
        self.line_operator_l = QLabel(self.line_operator_f)
        self.line_operator_l.setObjectName(u"line_operator_l")
        sizePolicy1.setHeightForWidth(self.line_operator_l.sizePolicy().hasHeightForWidth())
        self.line_operator_l.setSizePolicy(sizePolicy1)
        self.line_operator_l.setMinimumSize(QSize(75, 0))
        self.line_operator_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_8.addWidget(self.line_operator_l)

        self.line_operator_i = QLineEdit(self.line_operator_f)
        self.line_operator_i.setObjectName(u"line_operator_i")

        self.horizontalLayout_8.addWidget(self.line_operator_i)


        self.gridLayout_2.addWidget(self.line_operator_f, 2, 1, 1, 1)

        self.empty_frame_2 = QFrame(self.frame_2)
        self.empty_frame_2.setObjectName(u"empty_frame_2")
        sizePolicy.setHeightForWidth(self.empty_frame_2.sizePolicy().hasHeightForWidth())
        self.empty_frame_2.setSizePolicy(sizePolicy)
        self.empty_frame_2.setMinimumSize(QSize(200, 30))
        self.empty_frame_2.setMaximumSize(QSize(200, 30))
        self.empty_frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.empty_frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.empty_frame_2)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(5, 1, 10, 1)

        self.gridLayout_2.addWidget(self.empty_frame_2, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_2)

        self.blank_3 = QFrame(Dialog)
        self.blank_3.setObjectName(u"blank_3")
        sizePolicy.setHeightForWidth(self.blank_3.sizePolicy().hasHeightForWidth())
        self.blank_3.setSizePolicy(sizePolicy)
        self.blank_3.setMinimumSize(QSize(400, 10))
        self.blank_3.setMaximumSize(QSize(400, 10))
        self.blank_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.blank_3.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.blank_3)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QSize(400, 60))
        self.frame_3.setMaximumSize(QSize(400, 60))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.line_start_f = QFrame(self.frame_3)
        self.line_start_f.setObjectName(u"line_start_f")
        sizePolicy.setHeightForWidth(self.line_start_f.sizePolicy().hasHeightForWidth())
        self.line_start_f.setSizePolicy(sizePolicy)
        self.line_start_f.setMinimumSize(QSize(200, 30))
        self.line_start_f.setMaximumSize(QSize(200, 30))
        self.line_start_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_start_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.line_start_f)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(10, 1, 5, 1)
        self.line_start_l = QLabel(self.line_start_f)
        self.line_start_l.setObjectName(u"line_start_l")
        sizePolicy1.setHeightForWidth(self.line_start_l.sizePolicy().hasHeightForWidth())
        self.line_start_l.setSizePolicy(sizePolicy1)
        self.line_start_l.setMinimumSize(QSize(75, 0))
        self.line_start_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_13.addWidget(self.line_start_l)

        self.line_start_i = QLineEdit(self.line_start_f)
        self.line_start_i.setObjectName(u"line_start_i")
        self.line_start_i.setFrame(True)
        self.line_start_i.setReadOnly(True)

        self.horizontalLayout_13.addWidget(self.line_start_i)


        self.gridLayout_3.addWidget(self.line_start_f, 0, 0, 1, 1)

        self.line_end_f = QFrame(self.frame_3)
        self.line_end_f.setObjectName(u"line_end_f")
        sizePolicy.setHeightForWidth(self.line_end_f.sizePolicy().hasHeightForWidth())
        self.line_end_f.setSizePolicy(sizePolicy)
        self.line_end_f.setMinimumSize(QSize(200, 30))
        self.line_end_f.setMaximumSize(QSize(200, 30))
        self.line_end_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_end_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.line_end_f)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(5, 1, 10, 1)
        self.line_end_l = QLabel(self.line_end_f)
        self.line_end_l.setObjectName(u"line_end_l")
        sizePolicy1.setHeightForWidth(self.line_end_l.sizePolicy().hasHeightForWidth())
        self.line_end_l.setSizePolicy(sizePolicy1)
        self.line_end_l.setMinimumSize(QSize(75, 0))
        self.line_end_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_14.addWidget(self.line_end_l)

        self.line_end_i = QLineEdit(self.line_end_f)
        self.line_end_i.setObjectName(u"line_end_i")
        self.line_end_i.setReadOnly(True)

        self.horizontalLayout_14.addWidget(self.line_end_i)


        self.gridLayout_3.addWidget(self.line_end_f, 0, 1, 1, 1)

        self.line_count_f = QFrame(self.frame_3)
        self.line_count_f.setObjectName(u"line_count_f")
        sizePolicy.setHeightForWidth(self.line_count_f.sizePolicy().hasHeightForWidth())
        self.line_count_f.setSizePolicy(sizePolicy)
        self.line_count_f.setMinimumSize(QSize(200, 30))
        self.line_count_f.setMaximumSize(QSize(200, 30))
        self.line_count_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_count_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.line_count_f)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(10, 1, 5, 1)
        self.line_count_l = QLabel(self.line_count_f)
        self.line_count_l.setObjectName(u"line_count_l")
        sizePolicy1.setHeightForWidth(self.line_count_l.sizePolicy().hasHeightForWidth())
        self.line_count_l.setSizePolicy(sizePolicy1)
        self.line_count_l.setMinimumSize(QSize(75, 0))
        self.line_count_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_15.addWidget(self.line_count_l)

        self.line_count_i = QLineEdit(self.line_count_f)
        self.line_count_i.setObjectName(u"line_count_i")
        self.line_count_i.setMaxLength(8)
        self.line_count_i.setFrame(True)
        self.line_count_i.setReadOnly(True)

        self.horizontalLayout_15.addWidget(self.line_count_i)


        self.gridLayout_3.addWidget(self.line_count_f, 1, 0, 1, 1)

        self.empty_frame_3 = QFrame(self.frame_3)
        self.empty_frame_3.setObjectName(u"empty_frame_3")
        sizePolicy.setHeightForWidth(self.empty_frame_3.sizePolicy().hasHeightForWidth())
        self.empty_frame_3.setSizePolicy(sizePolicy)
        self.empty_frame_3.setMinimumSize(QSize(200, 30))
        self.empty_frame_3.setMaximumSize(QSize(200, 30))
        self.empty_frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.empty_frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.empty_frame_3)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(5, 1, 10, 1)
        self.text_1 = QLabel(self.empty_frame_3)
        self.text_1.setObjectName(u"text_1")
        font = QFont()
        font.setPointSize(8)
        self.text_1.setFont(font)

        self.horizontalLayout_16.addWidget(self.text_1)


        self.gridLayout_3.addWidget(self.empty_frame_3, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_3)

        self.blank_4 = QFrame(Dialog)
        self.blank_4.setObjectName(u"blank_4")
        sizePolicy.setHeightForWidth(self.blank_4.sizePolicy().hasHeightForWidth())
        self.blank_4.setSizePolicy(sizePolicy)
        self.blank_4.setMinimumSize(QSize(400, 10))
        self.blank_4.setMaximumSize(QSize(400, 10))
        self.blank_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.blank_4.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.blank_4)

        self.frame_4 = QFrame(Dialog)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setMinimumSize(QSize(400, 60))
        self.frame_4.setMaximumSize(QSize(400, 60))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.line_speed_f = QFrame(self.frame_4)
        self.line_speed_f.setObjectName(u"line_speed_f")
        sizePolicy.setHeightForWidth(self.line_speed_f.sizePolicy().hasHeightForWidth())
        self.line_speed_f.setSizePolicy(sizePolicy)
        self.line_speed_f.setMinimumSize(QSize(200, 30))
        self.line_speed_f.setMaximumSize(QSize(200, 30))
        self.line_speed_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_speed_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.line_speed_f)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(10, 1, 5, 1)
        self.line_speed_l = QLabel(self.line_speed_f)
        self.line_speed_l.setObjectName(u"line_speed_l")
        sizePolicy1.setHeightForWidth(self.line_speed_l.sizePolicy().hasHeightForWidth())
        self.line_speed_l.setSizePolicy(sizePolicy1)
        self.line_speed_l.setMinimumSize(QSize(75, 0))
        self.line_speed_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_17.addWidget(self.line_speed_l)

        self.line_speed_i = QLineEdit(self.line_speed_f)
        self.line_speed_i.setObjectName(u"line_speed_i")
        self.line_speed_i.setMaxLength(5)
        self.line_speed_i.setFrame(True)
        self.line_speed_i.setReadOnly(False)

        self.horizontalLayout_17.addWidget(self.line_speed_i)

        self.label_1 = QLabel(self.line_speed_f)
        self.label_1.setObjectName(u"label_1")
        sizePolicy.setHeightForWidth(self.label_1.sizePolicy().hasHeightForWidth())
        self.label_1.setSizePolicy(sizePolicy)
        self.label_1.setMinimumSize(QSize(30, 16))
        self.label_1.setMaximumSize(QSize(30, 16))

        self.horizontalLayout_17.addWidget(self.label_1)


        self.gridLayout_4.addWidget(self.line_speed_f, 0, 0, 1, 1)

        self.line_linetype_f = QFrame(self.frame_4)
        self.line_linetype_f.setObjectName(u"line_linetype_f")
        sizePolicy.setHeightForWidth(self.line_linetype_f.sizePolicy().hasHeightForWidth())
        self.line_linetype_f.setSizePolicy(sizePolicy)
        self.line_linetype_f.setMinimumSize(QSize(200, 30))
        self.line_linetype_f.setMaximumSize(QSize(200, 30))
        self.line_linetype_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_linetype_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.line_linetype_f)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(5, 1, 10, 1)
        self.line_linetype_l = QLabel(self.line_linetype_f)
        self.line_linetype_l.setObjectName(u"line_linetype_l")
        sizePolicy1.setHeightForWidth(self.line_linetype_l.sizePolicy().hasHeightForWidth())
        self.line_linetype_l.setSizePolicy(sizePolicy1)
        self.line_linetype_l.setMinimumSize(QSize(75, 0))
        self.line_linetype_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_18.addWidget(self.line_linetype_l)

        self.line_linetype_i = QLineEdit(self.line_linetype_f)
        self.line_linetype_i.setObjectName(u"line_linetype_i")
        self.line_linetype_i.setReadOnly(False)

        self.horizontalLayout_18.addWidget(self.line_linetype_i)


        self.gridLayout_4.addWidget(self.line_linetype_f, 0, 1, 1, 1)

        self.line_electric_f = QFrame(self.frame_4)
        self.line_electric_f.setObjectName(u"line_electric_f")
        sizePolicy.setHeightForWidth(self.line_electric_f.sizePolicy().hasHeightForWidth())
        self.line_electric_f.setSizePolicy(sizePolicy)
        self.line_electric_f.setMinimumSize(QSize(200, 30))
        self.line_electric_f.setMaximumSize(QSize(200, 30))
        self.line_electric_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_electric_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.line_electric_f)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(10, 1, 5, 1)
        self.line_electric_l = QLabel(self.line_electric_f)
        self.line_electric_l.setObjectName(u"line_electric_l")
        sizePolicy1.setHeightForWidth(self.line_electric_l.sizePolicy().hasHeightForWidth())
        self.line_electric_l.setSizePolicy(sizePolicy1)
        self.line_electric_l.setMinimumSize(QSize(75, 0))
        self.line_electric_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_19.addWidget(self.line_electric_l)

        self.line_electric_i = QLineEdit(self.line_electric_f)
        self.line_electric_i.setObjectName(u"line_electric_i")
        self.line_electric_i.setFrame(True)
        self.line_electric_i.setReadOnly(False)

        self.horizontalLayout_19.addWidget(self.line_electric_i)


        self.gridLayout_4.addWidget(self.line_electric_f, 1, 0, 1, 1)

        self.line_safety_f = QFrame(self.frame_4)
        self.line_safety_f.setObjectName(u"line_safety_f")
        sizePolicy.setHeightForWidth(self.line_safety_f.sizePolicy().hasHeightForWidth())
        self.line_safety_f.setSizePolicy(sizePolicy)
        self.line_safety_f.setMinimumSize(QSize(200, 30))
        self.line_safety_f.setMaximumSize(QSize(200, 30))
        self.line_safety_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_safety_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.line_safety_f)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(5, 1, 10, 1)
        self.line_safety_l = QLabel(self.line_safety_f)
        self.line_safety_l.setObjectName(u"line_safety_l")
        sizePolicy1.setHeightForWidth(self.line_safety_l.sizePolicy().hasHeightForWidth())
        self.line_safety_l.setSizePolicy(sizePolicy1)
        self.line_safety_l.setMinimumSize(QSize(75, 0))
        self.line_safety_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_20.addWidget(self.line_safety_l)

        self.line_safety_i = QLineEdit(self.line_safety_f)
        self.line_safety_i.setObjectName(u"line_safety_i")
        self.line_safety_i.setReadOnly(False)

        self.horizontalLayout_20.addWidget(self.line_safety_i)


        self.gridLayout_4.addWidget(self.line_safety_f, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_4)

        self.blank_5 = QFrame(Dialog)
        self.blank_5.setObjectName(u"blank_5")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.blank_5.sizePolicy().hasHeightForWidth())
        self.blank_5.setSizePolicy(sizePolicy2)
        self.blank_5.setMaximumSize(QSize(16777215, 10))
        self.blank_5.setBaseSize(QSize(0, 10))
        self.blank_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.blank_5.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.blank_5)

        self.frame_5 = QFrame(Dialog)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy2.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy2)
        self.frame_5.setMinimumSize(QSize(0, 60))
        self.frame_5.setMaximumSize(QSize(16777215, 60))
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_5)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.stopping_time_stretching_c = QCheckBox(self.frame_5)
        self.stopping_time_stretching_c.setObjectName(u"stopping_time_stretching_c")

        self.gridLayout_5.addWidget(self.stopping_time_stretching_c, 1, 2, 2, 1)

        self.empty_frame_4 = QFrame(self.frame_5)
        self.empty_frame_4.setObjectName(u"empty_frame_4")
        sizePolicy.setHeightForWidth(self.empty_frame_4.sizePolicy().hasHeightForWidth())
        self.empty_frame_4.setSizePolicy(sizePolicy)
        self.empty_frame_4.setMinimumSize(QSize(200, 30))
        self.empty_frame_4.setMaximumSize(QSize(200, 30))
        self.empty_frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.empty_frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.empty_frame_4)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(5, 1, 10, 1)

        self.gridLayout_5.addWidget(self.empty_frame_4, 0, 2, 1, 1)

        self.interval_time_f = QFrame(self.frame_5)
        self.interval_time_f.setObjectName(u"interval_time_f")
        sizePolicy.setHeightForWidth(self.interval_time_f.sizePolicy().hasHeightForWidth())
        self.interval_time_f.setSizePolicy(sizePolicy)
        self.interval_time_f.setMinimumSize(QSize(200, 30))
        self.interval_time_f.setMaximumSize(QSize(200, 30))
        self.interval_time_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.interval_time_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.interval_time_f)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(10, 1, 5, 1)
        self.interval_time_l = QLabel(self.interval_time_f)
        self.interval_time_l.setObjectName(u"interval_time_l")
        sizePolicy1.setHeightForWidth(self.interval_time_l.sizePolicy().hasHeightForWidth())
        self.interval_time_l.setSizePolicy(sizePolicy1)
        self.interval_time_l.setMinimumSize(QSize(75, 0))
        self.interval_time_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_10.addWidget(self.interval_time_l)

        self.interval_time_i = QLineEdit(self.interval_time_f)
        self.interval_time_i.setObjectName(u"interval_time_i")
        self.interval_time_i.setMaxLength(12)
        self.interval_time_i.setFrame(True)

        self.horizontalLayout_10.addWidget(self.interval_time_i)

        self.label_2 = QLabel(self.interval_time_f)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(30, 16))
        self.label_2.setMaximumSize(QSize(30, 16))

        self.horizontalLayout_10.addWidget(self.label_2)


        self.gridLayout_5.addWidget(self.interval_time_f, 0, 0, 2, 1)

        self.shift_step_f = QFrame(self.frame_5)
        self.shift_step_f.setObjectName(u"shift_step_f")
        sizePolicy.setHeightForWidth(self.shift_step_f.sizePolicy().hasHeightForWidth())
        self.shift_step_f.setSizePolicy(sizePolicy)
        self.shift_step_f.setMinimumSize(QSize(200, 30))
        self.shift_step_f.setMaximumSize(QSize(200, 30))
        self.shift_step_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.shift_step_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.shift_step_f)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(10, 1, 5, 1)
        self.shift_step_l = QLabel(self.shift_step_f)
        self.shift_step_l.setObjectName(u"shift_step_l")
        sizePolicy1.setHeightForWidth(self.shift_step_l.sizePolicy().hasHeightForWidth())
        self.shift_step_l.setSizePolicy(sizePolicy1)
        self.shift_step_l.setMinimumSize(QSize(75, 0))
        self.shift_step_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_22.addWidget(self.shift_step_l)

        self.shift_step_i = QLineEdit(self.shift_step_f)
        self.shift_step_i.setObjectName(u"shift_step_i")
        self.shift_step_i.setMaxLength(12)
        self.shift_step_i.setFrame(True)

        self.horizontalLayout_22.addWidget(self.shift_step_i)

        self.shift_step_unit_l = QLabel(self.shift_step_f)
        self.shift_step_unit_l.setObjectName(u"shift_step_unit_l")
        sizePolicy.setHeightForWidth(self.shift_step_unit_l.sizePolicy().hasHeightForWidth())
        self.shift_step_unit_l.setSizePolicy(sizePolicy)
        self.shift_step_unit_l.setMinimumSize(QSize(30, 16))
        self.shift_step_unit_l.setMaximumSize(QSize(30, 16))

        self.horizontalLayout_22.addWidget(self.shift_step_unit_l)


        self.gridLayout_5.addWidget(self.shift_step_f, 2, 0, 1, 1)

        self.empty_frame_5 = QFrame(self.frame_5)
        self.empty_frame_5.setObjectName(u"empty_frame_5")
        sizePolicy1.setHeightForWidth(self.empty_frame_5.sizePolicy().hasHeightForWidth())
        self.empty_frame_5.setSizePolicy(sizePolicy1)
        self.empty_frame_5.setMinimumSize(QSize(14, 0))
        self.empty_frame_5.setMaximumSize(QSize(14, 16777215))
        self.empty_frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.empty_frame_5.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_5.addWidget(self.empty_frame_5, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_5)

        self.blank_6 = QFrame(Dialog)
        self.blank_6.setObjectName(u"blank_6")
        sizePolicy2.setHeightForWidth(self.blank_6.sizePolicy().hasHeightForWidth())
        self.blank_6.setSizePolicy(sizePolicy2)
        self.blank_6.setMinimumSize(QSize(0, 10))
        self.blank_6.setMaximumSize(QSize(16777215, 10))
        self.blank_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.blank_6.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.blank_6)

        self.frame_6 = QFrame(Dialog)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy2.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy2)
        self.frame_6.setMinimumSize(QSize(0, 30))
        self.frame_6.setMaximumSize(QSize(16777215, 30))
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.line_start_f_2 = QFrame(self.frame_6)
        self.line_start_f_2.setObjectName(u"line_start_f_2")
        sizePolicy.setHeightForWidth(self.line_start_f_2.sizePolicy().hasHeightForWidth())
        self.line_start_f_2.setSizePolicy(sizePolicy)
        self.line_start_f_2.setMinimumSize(QSize(200, 30))
        self.line_start_f_2.setMaximumSize(QSize(200, 30))
        self.line_start_f_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_start_f_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.line_start_f_2)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(10, 1, 5, 1)
        self.first_departure_l = QLabel(self.line_start_f_2)
        self.first_departure_l.setObjectName(u"first_departure_l")
        sizePolicy1.setHeightForWidth(self.first_departure_l.sizePolicy().hasHeightForWidth())
        self.first_departure_l.setSizePolicy(sizePolicy1)
        self.first_departure_l.setMinimumSize(QSize(75, 0))
        self.first_departure_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_24.addWidget(self.first_departure_l)

        self.first_departure_t = QTimeEdit(self.line_start_f_2)
        self.first_departure_t.setObjectName(u"first_departure_t")
        self.first_departure_t.setCurrentSection(QDateTimeEdit.Section.AmPmSection)

        self.horizontalLayout_24.addWidget(self.first_departure_t)


        self.horizontalLayout_3.addWidget(self.line_start_f_2)

        self.line_end_f_2 = QFrame(self.frame_6)
        self.line_end_f_2.setObjectName(u"line_end_f_2")
        sizePolicy.setHeightForWidth(self.line_end_f_2.sizePolicy().hasHeightForWidth())
        self.line_end_f_2.setSizePolicy(sizePolicy)
        self.line_end_f_2.setMinimumSize(QSize(200, 30))
        self.line_end_f_2.setMaximumSize(QSize(200, 30))
        self.line_end_f_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_end_f_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.line_end_f_2)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(5, 1, 10, 1)
        self.last_departure_l = QLabel(self.line_end_f_2)
        self.last_departure_l.setObjectName(u"last_departure_l")
        sizePolicy1.setHeightForWidth(self.last_departure_l.sizePolicy().hasHeightForWidth())
        self.last_departure_l.setSizePolicy(sizePolicy1)
        self.last_departure_l.setMinimumSize(QSize(75, 0))
        self.last_departure_l.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_25.addWidget(self.last_departure_l)

        self.last_departure_t = QTimeEdit(self.line_end_f_2)
        self.last_departure_t.setObjectName(u"last_departure_t")
        self.last_departure_t.setTimeSpec(Qt.TimeSpec.UTC)

        self.horizontalLayout_25.addWidget(self.last_departure_t)


        self.horizontalLayout_3.addWidget(self.line_end_f_2)


        self.verticalLayout.addWidget(self.frame_6)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u8def\u7dda\u8cc7\u6599\u8a2d\u5b9a", None))
        self.line_name_l.setText(QCoreApplication.translate("Dialog", u"\u8def\u7dda\u540d\u7a31*", None))
        self.line_id_l.setText(QCoreApplication.translate("Dialog", u"\u8def\u7ddaID*", None))
        self.line_color_l.setText(QCoreApplication.translate("Dialog", u"\u8def\u7dda\u984f\u8272*", None))
        self.line_color_c.setText("")
        self.line_country_l.setText(QCoreApplication.translate("Dialog", u"\u8def\u7dda\u6240\u5728\u570b", None))
        self.line_type_l.setText(QCoreApplication.translate("Dialog", u"\u8def\u7dda\u985e\u578b", None))
        self.line_city_l.setText(QCoreApplication.translate("Dialog", u"\u4e3b\u8981\u71df\u904b\u57ce\u5e02", None))
        self.line_owner_l.setText(QCoreApplication.translate("Dialog", u"\u8def\u7dda\u64c1\u6709\u8005", None))
        self.line_operator_l.setText(QCoreApplication.translate("Dialog", u"\u8def\u7dda\u71df\u904b\u8005", None))
        self.line_start_l.setText(QCoreApplication.translate("Dialog", u"\u8def\u7dda\u8d77\u9ede", None))
        self.line_end_l.setText(QCoreApplication.translate("Dialog", u"\u8def\u7dda\u7d42\u9ede", None))
        self.line_count_l.setText(QCoreApplication.translate("Dialog", u"\u8def\u7dda\u8eca\u7ad9\u6578", None))
        self.text_1.setText(QCoreApplication.translate("Dialog", u"(\u57fa\u672c\u904b\u884c\u6642\u523b\u8868\u4e0a\u50b3\u5f8c\u81ea\u52d5\u986f\u793a)", None))
        self.line_speed_l.setText(QCoreApplication.translate("Dialog", u"\u6700\u9ad8\u71df\u904b\u901f\u5ea6", None))
        self.label_1.setText(QCoreApplication.translate("Dialog", u"km/h", None))
        self.line_linetype_l.setText(QCoreApplication.translate("Dialog", u"\u7dda\u8def\u985e\u578b", None))
        self.line_electric_l.setText(QCoreApplication.translate("Dialog", u"\u96fb\u6c23\u5316\u6a21\u5f0f", None))
        self.line_safety_l.setText(QCoreApplication.translate("Dialog", u"\u5b89\u5168\u88dd\u7f6e", None))
        self.stopping_time_stretching_c.setText(QCoreApplication.translate("Dialog", u"\u505c\u9760\u6642\u9593\u53ef\u62c9\u4f38", None))
        self.interval_time_l.setText(QCoreApplication.translate("Dialog", u"\u767c\u8eca\u9593\u9694\u6642\u9593", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u79d2", None))
        self.shift_step_l.setText(QCoreApplication.translate("Dialog", u"\u73ed\u6b21\u5e73\u79fb\u6b65\u9032", None))
        self.shift_step_unit_l.setText(QCoreApplication.translate("Dialog", u"\u79d2", None))
        self.first_departure_l.setText(QCoreApplication.translate("Dialog", u"\u8def\u7dda\u8d77\u9ede", None))
        self.first_departure_t.setDisplayFormat(QCoreApplication.translate("Dialog", u"AP hh:mm:ss", None))
        self.last_departure_l.setText(QCoreApplication.translate("Dialog", u"\u8def\u7dda\u7d42\u9ede", None))
        self.last_departure_t.setDisplayFormat(QCoreApplication.translate("Dialog", u"AP hh:mm:ss", None))
    # retranslateUi

