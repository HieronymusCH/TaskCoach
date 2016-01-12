'''
Task Coach - Your friendly task manager
Copyright (C) 2004-2008 Frank Niessink <frank@niessink.com>

Task Coach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Task Coach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import wx
from taskcoachlib import widgets, patterns, persistence, gui


class DummyWidget(wx.Frame):
    def __init__(self, viewer):
        super(DummyWidget, self).__init__(viewer)
        self._selection = []
        self.viewer = viewer
        self.refreshedItems = []

    def DeleteAllItems(self, *args, **kwargs):
        pass

    def curselection(self):
        return self._selection

    def selection_set(self, index):
        self._selection.append(index)

    def selectall(self):
        self._selection = range(len(self.viewer.list))

    def select(self, indices):
        self._selection = indices

    def GetItemCount(self):
        return len(self.viewer.list)

    def refresh(self, *args, **kwargs):
        pass

    def RefreshItems(self, *args, **kwargs):
        pass

    def RefreshItem(self, index):
        self.refreshedItems.append(index)
        
    def refreshItem(self, index):
        self.refreshedItems.append(index)

    def GetColumnWidth(self, column):
        return 100
        
    def showSort(self, *args, **kwargs):
        pass

    def showColumn(self, *args, **kwargs):
        pass

    def showSortColumn(self, *args, **kwargs):
        pass

    def showSortOrder(self, *args, **kwargs):
        pass


class DummyUICommand(gui.uicommand.UICommand):
    bitmap = 'undo'
    section = 'view'
    setting = 'setting'

    def onCommandActivate(self, event):
        self.activated = True

    def getHelpText(self):
        return 'Help text'
    
    def getMenuText(self):
        return 'Menu text'


class DummyUICommands(gui.uicommand.UICommands):
    def __init__(self, iocontroller=None, taskList=None, effortList=None, categories=None, notes=None, viewer=None):
        super(DummyUICommands, self).__init__(None, iocontroller, viewer, None, 
                                              taskList, effortList, categories, notes)
        
    def __getitem__(self, key):
        return DummyUICommand()
        
    def keys(self):
        return ['new', 'stopeffort']


class ViewerWithDummyWidget(gui.viewer.Viewer):
    def createWidget(self):
        self._columns = self._createColumns()
        return DummyWidget(self)

    def _createColumns(self):
        return []
    
    def getItemWithIndex(self, index):
        return self.model()[index]

    
class TaskViewerWithDummyWidget(ViewerWithDummyWidget, gui.viewer.TaskViewer):
    def createWidget(self):
        self.createImageList()
        return super(TaskViewerWithDummyWidget, self).createWidget()


class TaskListViewerWithDummyWidget(TaskViewerWithDummyWidget, 
        gui.viewer.TaskListViewer):
    def _createColumns(self):
        return gui.viewer.TaskListViewer._createColumns(self)


class EffortListViewerWithDummyWidget(ViewerWithDummyWidget,
        gui.viewer.EffortListViewer):
    def createSorter(self, *args, **kwargs):
        return gui.viewer.EffortListViewer.createSorter(self, *args, **kwargs)

    def _createColumns(self):
        return gui.viewer.EffortListViewer._createColumns(self)


class EffortPerDayViewerWithDummyWidget(ViewerWithDummyWidget,
        gui.viewer.EffortPerDayViewer):
    def createSorter(self, *args, **kwargs):
        return gui.viewer.EffortPerDayViewer.createSorter(self, *args, **kwargs)

    def _createColumns(self):
        return gui.viewer.EffortPerDayViewer._createColumns(self)

        
class TaskList(patterns.ObservableList):        
    def rootItems(self):
        return [task for task in self if task.parent() is None]
    
    
class TaskFile(persistence.TaskFile):
    def load(self, *args, **kwargs):
        pass
        
    merge = save = saveas = load

class MainWindow:
    def setToolBarSize(self, *args, **kwargs):
        pass
        
    showFindDialog = setToolBarSize

class IOController:
    def needSave(self, *args, **kwargs):
        return False
