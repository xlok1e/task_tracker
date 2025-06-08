# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QPushButton, QScrollArea, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1187, 754)
        self.central_widget = QWidget(Form)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setGeometry(QRect(0, 0, 1191, 761))
        self.horizontalLayout = QHBoxLayout(self.central_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.menu = QWidget(self.central_widget)
        self.menu.setObjectName(u"menu")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu.sizePolicy().hasHeightForWidth())
        self.menu.setSizePolicy(sizePolicy)
        self.menu.setMinimumSize(QSize(250, 0))
        self.menu.setStyleSheet(u"")
        self.layoutWidget = QWidget(self.menu)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 251, 751))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setSpacing(48)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.layout_add_btn = QVBoxLayout()
        self.layout_add_btn.setSpacing(8)
        self.layout_add_btn.setObjectName(u"layout_add_btn")
        self.layout_add_btn.setContentsMargins(12, 12, 12, 12)
        self.menu_add_list_btn = QPushButton(self.layoutWidget)
        self.menu_add_list_btn.setObjectName(u"menu_add_list_btn")
        self.menu_add_list_btn.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.menu_add_list_btn.setAutoFillBackground(False)
        self.menu_add_list_btn.setStyleSheet(u"")

        self.layout_add_btn.addWidget(self.menu_add_list_btn)


        self.verticalLayout_3.addLayout(self.layout_add_btn)

        self.layout_lists = QVBoxLayout()
        self.layout_lists.setObjectName(u"layout_lists")
        self.layout_lists.setContentsMargins(12, 12, 12, 12)
        self.my_lists_text = QLabel(self.layoutWidget)
        self.my_lists_text.setObjectName(u"my_lists_text")
        self.my_lists_text.setStyleSheet(u"color: #9CA3AF;\n"
"font-weight: 500;")

        self.layout_lists.addWidget(self.my_lists_text)

        self.all_lists_area = QScrollArea(self.layoutWidget)
        self.all_lists_area.setObjectName(u"all_lists_area")
        self.all_lists_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 223, 601))
        self.all_lists_area.setWidget(self.scrollAreaWidgetContents)

        self.layout_lists.addWidget(self.all_lists_area)


        self.verticalLayout_3.addLayout(self.layout_lists)


        self.horizontalLayout.addWidget(self.menu)

        self.main_content = QStackedWidget(self.central_widget)
        self.main_content.setObjectName(u"main_content")
        self.main_content.setStyleSheet(u"")
        self.project_page = QWidget()
        self.project_page.setObjectName(u"project_page")
        self.horizontalLayoutWidget = QWidget(self.project_page)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 90, 891, 651))
        self.layout_board = QHBoxLayout(self.horizontalLayoutWidget)
        self.layout_board.setSpacing(10)
        self.layout_board.setObjectName(u"layout_board")
        self.layout_board.setContentsMargins(0, 0, 0, 0)
        self.backlog = QScrollArea(self.horizontalLayoutWidget)
        self.backlog.setObjectName(u"backlog")
        self.backlog.setWidgetResizable(True)
        self.backlog.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.column_backlog = QWidget()
        self.column_backlog.setObjectName(u"column_backlog")
        self.column_backlog.setGeometry(QRect(0, 0, 288, 647))
        self.verticalLayoutWidget_3 = QWidget(self.column_backlog)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 80, 271, 631))
        self.layout_backlog = QVBoxLayout(self.verticalLayoutWidget_3)
        self.layout_backlog.setSpacing(0)
        self.layout_backlog.setObjectName(u"layout_backlog")
        self.layout_backlog.setContentsMargins(0, 65, 0, 0)
        self.layoutWidget1 = QWidget(self.column_backlog)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(14, 24, 231, 31))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setSpacing(16)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.add_task_to_backlog = QPushButton(self.layoutWidget1)
        self.add_task_to_backlog.setObjectName(u"add_task_to_backlog")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(20)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.add_task_to_backlog.sizePolicy().hasHeightForWidth())
        self.add_task_to_backlog.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.add_task_to_backlog)

        self.backlog_text = QLabel(self.layoutWidget1)
        self.backlog_text.setObjectName(u"backlog_text")
        self.backlog_text.setStyleSheet(u"color: #9CA3AF;\n"
"font-weight: 600;\n"
"font-size: 16px;")

        self.horizontalLayout_2.addWidget(self.backlog_text)

        self.backlog.setWidget(self.column_backlog)

        self.layout_board.addWidget(self.backlog)

        self.todo = QScrollArea(self.horizontalLayoutWidget)
        self.todo.setObjectName(u"todo")
        self.todo.setWidgetResizable(True)
        self.column_todo = QWidget()
        self.column_todo.setObjectName(u"column_todo")
        self.column_todo.setGeometry(QRect(0, 0, 287, 647))
        self.verticalLayoutWidget_7 = QWidget(self.column_todo)
        self.verticalLayoutWidget_7.setObjectName(u"verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(10, 80, 271, 631))
        self.layout_todo = QVBoxLayout(self.verticalLayoutWidget_7)
        self.layout_todo.setSpacing(0)
        self.layout_todo.setObjectName(u"layout_todo")
        self.layout_todo.setContentsMargins(0, 65, 0, 0)
        self.layoutWidget_2 = QWidget(self.column_todo)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(11, 24, 251, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setSpacing(16)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.add_task_to_inprogress = QPushButton(self.layoutWidget_2)
        self.add_task_to_inprogress.setObjectName(u"add_task_to_inprogress")
        sizePolicy1.setHeightForWidth(self.add_task_to_inprogress.sizePolicy().hasHeightForWidth())
        self.add_task_to_inprogress.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.add_task_to_inprogress)

        self.inprogress_text = QLabel(self.layoutWidget_2)
        self.inprogress_text.setObjectName(u"inprogress_text")
        self.inprogress_text.setStyleSheet(u"color: #9CA3AF;\n"
"font-weight: 600;\n"
"font-size: 16px;")

        self.horizontalLayout_3.addWidget(self.inprogress_text)

        self.todo.setWidget(self.column_todo)

        self.layout_board.addWidget(self.todo)

        self.done = QScrollArea(self.horizontalLayoutWidget)
        self.done.setObjectName(u"done")
        self.done.setWidgetResizable(True)
        self.column_done = QWidget()
        self.column_done.setObjectName(u"column_done")
        self.column_done.setGeometry(QRect(0, 0, 288, 647))
        self.verticalLayoutWidget_8 = QWidget(self.column_done)
        self.verticalLayoutWidget_8.setObjectName(u"verticalLayoutWidget_8")
        self.verticalLayoutWidget_8.setGeometry(QRect(10, 80, 271, 631))
        self.layout_done = QVBoxLayout(self.verticalLayoutWidget_8)
        self.layout_done.setSpacing(0)
        self.layout_done.setObjectName(u"layout_done")
        self.layout_done.setContentsMargins(0, 65, 0, 0)
        self.layoutWidget_3 = QWidget(self.column_done)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(12, 23, 195, 31))
        self.horizontalLayout_5 = QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_5.setSpacing(16)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.add_task_to_done = QPushButton(self.layoutWidget_3)
        self.add_task_to_done.setObjectName(u"add_task_to_done")
        sizePolicy1.setHeightForWidth(self.add_task_to_done.sizePolicy().hasHeightForWidth())
        self.add_task_to_done.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.add_task_to_done)

        self.done_text_3 = QLabel(self.layoutWidget_3)
        self.done_text_3.setObjectName(u"done_text_3")
        self.done_text_3.setStyleSheet(u"color: #9CA3AF;\n"
"font-weight: 600;\n"
"font-size: 16px;")

        self.horizontalLayout_5.addWidget(self.done_text_3)

        self.done.setWidget(self.column_done)

        self.layout_board.addWidget(self.done)

        self.layoutWidget2 = QWidget(self.project_page)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(21, 30, 891, 31))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.list_name_text = QLabel(self.layoutWidget2)
        self.list_name_text.setObjectName(u"list_name_text")
        self.list_name_text.setStyleSheet(u"color: #FFF;\n"
"font-weight: 600;\n"
"font-size: 24px;")

        self.horizontalLayout_4.addWidget(self.list_name_text)

        self.edit_list_btn = QPushButton(self.layoutWidget2)
        self.edit_list_btn.setObjectName(u"edit_list_btn")
        sizePolicy1.setHeightForWidth(self.edit_list_btn.sizePolicy().hasHeightForWidth())
        self.edit_list_btn.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.edit_list_btn)

        self.main_content.addWidget(self.project_page)
        self.no_lists_page = QWidget()
        self.no_lists_page.setObjectName(u"no_lists_page")
        self.verticalLayoutWidget = QWidget(self.no_lists_page)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(40, 280, 851, 182))
        self.no_lists_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.no_lists_layout.setSpacing(0)
        self.no_lists_layout.setObjectName(u"no_lists_layout")
        self.no_lists_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.no_lists_layout.setContentsMargins(0, 0, 0, 0)
        self.welcome_label = QLabel(self.verticalLayoutWidget)
        self.welcome_label.setObjectName(u"welcome_label")
        self.welcome_label.setMaximumSize(QSize(16777215, 100))
        self.welcome_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.welcome_label.setStyleSheet(u"font: 48pt \"Google Sans\";\n"
"font-weight: 500;")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.no_lists_layout.addWidget(self.welcome_label)

        self.welcome_label_2 = QLabel(self.verticalLayoutWidget)
        self.welcome_label_2.setObjectName(u"welcome_label_2")
        self.welcome_label_2.setMaximumSize(QSize(16777215, 100))
        self.welcome_label_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.welcome_label_2.setStyleSheet(u"font: 20pt \"Google Sans\";")
        self.welcome_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.no_lists_layout.addWidget(self.welcome_label_2)

        self.main_screen_add_project_btn = QPushButton(self.verticalLayoutWidget)
        self.main_screen_add_project_btn.setObjectName(u"main_screen_add_project_btn")
        self.main_screen_add_project_btn.setMaximumSize(QSize(16777215, 16777215))
        self.main_screen_add_project_btn.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.main_screen_add_project_btn.setAutoFillBackground(False)
        self.main_screen_add_project_btn.setStyleSheet(u"")

        self.no_lists_layout.addWidget(self.main_screen_add_project_btn)

        self.main_content.addWidget(self.no_lists_page)

        self.horizontalLayout.addWidget(self.main_content)


        self.retranslateUi(Form)

        self.main_content.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.menu_add_list_btn.setText(QCoreApplication.translate("Form", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0440\u043e\u0435\u043a\u0442", None))
        self.my_lists_text.setText(QCoreApplication.translate("Form", u"\u041c\u043e\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u044b", None))
        self.add_task_to_backlog.setText(QCoreApplication.translate("Form", u"+", None))
        self.backlog_text.setText(QCoreApplication.translate("Form", u"BACKLOG (0)", None))
        self.add_task_to_inprogress.setText(QCoreApplication.translate("Form", u"+", None))
        self.inprogress_text.setText(QCoreApplication.translate("Form", u"IN PROGRESS (0)", None))
        self.add_task_to_done.setText(QCoreApplication.translate("Form", u"+", None))
        self.done_text_3.setText(QCoreApplication.translate("Form", u"DONE (0)", None))
        self.list_name_text.setText(QCoreApplication.translate("Form", u"\u0421\u043f\u0438\u0441\u043e\u043a 1", None))
        self.edit_list_btn.setText(QCoreApplication.translate("Form", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043f\u0440\u043e\u0435\u043a\u0442", None))
        self.welcome_label.setText(QCoreApplication.translate("Form", u"\u0414\u043e\u0431\u0440\u043e \u043f\u043e\u0436\u0430\u043b\u043e\u0432\u0430\u0442\u044c!", None))
        self.welcome_label_2.setText(QCoreApplication.translate("Form", u"\u041d\u0430\u0447\u043d\u0438\u0442\u0435 \u0441 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f \u043f\u0435\u0440\u0432\u043e\u0433\u043e \u043f\u0440\u043e\u0435\u043a\u0442\u0430", None))
        self.main_screen_add_project_btn.setText(QCoreApplication.translate("Form", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u0440\u043e\u0435\u043a\u0442", None))
    # retranslateUi

