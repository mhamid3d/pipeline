from qtpy import QtWidgets, QtGui, QtCore


def h_line():
    frame = QtWidgets.QFrame()
    frame.setFrameShape(QtWidgets.QFrame.HLine)
    frame.setFixedHeight(2)
    frame.setStyleSheet("""
        QFrame{
            background: #3e3e3e;
            border: 0px;
        }""")

    return frame


def v_line():
    frame = QtWidgets.QFrame()
    frame.setFrameShape(QtWidgets.QFrame.VLine)
    frame.setFixedWidth(2)
    frame.setStyleSheet("""
        QFrame{
            background: #3e3e3e;
            border: 0px;
        }""")

    return frame


def get_settings(appName="Comet Browser"):
    return QtCore.QSettings("Comet Pipeline", appName)


def get_top_window(fromObject, topClass):
    w = fromObject.parent()
    while w.parent():
        w = w.parent()

    assert isinstance(w, topClass), "Could not find valid top window of instance {}. Got {} instead".format(str(topClass), str(w))

    return w


class FlatIconButton(QtWidgets.QPushButton):
    def __init__(self, size=32, icon=None):
        super(FlatIconButton, self).__init__()
        self.setFixedSize(size, size)
        self.setIcon(QtGui.QIcon(icon))
        self.setStyleSheet("""
            QPushButton{
                background: none;
                border-radius: %spx;
                border: none;
            }
            QPushButton:pressed{
                background: #4e4e4e;
            }
            QPushButton:checked{
                background: #5e5e5e;
            }
        """ % (size / 2))
        self.setCursor(QtCore.Qt.PointingHandCursor)


class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setMargin(margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self._doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QtCore.QSize(2 * self.margin(), 2 * self.margin())
        return size

    def _doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(
                QtWidgets.QSizePolicy.PushButton,
                QtWidgets.QSizePolicy.PushButton,
                QtCore.Qt.Horizontal)

            spaceY = self.spacing() + wid.style().layoutSpacing(
                QtWidgets.QSizePolicy.PushButton,
                QtWidgets.QSizePolicy.PushButton,
                QtCore.Qt.Vertical)

            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()