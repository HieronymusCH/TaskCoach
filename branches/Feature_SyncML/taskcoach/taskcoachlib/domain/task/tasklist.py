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
from taskcoachlib.i18n import _
from taskcoachlib.domain import date
import task


def newTaskMenuText():
    # There is a bug in wxWidget/wxPython on the Mac that causes the 
    # INSERT accelerator to be mapped so some other key sequence ('c' in
    # this case) so that whenever that key sequence is typed, this command
    # is invoked. Hence, we use a different accelarator on the Mac.
    menuText = _('&New task...')
    if '__WXMAC__' in wx.PlatformInfo:
        menuText += u'\tCtrl+N'
    else:
        menuText += u'\tCtrl+INS'
    return menuText

def newSubTaskMenuText():
    # See comments in newTaskMenuText() above
    menuText = _('New &subtask...')
    if '__WXMAC__' in wx.PlatformInfo:
        menuText += u'\tShift+Ctrl+N'
    else:
        menuText += u'\tShift+Ctrl+INS'
    return menuText  
            
class TaskList(patterns.CompositeSet):
    # FIXME: TaskList should be called TaskCollection or TaskSet

    newItemMenuText = newTaskMenuText()
    newItemHelpText = _('Insert a new task')
    editItemMenuText = _('&Edit task...')
    editItemHelpText = _('Edit the selected task')
    deleteItemMenuText = _('&Delete task\tCtrl+DEL')
    deleteItemHelpText = _('Delete the selected task(s)')
    newSubItemMenuText = newSubTaskMenuText()
    newSubItemHelpText = _('Insert a new subtask into the selected task')
    
    def extend(self, tasks):
        super(TaskList, self).extend(tasks)
        for task in self._compositesAndAllChildren(tasks):
            for category in task.categories():
                category.addCategorizable(task)
                
    def removeItems(self, tasks):
        super(TaskList, self).removeItems(tasks)
        for task in self._compositesAndAllChildren(tasks):
            for category in task.categories():
                category.removeCategorizable(task)
    
    def _nrInterestingTasks(self, isInteresting):
        interestingTasks = [task for task in self if isInteresting(task)]
        return len(interestingTasks)

    def nrCompleted(self):
        return self._nrInterestingTasks(task.Task.completed)

    def nrOverdue(self):
        return self._nrInterestingTasks(task.Task.overdue)

    def nrInactive(self):
        return self._nrInterestingTasks(task.Task.inactive)

    def nrDueToday(self):
        return self._nrInterestingTasks(task.Task.dueToday)
    
    def nrBeingTracked(self):
        return self._nrInterestingTasks(task.Task.isBeingTracked)

    def allCompleted(self):
        nrCompleted = self.nrCompleted()
        return nrCompleted > 0 and nrCompleted == len(self)
            
    def efforts(self):
        result = []
        for task in self:
            result.extend(task.efforts())
        return result
        
    def originalLength(self):
        ''' Provide a way for bypassing the __len__ method of decorators. '''
        return len(self)
    
    def minDate(self):      
        return min(self.__allDates())
          
    def maxDate(self):
        return max(self.__allDates())

    def __allDates(self):        
        realDates = [aDate for task in self 
            for aDate in (task.startDate(), task.dueDate(), task.completionDate()) 
            if aDate != date.Date()]
        return realDates or [date.Date()]            

    def minPriority(self):
        return min(self.__allPriorities())
        
    def maxPriority(self):
        return max(self.__allPriorities())
        
    def __allPriorities(self):
        return [task.priority() for task in self] or (0,)

        
class SingleTaskList(TaskList):
    pass

