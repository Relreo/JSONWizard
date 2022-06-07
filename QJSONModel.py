"""Python adaptation of https://github.com/dridk/QJsonModel

Tweaked for JSONWizard project by Ian Maynard

Supports Python 2 and 3 with PySide, PySide2, PyQt4 or PyQt5.
Requires https://github.com/mottosso/Qt.py

Changes:
    This module differs from the C++ version in the following ways.

    1. Setters and getters are replaced by Python properties
    2. Objects are sorted by default, disabled via load(sort=False)
    3. load() takes a Python dictionary as opposed to
       a string or file handle.

        - To load from a string, use built-in `json.loads()`
            >>> import json
            >>> document = json.loads("{'key': 'value'}")
            >>> model.load(document)

        - To load from a file, use `with open(fname)`
              >>> import json
              >>> with open("file.json") as f:
              ...    document = json.load(f)
              ...    model.load(document)

"""
from PySide2 import QtCore

class QJsonTreeItem(object):
    def __init__(self, parent=None):
        self._parent = parent

        self._key = ""
        self._value = ""
        self._type = None
        self._children = list()

    def appendChild(self, item):
        self._children.append(item)
    
    def removeChild(self, item):
        self._children.remove(item)

    def child(self, row):
        return self._children[row]

    def parent(self):
        return self._parent

    def childCount(self):
        return len(self._children)

    def row(self):
        return (
            self._parent._children.index(self)
            if self._parent else 0
        )
    
    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, typ):
        self._type = typ

    @classmethod
    def load(self, value, parent=None, sort=False):
        rootItem = QJsonTreeItem(parent)
        rootItem.key = "root"

        if isinstance(value, dict):
            items = (
                sorted(value.items())
                if sort else value.items()
            )

            for key, value in items:
                # rootItem.value = "**JSON Object**"
                child = self.load(value, rootItem)
                child.key = key
                child.type = type(value)
                rootItem.appendChild(child)

        elif isinstance(value, list):
            # rootItem.value = "**JSON Array**"
            for index, value in enumerate(value):
                child = self.load(value, rootItem)
                child.key = index
                child.type = type(value)
                rootItem.appendChild(child)

        else:
            rootItem.value = value
            rootItem.type = type(value)

        return rootItem

class QJsonModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super(QJsonModel, self).__init__(parent)

        self._rootItem = QJsonTreeItem()
        self._headers = ("Key", "Value")

    def clear(self):
        self.load({})

    def insertRow(self, currentIndex: QtCore.QModelIndex, itemType: str | list | dict, parent: QtCore.QModelIndex) -> bool:
        return self.insertRows(currentIndex, 1, itemType, parent)

    def insertRows(self, currentIndex: QtCore.QModelIndex, count: int, itemType: str | list | dict, parent: QtCore.QModelIndex) -> bool:
        row = 0
        if currentIndex:
            row = currentIndex.row()

        if count <= 0 or row < 0:
            return False

        parentItem = self.data(parent, QtCore.Qt.EditRole)
        
        if not parentItem or not currentIndex:
            parentItem = self._rootItem
        else:
            currentItem = self.data(currentIndex, QtCore.Qt.EditRole)
            parentItem = self.data(parent, QtCore.Qt.EditRole)
            if currentItem:
                if currentItem.type is list or currentItem.type is dict:
                    parentItem = currentItem
            
        

        newItem = QJsonTreeItem(parentItem)
        newItem.type = itemType
        if parentItem.type is list:
            newItem.key = parentItem.childCount()
        elif parentItem.type is dict:
            if itemType is list:
                newItem.key = "**UNNAMED ARRAY**"
            elif itemType is dict:
                newItem.key = "**UNNAMED OBJECT**"
            else:
                newItem.key = "**KEY**"
        if itemType is str:
            newItem.value = "**VALUE**"

        self.beginInsertRows(parent, row, row + count - 1)
        parentItem.appendChild(newItem)
        self.endInsertRows()

        return True

    def removeRows(self, row: int, count: int, parent: QtCore.QModelIndex = ...) -> bool:
        if count <= 0 or row < 0 or (row + count) > self.rowCount(parent):
            return False
        
        self.beginRemoveRows(parent, row, row + count - 1)
        
        parentItem = self.data(parent, QtCore.Qt.EditRole)
        if not parentItem:
            parentItem = self._rootItem

        for n in range(row, row + count):
            parentItem.removeChild(parentItem.child(n))
        if parentItem.type is list:
            for n in range(row + count - 1, parentItem.childCount()):
                currentKey = parentItem.child(n).key
                parentItem.child(n).key = currentKey - count


        self.endRemoveRows()

        return True

    def load(self, document):
        """Load from dictionary

        Arguments:
            document (dict): JSON-compatible dictionary

        """

        assert isinstance(document, (dict, list, tuple)), (
            "`document` must be of dict, list or tuple, "
            "not %s" % type(document)
        )

        self.beginResetModel()

        self._rootItem = QJsonTreeItem.load(document)
        self._rootItem.type = type(document)

        self.endResetModel()

        return True

    def json(self, root=None):
        """Serialise model as JSON-compliant dictionary

        Arguments:
            root (QJsonTreeItem, optional): Serialise from here
                defaults to the the top-level item

        Returns:
            model as dict

        """

        root = root or self._rootItem
        return self.genJson(root)

    def data(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return item.key

            if index.column() == 1:
                return item.value

        elif role == QtCore.Qt.EditRole:
            return item

    def setData(self, index, value, role):
        valueString = str(value)
        if valueString == "":
            return False

        if role == QtCore.Qt.EditRole:
            item = index.internalPointer()
            if index.column() == 1:
                if item.type != list and item.type != dict:
                    if valueString.isdigit():
                        item.value = int(valueString)
                        item.type = int
                    elif valueString == "null":
                        item.value = None
                        item.type = None
                    elif (valueString == "true") | (valueString == "True"):
                        item.value = True
                        item.type = bool
                    elif (valueString == "false") | (valueString == "False"):
                        item.value = False
                        item.type = bool
                    else:
                        item.value = valueString
                        item.type = str
            else:
                if item.parent().type != list:
                    item.key = valueString

            self.dataChanged.emit(index, index, [QtCore.Qt.EditRole])

            return True

        return False

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            return self._headers[section]

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self._rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 2

    def flags(self, index):
        flags = super(QJsonModel, self).flags(index)

        return QtCore.Qt.ItemIsEditable | flags

    def genJson(self, item):
        nchild = item.childCount()

        if item.type is dict:
            document = {}
            for i in range(nchild):
                ch = item.child(i)
                document[ch.key] = self.genJson(ch)
            return document

        elif item.type == list:
            document = []
            for i in range(nchild):
                ch = item.child(i)
                document.append(self.genJson(ch))
            return document

        else:
            return item.value

