# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'train_levels_editor.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(525, 352)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.upper_frame = QFrame(Form)
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
        self.label1 = QLabel(self.upper_frame)
        self.label1.setObjectName(u"label1")

        self.horizontalLayout.addWidget(self.label1)

        self.train_level_name_input = QLineEdit(self.upper_frame)
        self.train_level_name_input.setObjectName(u"train_level_name_input")
        self.train_level_name_input.setMinimumSize(QSize(20, 0))
        self.train_level_name_input.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout.addWidget(self.train_level_name_input)

        self.label2 = QLabel(self.upper_frame)
        self.label2.setObjectName(u"label2")

        self.horizontalLayout.addWidget(self.label2)

        self.train_level_priority_input = QLineEdit(self.upper_frame)
        self.train_level_priority_input.setObjectName(u"train_level_priority_input")
        self.train_level_priority_input.setMinimumSize(QSize(20, 0))
        self.train_level_priority_input.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout.addWidget(self.train_level_priority_input)

        self.label3 = QLabel(self.upper_frame)
        self.label3.setObjectName(u"label3")

        self.horizontalLayout.addWidget(self.label3)

        self.comboBox = QComboBox(self.upper_frame)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.comboBox)

        self.add_train_level_b = QPushButton(self.upper_frame)
        self.add_train_level_b.setObjectName(u"add_train_level_b")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.add_train_level_b.sizePolicy().hasHeightForWidth())
        self.add_train_level_b.setSizePolicy(sizePolicy1)
        self.add_train_level_b.setMinimumSize(QSize(80, 0))
        self.add_train_level_b.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.add_train_level_b)

        self.delete_train_level_b = QPushButton(self.upper_frame)
        self.delete_train_level_b.setObjectName(u"delete_train_level_b")
        sizePolicy1.setHeightForWidth(self.delete_train_level_b.sizePolicy().hasHeightForWidth())
        self.delete_train_level_b.setSizePolicy(sizePolicy1)
        self.delete_train_level_b.setMinimumSize(QSize(80, 0))
        self.delete_train_level_b.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.delete_train_level_b)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.upper_frame)

        self.main_table = QTableWidget(Form)
        self.main_table.setObjectName(u"main_table")
        self.main_table.setAlternatingRowColors(True)

        self.verticalLayout.addWidget(self.main_table)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label1.setText(QCoreApplication.translate("Form", u"\u5217\u8eca\u7b49\u7d1a\u540d", None))
        self.label2.setText(QCoreApplication.translate("Form", u"\u5217\u8eca\u512a\u5148\u5ea6", None))
        self.label3.setText(QCoreApplication.translate("Form", u"\u65b9\u5411", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"\u4e0a\u884c", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"\u4e0b\u884c", None))

#if QT_CONFIG(tooltip)
        self.add_train_level_b.setToolTip(QCoreApplication.translate("Form", u"\u65b0\u589e\u8eca\u7ad9", None))
#endif // QT_CONFIG(tooltip)
        self.add_train_level_b.setText(QCoreApplication.translate("Form", u"\u65b0\u589e\u5217\u8eca\u7b49\u7d1a", None))
        self.delete_train_level_b.setText(QCoreApplication.translate("Form", u"\u522a\u9664\u5217\u8eca\u7b49\u7d1a", None))
    # retranslateUi

