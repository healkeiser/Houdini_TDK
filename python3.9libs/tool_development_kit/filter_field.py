# -*- coding: utf-8 -*-
"""_summary_"""

# Libraries
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

# Files
from tool_development_kit.input_field import InputField

# TODO: Disable for release
# from importlib import reload

# Metadatas
__author__ = "Ivan Titov, Valentin Beaumont"
__email__ = "valentin.onze@gmail.com"


###### CODE ####################################################################


class FilterField(InputField):
    # Signals
    accepted = Signal(str)

    def __init__(self):
        super(FilterField, self).__init__()
        self.setPlaceholderText("Type to Filter...")

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Enter or key == Qt.Key_Return:
            self.accepted.emit(self.text())
        else:
            super(FilterField, self).keyPressEvent(event)
