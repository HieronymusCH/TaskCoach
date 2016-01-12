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
from taskcoachlib import patterns
from taskcoachlib.domain import task
from taskcoachlib.i18n import _
import uicommand


class Menu(wx.Menu, uicommand.UICommandContainer):
    def __init__(self, window):
        super(Menu, self).__init__()
        self._window = window
        
    def __len__(self):
        return self.GetMenuItemCount()

    def appendUICommand(self, uiCommand):
        return uiCommand.appendToMenu(self, self._window)    
    
    def appendMenu(self, text, subMenu, bitmap=None):
        subMenuItem = wx.MenuItem(self, id=wx.NewId(), text=text, subMenu=subMenu)
        if not bitmap and '__WXMSW__' in wx.PlatformInfo:
            # hack to force a 16 bit margin. SetMarginWidth doesn't work
            bitmap = 'nobitmap'
        if bitmap:
            subMenuItem.SetBitmap(wx.ArtProvider_GetBitmap(bitmap, 
                wx.ART_MENU, (16,16)))
        self.AppendItem(subMenuItem)

    def invokeMenuItem(self, menuItem):
        ''' Programmatically invoke the menuItem. This is mainly for testing 
            purposes. '''
        self._window.ProcessEvent(wx.CommandEvent( \
            wx.wxEVT_COMMAND_MENU_SELECTED, winid=menuItem.GetId()))
    
    def openMenu(self):
        ''' Programmatically open the menu. This is mainly for testing 
            purposes. '''
        # On Mac OSX, an explicit UpdateWindowUI is needed to ensure that
        # menu items are updated before the menu is opened. This is not needed
        # on other platforms, but it doesn't hurt either.
        self._window.UpdateWindowUI() 
        self._window.ProcessEvent(wx.MenuEvent(wx.wxEVT_MENU_OPEN, menu=self))


class StaticMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(StaticMenu, self).__init__(mainwindow)
        wx.CallAfter(self.appendUICommands, uiCommands, self.getUICommands())
        
    def getUICommands(self):
        raise NotImplementedError


class DynamicMenu(Menu):
    ''' A menu that registers for events and then updates itself whenever the
        event is fired. '''
    def __init__(self, mainwindow, parentMenu, labelInParentMenu):
        ''' Initialize the menu. labelInParentMenu is needed to be able to
            find this menu in its parentMenu. '''
        super(DynamicMenu, self).__init__(mainwindow)
        self._parentMenu = parentMenu
        self._labelInParentMenu = self.__GetLabelText(labelInParentMenu)
        self.registerForMenuUpdate()
        self.updateMenu()
         
    def registerForMenuUpdate(self):
        ''' Subclasses are responsible for binding an event to onUpdateMenu so
            that the menu gets a chance to update itself at the right time. '''
        raise NotImplementedError

    def onUpdateMenu(self, event):
        ''' This event handler should be called at the right times so that
            the menu has a chance to update itself. '''
        # If this is called by wx, 'skip' the event so that other event
        # handlers get a chance too:
        if hasattr(event, 'Skip'):
            event.Skip()
        self.updateMenu()
        
    def updateMenu(self):
        ''' Updating the menu consists of two steps: updating the menu item
            of this menu in its parent menu, e.g. to enable or disable it, and
            updating the menu items of this menu. '''
        self.updateMenuItemInParentMenu()
        self.updateMenuItems()
        
    def clearMenu(self):
        ''' Remove all menu items. '''
        for menuItem in self.MenuItems:
            self.DestroyItem(menuItem)       
            
    def updateMenuItemInParentMenu(self):
        ''' Enable or disable the menu item in the parent menu, depending on
            what enabled() returns. '''
        if self._parentMenu:
            # I'd rather use wx.Menu.FindItem, but it seems that that 
            # method currently does not work for menu items with accelerators 
            # (wxPython 2.8.6 on Ubuntu). When that is fixed replace the 7
            # lines below with this one:
            # myId = self._parentMenu.FindItem(self._labelInParentMenu)
            for item in self._parentMenu.MenuItems:
                if self.__GetLabelText(item.GetText()) == self._labelInParentMenu:
                    myId = item.Id
                    break
            else:
                myId = wx.NOT_FOUND
            if myId != wx.NOT_FOUND:
                self._parentMenu.Enable(myId, self.enabled())

    def updateMenuItems(self):
        ''' Update the menu items of this menu. '''
        pass
    
    def enabled(self):
        ''' Return a boolean indicating whether this menu should be enabled in
            its parent menu. This method is called by 
            updateMenuItemInParentMenu(). It returns True by default. Override
            in a subclass as needed.'''
        return True
    
    @staticmethod
    def __GetLabelText(menuText):
        ''' Remove accelerators from the menuText. This is necessary because on
            some platforms '&' is changed into '_' so menuTexts would compare
            different even though they are really the same. '''
        return menuText.replace('&', '').replace('_', '')

            
