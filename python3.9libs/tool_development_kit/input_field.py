# -*- coding: utf-8 -*-
"""_summary_"""

# Libraries
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

# Metadatas
__author__ = "Ivan Titov, Valentin Beaumont"
__email__ = "valentin.onze@gmail.com"


###### CODE ####################################################################


class InputField(QLineEdit):
    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Cancel):
            self.clear()
        else:
            super(InputField, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        if (
            event.button() == Qt.MiddleButton
            and event.modifiers() == Qt.ControlModifier
        ):
            self.clear()
        else:
            super(InputField, self).mousePressEvent(event)
