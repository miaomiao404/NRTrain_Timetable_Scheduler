# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stations_facilities_editor.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGraphicsView,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_stations_facilities_frame(object):
    def setupUi(self, stations_facilities_frame):
        if not stations_facilities_frame.objectName():
            stations_facilities_frame.setObjectName(u"stations_facilities_frame")
        stations_facilities_frame.resize(1200, 600)
        self.verticalLayout_2 = QVBoxLayout(stations_facilities_frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(stations_facilities_frame)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setMaximumSize(QSize(16777215, 16777215))
        self.splitter.setFrameShape(QFrame.Shape.NoFrame)
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
        self.verticalLayout = QVBoxLayout(self.stations_facilities_list_f)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 0, 5, 0)
        self.searching_f = QFrame(self.stations_facilities_list_f)
        self.searching_f.setObjectName(u"searching_f")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.searching_f.sizePolicy().hasHeightForWidth())
        self.searching_f.setSizePolicy(sizePolicy1)
        self.searching_f.setMinimumSize(QSize(0, 30))
        self.searching_f.setMaximumSize(QSize(16777215, 30))
        self.searching_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.searching_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.searching_f)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.searching_bar = QLineEdit(self.searching_f)
        self.searching_bar.setObjectName(u"searching_bar")
        self.searching_bar.setMaxLength(200)

        self.horizontalLayout_2.addWidget(self.searching_bar)

        self.searching_b = QPushButton(self.searching_f)
        self.searching_b.setObjectName(u"searching_b")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.searching_b.sizePolicy().hasHeightForWidth())
        self.searching_b.setSizePolicy(sizePolicy2)
        self.searching_b.setMinimumSize(QSize(40, 0))
        self.searching_b.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_2.addWidget(self.searching_b)


        self.verticalLayout.addWidget(self.searching_f)

        self.line_filter_f = QFrame(self.stations_facilities_list_f)
        self.line_filter_f.setObjectName(u"line_filter_f")
        sizePolicy1.setHeightForWidth(self.line_filter_f.sizePolicy().hasHeightForWidth())
        self.line_filter_f.setSizePolicy(sizePolicy1)
        self.line_filter_f.setMinimumSize(QSize(0, 30))
        self.line_filter_f.setMaximumSize(QSize(16777215, 30))
        self.line_filter_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.line_filter_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.line_filter_f)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.line_filter_box = QComboBox(self.line_filter_f)
        self.line_filter_box.setObjectName(u"line_filter_box")

        self.horizontalLayout.addWidget(self.line_filter_box)

        self.reset_filter_b = QPushButton(self.line_filter_f)
        self.reset_filter_b.setObjectName(u"reset_filter_b")
        sizePolicy2.setHeightForWidth(self.reset_filter_b.sizePolicy().hasHeightForWidth())
        self.reset_filter_b.setSizePolicy(sizePolicy2)
        self.reset_filter_b.setMinimumSize(QSize(80, 0))
        self.reset_filter_b.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.reset_filter_b)


        self.verticalLayout.addWidget(self.line_filter_f)

        self.splitter_2 = QSplitter(self.stations_facilities_list_f)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)
        self.splitter_2.setChildrenCollapsible(False)
        self.stations_list_f = QFrame(self.splitter_2)
        self.stations_list_f.setObjectName(u"stations_list_f")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(7)
        sizePolicy3.setHeightForWidth(self.stations_list_f.sizePolicy().hasHeightForWidth())
        self.stations_list_f.setSizePolicy(sizePolicy3)
        self.stations_list_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.stations_list_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.stations_list_f)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.stations_list_l = QLabel(self.stations_list_f)
        self.stations_list_l.setObjectName(u"stations_list_l")
        self.stations_list_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.stations_list_l)

        self.stations_list = QTableWidget(self.stations_list_f)
        self.stations_list.setObjectName(u"stations_list")
        self.stations_list.setFrameShape(QFrame.Shape.HLine)
        self.stations_list.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout_3.addWidget(self.stations_list)

        self.add_stations_f = QFrame(self.stations_list_f)
        self.add_stations_f.setObjectName(u"add_stations_f")
        self.add_stations_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.add_stations_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.add_stations_f)
        self.horizontalLayout_6.setSpacing(3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.add_stations_id_l = QLabel(self.add_stations_f)
        self.add_stations_id_l.setObjectName(u"add_stations_id_l")

        self.horizontalLayout_6.addWidget(self.add_stations_id_l)

        self.add_stations_id_editor = QLineEdit(self.add_stations_f)
        self.add_stations_id_editor.setObjectName(u"add_stations_id_editor")
        self.add_stations_id_editor.setMaxLength(20)

        self.horizontalLayout_6.addWidget(self.add_stations_id_editor)

        self.add_stations_b = QPushButton(self.add_stations_f)
        self.add_stations_b.setObjectName(u"add_stations_b")
        sizePolicy2.setHeightForWidth(self.add_stations_b.sizePolicy().hasHeightForWidth())
        self.add_stations_b.setSizePolicy(sizePolicy2)
        self.add_stations_b.setMinimumSize(QSize(60, 0))
        self.add_stations_b.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_6.addWidget(self.add_stations_b)


        self.verticalLayout_3.addWidget(self.add_stations_f)

        self.splitter_2.addWidget(self.stations_list_f)
        self.facilities_list_f = QFrame(self.splitter_2)
        self.facilities_list_f.setObjectName(u"facilities_list_f")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(3)
        sizePolicy4.setHeightForWidth(self.facilities_list_f.sizePolicy().hasHeightForWidth())
        self.facilities_list_f.setSizePolicy(sizePolicy4)
        self.facilities_list_f.setMinimumSize(QSize(0, 100))
        self.facilities_list_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.facilities_list_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.facilities_list_f)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.facilities_list_l = QLabel(self.facilities_list_f)
        self.facilities_list_l.setObjectName(u"facilities_list_l")
        self.facilities_list_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.facilities_list_l)

        self.facilities_list = QTableWidget(self.facilities_list_f)
        self.facilities_list.setObjectName(u"facilities_list")
        self.facilities_list.setFrameShape(QFrame.Shape.HLine)
        self.facilities_list.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout_4.addWidget(self.facilities_list)

        self.add_facilities_f = QFrame(self.facilities_list_f)
        self.add_facilities_f.setObjectName(u"add_facilities_f")
        self.add_facilities_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.add_facilities_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.add_facilities_f)
        self.horizontalLayout_7.setSpacing(3)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.add_facilities_id_l = QLabel(self.add_facilities_f)
        self.add_facilities_id_l.setObjectName(u"add_facilities_id_l")

        self.horizontalLayout_7.addWidget(self.add_facilities_id_l)

        self.add_facilities_id_editor = QLineEdit(self.add_facilities_f)
        self.add_facilities_id_editor.setObjectName(u"add_facilities_id_editor")
        self.add_facilities_id_editor.setMaxLength(20)

        self.horizontalLayout_7.addWidget(self.add_facilities_id_editor)

        self.add_facilities_b = QPushButton(self.add_facilities_f)
        self.add_facilities_b.setObjectName(u"add_facilities_b")
        sizePolicy2.setHeightForWidth(self.add_facilities_b.sizePolicy().hasHeightForWidth())
        self.add_facilities_b.setSizePolicy(sizePolicy2)
        self.add_facilities_b.setMinimumSize(QSize(60, 0))
        self.add_facilities_b.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_7.addWidget(self.add_facilities_b)


        self.verticalLayout_4.addWidget(self.add_facilities_f)

        self.splitter_2.addWidget(self.facilities_list_f)

        self.verticalLayout.addWidget(self.splitter_2)

        self.splitter.addWidget(self.stations_facilities_list_f)
        self.right_frame = QFrame(self.splitter)
        self.right_frame.setObjectName(u"right_frame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(8)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.right_frame.sizePolicy().hasHeightForWidth())
        self.right_frame.setSizePolicy(sizePolicy5)
        self.right_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.right_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.right_frame)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 0, 5, 0)
        self.station_information_f = QFrame(self.right_frame)
        self.station_information_f.setObjectName(u"station_information_f")
        sizePolicy1.setHeightForWidth(self.station_information_f.sizePolicy().hasHeightForWidth())
        self.station_information_f.setSizePolicy(sizePolicy1)
        self.station_information_f.setMinimumSize(QSize(0, 40))
        self.station_information_f.setMaximumSize(QSize(16777215, 40))
        self.station_information_f.setFrameShape(QFrame.Shape.NoFrame)
        self.station_information_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.station_information_f)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.station_id_l = QLabel(self.station_information_f)
        self.station_id_l.setObjectName(u"station_id_l")

        self.horizontalLayout_3.addWidget(self.station_id_l)

        self.station_id_editor = QLineEdit(self.station_information_f)
        self.station_id_editor.setObjectName(u"station_id_editor")
        self.station_id_editor.setMinimumSize(QSize(40, 0))
        self.station_id_editor.setMaximumSize(QSize(80, 16777215))
        self.station_id_editor.setMaxLength(20)

        self.horizontalLayout_3.addWidget(self.station_id_editor)

        self.station_name_l = QLabel(self.station_information_f)
        self.station_name_l.setObjectName(u"station_name_l")

        self.horizontalLayout_3.addWidget(self.station_name_l)

        self.station_name_editor = QLineEdit(self.station_information_f)
        self.station_name_editor.setObjectName(u"station_name_editor")
        self.station_name_editor.setMinimumSize(QSize(60, 0))
        self.station_name_editor.setMaximumSize(QSize(240, 16777215))
        self.station_name_editor.setMaxLength(1000)

        self.horizontalLayout_3.addWidget(self.station_name_editor)

        self.station_line_id_l = QLabel(self.station_information_f)
        self.station_line_id_l.setObjectName(u"station_line_id_l")

        self.horizontalLayout_3.addWidget(self.station_line_id_l)

        self.station_line_id_editor = QLineEdit(self.station_information_f)
        self.station_line_id_editor.setObjectName(u"station_line_id_editor")
        self.station_line_id_editor.setMinimumSize(QSize(40, 0))
        self.station_line_id_editor.setMaximumSize(QSize(160, 16777215))

        self.horizontalLayout_3.addWidget(self.station_line_id_editor)

        self.station_type_ = QLabel(self.station_information_f)
        self.station_type_.setObjectName(u"station_type_")

        self.horizontalLayout_3.addWidget(self.station_type_)

        self.station_type_b = QComboBox(self.station_information_f)
        self.station_type_b.setObjectName(u"station_type_b")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.station_type_b.sizePolicy().hasHeightForWidth())
        self.station_type_b.setSizePolicy(sizePolicy6)
        self.station_type_b.setMinimumSize(QSize(110, 0))
        self.station_type_b.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout_3.addWidget(self.station_type_b)

        self.used_lines_l = QLabel(self.station_information_f)
        self.used_lines_l.setObjectName(u"used_lines_l")

        self.horizontalLayout_3.addWidget(self.used_lines_l)

        self.used_lines_editor = QLineEdit(self.station_information_f)
        self.used_lines_editor.setObjectName(u"used_lines_editor")
        sizePolicy1.setHeightForWidth(self.used_lines_editor.sizePolicy().hasHeightForWidth())
        self.used_lines_editor.setSizePolicy(sizePolicy1)
        self.used_lines_editor.setMinimumSize(QSize(100, 0))
        self.used_lines_editor.setMaximumSize(QSize(160, 16777215))
        self.used_lines_editor.setFrame(False)
        self.used_lines_editor.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.used_lines_editor)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.delete_station_b = QPushButton(self.station_information_f)
        self.delete_station_b.setObjectName(u"delete_station_b")

        self.horizontalLayout_3.addWidget(self.delete_station_b)


        self.verticalLayout_5.addWidget(self.station_information_f)

        self.track_editor_l = QLabel(self.right_frame)
        self.track_editor_l.setObjectName(u"track_editor_l")
        sizePolicy1.setHeightForWidth(self.track_editor_l.sizePolicy().hasHeightForWidth())
        self.track_editor_l.setSizePolicy(sizePolicy1)
        self.track_editor_l.setMinimumSize(QSize(0, 20))
        self.track_editor_l.setMaximumSize(QSize(16777215, 20))
        self.track_editor_l.setAutoFillBackground(False)
        self.track_editor_l.setStyleSheet(u"background-color: rgb(170, 255, 255);")

        self.verticalLayout_5.addWidget(self.track_editor_l)

        self.track_editor_f = QFrame(self.right_frame)
        self.track_editor_f.setObjectName(u"track_editor_f")
        self.track_editor_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.track_editor_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.track_editor_f)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.tracks_editor_view = QGraphicsView(self.track_editor_f)
        self.tracks_editor_view.setObjectName(u"tracks_editor_view")
        self.tracks_editor_view.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_6.addWidget(self.tracks_editor_view)

        self.add_track_f = QFrame(self.track_editor_f)
        self.add_track_f.setObjectName(u"add_track_f")
        sizePolicy1.setHeightForWidth(self.add_track_f.sizePolicy().hasHeightForWidth())
        self.add_track_f.setSizePolicy(sizePolicy1)
        self.add_track_f.setMinimumSize(QSize(0, 30))
        self.add_track_f.setMaximumSize(QSize(16777215, 30))
        self.add_track_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.add_track_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.add_track_f)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_2 = QSpacerItem(348, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.add_track_b = QPushButton(self.add_track_f)
        self.add_track_b.setObjectName(u"add_track_b")

        self.horizontalLayout_4.addWidget(self.add_track_b)

        self.horizontalSpacer_3 = QSpacerItem(347, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout_6.addWidget(self.add_track_f)


        self.verticalLayout_5.addWidget(self.track_editor_f)

        self.connection_editor_l = QLabel(self.right_frame)
        self.connection_editor_l.setObjectName(u"connection_editor_l")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(20)
        sizePolicy7.setHeightForWidth(self.connection_editor_l.sizePolicy().hasHeightForWidth())
        self.connection_editor_l.setSizePolicy(sizePolicy7)
        self.connection_editor_l.setMinimumSize(QSize(0, 20))
        self.connection_editor_l.setStyleSheet(u"background-color: rgb(170, 255, 255);")

        self.verticalLayout_5.addWidget(self.connection_editor_l)

        self.connections_editor_f = QFrame(self.right_frame)
        self.connections_editor_f.setObjectName(u"connections_editor_f")
        self.connections_editor_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.connections_editor_f.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.connections_editor_f)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.connections_editor_view = QGraphicsView(self.connections_editor_f)
        self.connections_editor_view.setObjectName(u"connections_editor_view")
        self.connections_editor_view.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_7.addWidget(self.connections_editor_view)

        self.add_connections_f = QFrame(self.connections_editor_f)
        self.add_connections_f.setObjectName(u"add_connections_f")
        sizePolicy1.setHeightForWidth(self.add_connections_f.sizePolicy().hasHeightForWidth())
        self.add_connections_f.setSizePolicy(sizePolicy1)
        self.add_connections_f.setMinimumSize(QSize(0, 30))
        self.add_connections_f.setMaximumSize(QSize(16777215, 30))
        self.add_connections_f.setFrameShape(QFrame.Shape.StyledPanel)
        self.add_connections_f.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.add_connections_f)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(109, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.label1 = QLabel(self.add_connections_f)
        self.label1.setObjectName(u"label1")

        self.horizontalLayout_5.addWidget(self.label1)

        self.connect_line_selection_box = QComboBox(self.add_connections_f)
        self.connect_line_selection_box.setObjectName(u"connect_line_selection_box")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.connect_line_selection_box.sizePolicy().hasHeightForWidth())
        self.connect_line_selection_box.setSizePolicy(sizePolicy8)
        self.connect_line_selection_box.setMinimumSize(QSize(160, 0))
        self.connect_line_selection_box.setMaximumSize(QSize(240, 16777215))

        self.horizontalLayout_5.addWidget(self.connect_line_selection_box)

        self.label2 = QLabel(self.add_connections_f)
        self.label2.setObjectName(u"label2")

        self.horizontalLayout_5.addWidget(self.label2)

        self.track_amount_selection_b = QComboBox(self.add_connections_f)
        self.track_amount_selection_b.setObjectName(u"track_amount_selection_b")
        self.track_amount_selection_b.setMinimumSize(QSize(60, 0))
        self.track_amount_selection_b.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_5.addWidget(self.track_amount_selection_b)

        self.label3 = QLabel(self.add_connections_f)
        self.label3.setObjectName(u"label3")

        self.horizontalLayout_5.addWidget(self.label3)

        self.connection_side_box = QComboBox(self.add_connections_f)
        self.connection_side_box.setObjectName(u"connection_side_box")
        self.connection_side_box.setMinimumSize(QSize(40, 0))
        self.connection_side_box.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_5.addWidget(self.connection_side_box)

        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.add_connections_b = QPushButton(self.add_connections_f)
        self.add_connections_b.setObjectName(u"add_connections_b")

        self.horizontalLayout_5.addWidget(self.add_connections_b)

        self.horizontalSpacer_5 = QSpacerItem(108, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout_7.addWidget(self.add_connections_f)


        self.verticalLayout_5.addWidget(self.connections_editor_f)

        self.splitter.addWidget(self.right_frame)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(stations_facilities_frame)

        QMetaObject.connectSlotsByName(stations_facilities_frame)
    # setupUi

    def retranslateUi(self, stations_facilities_frame):
        stations_facilities_frame.setWindowTitle(QCoreApplication.translate("stations_facilities_frame", u"Form", None))
        self.searching_b.setText(QCoreApplication.translate("stations_facilities_frame", u"\u641c\u5c0b", None))
        self.line_filter_box.setPlaceholderText(QCoreApplication.translate("stations_facilities_frame", u"\u9078\u64c7\u8def\u7dda", None))
        self.reset_filter_b.setText(QCoreApplication.translate("stations_facilities_frame", u"\u91cd\u7f6e\u7be9\u9078\u5668", None))
        self.stations_list_l.setText(QCoreApplication.translate("stations_facilities_frame", u"\u8eca\u7ad9\u5217\u8868", None))
        self.add_stations_id_l.setText(QCoreApplication.translate("stations_facilities_frame", u"\u8eca\u7ad9ID", None))
        self.add_stations_b.setText(QCoreApplication.translate("stations_facilities_frame", u"\u52a0\u5165\u8eca\u7ad9", None))
        self.facilities_list_l.setText(QCoreApplication.translate("stations_facilities_frame", u"\u8eca\u8f1b\u7dad\u8b77/\u5132\u8eca\u8a2d\u65bd\u5217\u8868", None))
        self.add_facilities_id_l.setText(QCoreApplication.translate("stations_facilities_frame", u"\u8a2d\u65bdID", None))
        self.add_facilities_b.setText(QCoreApplication.translate("stations_facilities_frame", u"\u52a0\u5165\u8a2d\u65bd", None))
        self.station_id_l.setText(QCoreApplication.translate("stations_facilities_frame", u"\u8eca\u7ad9ID(\u552f\u4e00)", None))
        self.station_name_l.setText(QCoreApplication.translate("stations_facilities_frame", u"\u8eca\u7ad9\u540d\u7a31", None))
        self.station_line_id_l.setText(QCoreApplication.translate("stations_facilities_frame", u"\u8eca\u7ad9\u8def\u7dda\u4ee3\u865f", None))
        self.station_line_id_editor.setPlaceholderText(QCoreApplication.translate("stations_facilities_frame", u"\u53ef\u8f38\u5165\u591a\u500b \u4ee5,\u5206\u9694", None))
        self.station_type_.setText(QCoreApplication.translate("stations_facilities_frame", u"\u985e\u578b", None))
        self.used_lines_l.setText(QCoreApplication.translate("stations_facilities_frame", u"\u4f7f\u7528\u672c\u8eca\u7ad9\u7684\u8def\u7dda: ", None))
#if QT_CONFIG(tooltip)
        self.delete_station_b.setToolTip(QCoreApplication.translate("stations_facilities_frame", u"\u522a\u9664\u8eca\u7ad9 \u9700\u8981\u7121\u8def\u7dda\u4f7f\u7528\u6b64\u8eca\u7ad9\u624d\u53ef\u4ee5\u522a\u9664", None))
#endif // QT_CONFIG(tooltip)
        self.delete_station_b.setText(QCoreApplication.translate("stations_facilities_frame", u"\u522a\u9664\u8eca\u7ad9", None))
        self.track_editor_l.setText(QCoreApplication.translate("stations_facilities_frame", u"  \u8eca\u7ad9/\u8a2d\u65bd\u80a1\u9053\u8a2d\u5b9a", None))
        self.add_track_b.setText(QCoreApplication.translate("stations_facilities_frame", u"\u589e\u52a0\u8eca\u7ad9\u80a1\u9053", None))
        self.connection_editor_l.setText(QCoreApplication.translate("stations_facilities_frame", u"  \u8eca\u7ad9/\u8a2d\u65bd\u9023\u63a5\u8a2d\u5b9a", None))
        self.label1.setText(QCoreApplication.translate("stations_facilities_frame", u"\u9023\u63a5\u8eca\u7ad9", None))
        self.label2.setText(QCoreApplication.translate("stations_facilities_frame", u"\u8ecc\u9053\u6578\u91cf", None))
        self.label3.setText(QCoreApplication.translate("stations_facilities_frame", u"\u9023\u63a5\u4f4d\u7f6e", None))
        self.add_connections_b.setText(QCoreApplication.translate("stations_facilities_frame", u"\u65b0\u589e\u8def\u7dda\u9023\u63a5", None))
    # retranslateUi