class DynamicMenuThatGetsUICommandsFromViewer(DynamicMenu):
    def __init__(self, mainwindow, uiCommands, parentMenu=None, 
                 labelInParentMenu=None):
        self._uiCommands = uiCommands
        self._uiCommandNames = None
        super(DynamicMenuThatGetsUICommandsFromViewer, self).__init__(\
            mainwindow, parentMenu, labelInParentMenu)

    def registerForMenuUpdate(self):
        # I would've liked to update the menu whenever the active viewer 
        # changes but with the aui managed frame there is no way that I know of 
        # to get notified when the active frame (i.e. viewer) changes. So, 
        # we'll just have to update the menu whenever it is opened:
        self._window.Bind(wx.EVT_MENU_OPEN, self.onUpdateMenu)
        
    def updateMenuItems(self):
        newCommandNames = self.getUICommands()
        if newCommandNames != self._uiCommandNames:
            self.clearMenu()
            self.fillMenu(newCommandNames)
            self._uiCommandNames = newCommandNames
        
    def fillMenu(self, commandNames):
        self.appendUICommands(self._uiCommands, commandNames)
        
    def getUICommands(self):
        raise NotImplementedError


class MainMenu(wx.MenuBar):
    def __init__(self, mainwindow, uiCommands, settings):
        super(MainMenu, self).__init__()
        self.Append(FileMenu(mainwindow, uiCommands, settings), _('&File'))
        self.Append(EditMenu(mainwindow, uiCommands), _('&Edit'))
        self.Append(ViewMenu(mainwindow, uiCommands, settings), _('&View'))
        self.Append(TaskMenu(mainwindow, uiCommands), _('&Task'))
        self.Append(EffortMenu(mainwindow, uiCommands), _('Eff&ort'))
        self.Append(CategoryMenu(mainwindow, uiCommands), _('&Category'))
        if settings.getboolean('feature', 'notes'):
            self.Append(NoteMenu(mainwindow, uiCommands), _('&Note'))
        self.Append(HelpMenu(mainwindow, uiCommands), _('&Help'))

'''
class OpenAttachmentsMenu(Menu):
    def __init__(self, mainwindow, uiCommands, settings):
        super(OpenAttachmentsMenu, self).__init__(mainwindow)
        self.Bind(wx.EVT_MENU_OPEN, self.onOpenMenu)
        
    def opOpenMenu(self, event):
        if event.GetMenu() == self:
            self.__clear()
            self.__fill()
        event.Skip()
        
    def __clear(self):
        for item in self.GetMenuItems():
            self.Delete(item)
            
    def __fill(self):
        pass
'''
       
class FileMenu(Menu):
    def __init__(self, mainwindow, uiCommands, settings):
        super(FileMenu, self).__init__(mainwindow)
        self.__settings = settings
        self.__uiCommands = uiCommands
        self.__recentFileUICommands = []
        self.__separator = None
        self.appendUICommands(uiCommands, ['open', 'merge', 'close', None, 
            'save', 'saveas', 'saveselection', None, 'printpagesetup',
            'printpreview', 'print', None])
        self.appendMenu(_('&Export'), ExportMenu(mainwindow, uiCommands),
            'export')
        try:
            import _pysyncml
        except ImportError, e:
            pass
        else:
            self.appendUICommands(uiCommands, [None, 'synchronize'])
        self.__recentFilesStartPosition = len(self) 
        self.appendUICommands(uiCommands, [None, 'quit'])
        self._window.Bind(wx.EVT_MENU_OPEN, self.onOpenMenu)

    def onOpenMenu(self, event):
        if event.GetMenu() == self:
            self.__removeRecentFileMenuItems()
            self.__insertRecentFileMenuItems()        
        event.Skip()
    
    def __insertRecentFileMenuItems(self):
        recentFiles = eval(self.__settings.get('file', 'recentfiles'))
        if not recentFiles:
            return
        maximumNumberOfRecentFiles = self.__settings.getint('file', 
            'maxrecentfiles')
        recentFiles = recentFiles[:maximumNumberOfRecentFiles]
        self.__separator = self.InsertSeparator(self.__recentFilesStartPosition)
        for index, recentFile in enumerate(recentFiles):
            recentFileNumber = index + 1 # Only computer nerds start counting at 0 :-)
            recentFileMenuPosition = self.__recentFilesStartPosition + 1 + index
            recentFileOpenUICommand = self.__uiCommands.createRecentFileOpenUICommand(recentFile, recentFileNumber)
            recentFileOpenUICommand.appendToMenu(self, self._window, 
                recentFileMenuPosition)
            self.__recentFileUICommands.append(recentFileOpenUICommand)

    def __removeRecentFileMenuItems(self):
        for recentFileUICommand in self.__recentFileUICommands:
            recentFileUICommand.removeFromMenu(self, self._window)
        self.__recentFileUICommands = []
        if self.__separator:
            self.RemoveItem(self.__separator)
            self.__separator = None


class ExportMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(ExportMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['exportashtml', 'exportasics', 
                                           'exportascsv'])
        

class EditMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(EditMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['undo', 'redo', None, 'cut', 
            'copy', 'paste', 'pasteintotask', None])
        # the spaces are to leave room for command names in the Undo and Redo menuitems:
        self.appendMenu(_('&Select')+' '*50, SelectMenu(mainwindow, uiCommands))
        self.appendUICommands(uiCommands, [None, 'editpreferences'])
        try:
            import _pysyncml
        except ImportError:
            pass
        else:
            self.appendUICommands(uiCommands, ['editsyncpreferences'])


class SelectMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(SelectMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['selectall', 'invertselection', 
            'clearselection'])


class ViewMenu(Menu):
    def __init__(self, mainwindow, uiCommands, settings):
        super(ViewMenu, self).__init__(mainwindow)
        self.appendMenu(_('&New viewer'), 
            ViewViewerMenu(mainwindow, uiCommands, settings), 'viewnewviewer')
        self.appendUICommands(uiCommands,
            ['activatenextviewer', 'activatepreviousviewer', 'renameviewer', 
             None])
        self.appendMenu(_('&Filter'), 
            FilterMenu(mainwindow, uiCommands, self, _('&Filter')))
        self.appendMenu(_('&Sort'),
            SortMenu(mainwindow, uiCommands, self, _('&Sort')))
        self.appendMenu(_('&Columns'), 
            ColumnMenu(mainwindow, uiCommands, self, _('&Columns')))
        self.appendUICommands(uiCommands, [None])
        self.appendMenu(_('&Tree options'), 
            ViewTreeOptionsMenu(mainwindow, uiCommands), 'treeview')
        self.appendUICommands(uiCommands, [None])
        self.appendMenu(_('T&oolbar'), ToolBarMenu(mainwindow, uiCommands))        
        self.appendUICommands(uiCommands, ['viewstatusbar'])   


class ViewViewerMenu(Menu):
    def __init__(self, mainwindow, uiCommands, settings):
        super(ViewViewerMenu, self).__init__(mainwindow)
        viewViewerCommands = ['viewtasklistviewer', 
            'viewtasktreeviewer', None, 'viewcategoryviewer', None,
            'vieweffortdetailviewer', 'vieweffortperdayviewer', 
            'vieweffortperweekviewer', 'vieweffortpermonthviewer']
        if settings.getboolean('feature', 'notes'):
            viewViewerCommands.extend([None, 'viewnoteviewer'])
        self.appendUICommands(uiCommands, viewViewerCommands)
        
                                      
class ViewTreeOptionsMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(ViewTreeOptionsMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['viewexpandselected', 
            'viewcollapseselected', None, 'viewexpandall', 'viewcollapseall'])


class FilterMenu(DynamicMenuThatGetsUICommandsFromViewer):
    def enabled(self):
        return self._window.viewer.isFilterable() and \
            bool(self._window.viewer.getFilterUICommands())
    
    def getUICommands(self):
        return self._window.viewer.getFilterUICommands()
    
    
class ColumnMenu(DynamicMenuThatGetsUICommandsFromViewer):
    def enabled(self):
        return self._window.viewer.hasHideableColumns()
    
    def getUICommands(self):
        return self._window.viewer.getColumnUICommands()
        

class SortMenu(DynamicMenuThatGetsUICommandsFromViewer):
    def enabled(self):
        return self._window.viewer.isSortable()
    
    def getUICommands(self):
        return self._window.viewer.getSortUICommands()


class ToolBarMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(ToolBarMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['toolbarhide', 'toolbarsmall',
            'toolbarmedium', 'toolbarbig'])


class TaskMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(TaskMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['newtask', 'newsubtask', None, 
            'edittask', 'toggletaskcompletion', 'incpriority', 'decpriority',
            'maxpriority', 'minpriority', None, 'deletetask', None, 
            'mailtask', 'addattachmenttotask', 'openalltaskattachments'])
            
            
class EffortMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(EffortMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['neweffort', 'editeffort', 
            'deleteeffort', None, 'starteffort', 'stopeffort'])
        

class CategoryMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(CategoryMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['newcategory', 'newsubcategory', 
            'editcategory', 'deletecategory'])
        
        
class NoteMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(NoteMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['newnote', 'newsubnote', 'editnote',
            'deletenote'])
        
        
class HelpMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(HelpMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['help', 'tips', None, 'about', 'license'])


class TaskBarMenu(Menu):
    def __init__(self, taskBarIcon, uiCommands, tasks):
        super(TaskBarMenu, self).__init__(taskBarIcon)
        self.appendUICommands(uiCommands, ['newtask', 'neweffort', None])
        label = _('&Start tracking effort')
        self.appendMenu(label,
            StartEffortForTaskMenu(taskBarIcon, tasks, self, label), 'start')                      
        self.appendUICommands(uiCommands, ['stopeffort', None, 'restore', 
                                           'quit'])
        
                   
class StartEffortForTaskMenu(DynamicMenu):
    def __init__(self, taskBarIcon, tasks, parentMenu, labelInParentMenu):
        self.tasks = tasks
        super(StartEffortForTaskMenu, self).__init__(taskBarIcon, parentMenu, 
                                                     labelInParentMenu)

    def registerForMenuUpdate(self):
        for eventType in (self.tasks.addItemEventType(), 
                          self.tasks.removeItemEventType(),
                          task.Task.subjectChangedEventType(),
                          'task.track.start', 'task.track.stop',
                          'task.startDate', 'task.dueDate', 
                          'task.completionDate'):
            patterns.Publisher().registerObserver(self.onUpdateMenu, eventType)
    
    def updateMenuItems(self):
        self.clearMenu()
        activeRootTasks = self._activeRootTasks()
        activeRootTasks.sort(key=lambda task: task.subject())
        for task in activeRootTasks:
            self.addMenuItemForTask(task, self)
                
    def addMenuItemForTask(self, task, menu):
        uiCommand = uicommand.EffortStartForTask(task=task, taskList=self.tasks)
        uiCommand.appendToMenu(menu, self._window)
        activeChildren = [child for child in task.children() if child.active()]
        if activeChildren:
            activeChildren.sort(key=lambda task: task.subject())
            subMenu = wx.Menu()
            for child in activeChildren:
                self.addMenuItemForTask(child, subMenu)
            menu.AppendSubMenu(subMenu, _('%s (subtasks)')%task.subject())
                        
    def enabled(self):
        return bool(self._activeRootTasks())

    def _activeRootTasks(self):
        return [task for task in self.tasks.rootItems() if task.active()]
    

class TaskPopupMenu(Menu):
    def __init__(self, mainwindow, uiCommands, treeViewer):
        super(TaskPopupMenu, self).__init__(mainwindow)
        commandsToAppend = ['cut', 'copy', 'paste',
            'pasteintotask', None, 'newtask', 'newsubtask', None, 'edittask', 
            'toggletaskcompletion', 'incpriority', 'decpriority', 'maxpriority', 
            'minpriority', None, 'deletetask', None, 'mailtask', 
            'addattachmenttotask', 'openalltaskattachments', None, 'neweffort', 
            'starteffort', 'stopeffort']
        if treeViewer:
            commandsToAppend.extend([None, 'viewexpandselected', 
                'viewcollapseselected'])
        self.appendUICommands(uiCommands, commandsToAppend)


class EffortPopupMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(EffortPopupMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['cut', 'copy', 'paste', 
           'pasteintotask', None, 'newtask', None, 'neweffort', 'editeffort', 
           'deleteeffort', None, 'stopeffort'])


class CategoryPopupMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(CategoryPopupMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['cut', 'copy', 'paste', None, 
            'newtaskwithselectedcategories', None, 'newcategory', 
            'newsubcategory', 'editcategory', 'deletecategory', None, 
            'stopeffort', None, 'viewexpandselected', 'viewcollapseselected'])


class NotePopupMenu(Menu):
    def __init__(self, mainwindow, uiCommands):
        super(NotePopupMenu, self).__init__(mainwindow)
        self.appendUICommands(uiCommands, ['cut', 'copy', 'paste', None,
            'newtask', None, 'newnote', 'newsubnote', 'editnote', 'deletenote',
            None, 'stopeffort', None, 'viewexpandselected', 
            'viewcollapseselected'])
        
        
# Column header popup menu

class ColumnPopupMenu(StaticMenu):           
    def __setColumn(self, columnIndex):
        self.__columnIndex = columnIndex
    
    def __getColumn(self):
        return self.__columnIndex
    
    # columnIndex is the index of the column clicked by the user to popup this menu
    # This property should be set by the control popping up this menu (see 
    # widgets._CtrlWithColumnPopupMenu.
    columnIndex = property(__getColumn, __setColumn) 
                            
    def getUICommands(self):
        return ['hidecurrentcolumn', None] + \
            self._window.getColumnUICommands()

