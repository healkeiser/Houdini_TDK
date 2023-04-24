# -*- coding: utf-8 -*-
"""_summary_"""

# Libraries
from __future__ import print_function
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

# TODO: Disable for release
# from importlib import reload

# Metadatas
__author__ = "Ivan Titov, Valentin Beaumont"
__email__ = "valentin.onze@gmail.com"


###### CODE ####################################################################


def fuzzyMatch(pattern, text):
    if pattern == text:
        return True, 999999

    try:
        pattern_start = text.index(pattern)
        pattern_length = len(pattern)
        return True, pattern_length * pattern_length + (1 - pattern_start / 500.0)
    except ValueError:
        pass

    weight = 0
    count = 0
    index = 0
    for char in text:
        try:
            if char == pattern[index]:
                count += 1
                index += 1
            elif count != 0:
                weight += count * count
                count = 0
        except IndexError:
            pass

    weight += count * count
    if index < len(pattern):
        return False, weight

    return True, weight + (1 - text.index(pattern[0]) / 500.0)


class FuzzyFilterProxyModel(QSortFilterProxyModel):
    def __init__(
        self, parent=None, accept_text_role=Qt.UserRole, comp_text_role=Qt.DisplayRole
    ):
        super(FuzzyFilterProxyModel, self).__init__(parent)

        self._accept_text_role = accept_text_role
        self.comp_text_role = comp_text_role

        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.sort(0, Qt.DescendingOrder)

        self._pattern = ""

    def setFilterPattern(self, pattern):
        self._pattern = pattern.lower()
        self.invalidate()

    def filterAcceptsRow(self, source_row, source_parent):
        if not self._pattern:
            return True

        source_model = self.sourceModel()
        text = source_model.data(
            source_model.index(source_row, 0, source_parent), self._accept_text_role
        )
        matches, _ = fuzzyMatch(self._pattern, text.lower())
        return matches

    def lessThan(self, source_left, source_right):
        if not self._pattern:
            return source_left.row() < source_right.row()

        text1 = source_left.data(self.comp_text_role)
        _, weight1 = fuzzyMatch(self._pattern, text1.lower())

        text2 = source_right.data(self.comp_text_role)
        _, weight2 = fuzzyMatch(self._pattern, text2.lower())

        return weight1 < weight2
