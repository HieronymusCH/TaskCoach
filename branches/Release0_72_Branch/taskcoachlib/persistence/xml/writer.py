'''
Task Coach - Your friendly task manager
Copyright (C) 2004-2009 Frank Niessink <frank@niessink.com>
Copyright (C) 2007-2008 Jerome Laheurte <fraca7@free.fr>

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

import xml.dom, os
from taskcoachlib import meta
from taskcoachlib.domain import date, attachment, task, note, category


class XMLWriter(object):
    def __init__(self, fd, versionnr=meta.data.tskversion):
        self.__fd = fd
        self.__versionnr = versionnr

    def write(self, taskList, categoryContainer,
              noteContainer, syncMLConfig, guid):
        domImplementation = xml.dom.getDOMImplementation()
        self.document = domImplementation.createDocument(None, 'tasks', None)
        pi = self.document.createProcessingInstruction('taskcoach', 
            'release="%s" tskversion="%d"'%(meta.data.version, 
            self.__versionnr))
        self.document.insertBefore(pi, self.document.documentElement)
        for task in taskList.rootItems():
            self.document.documentElement.appendChild(self.taskNode(task))
        for category in categoryContainer.rootItems():
            self.document.documentElement.appendChild(self.categoryNode(category, taskList, noteContainer))
        for note in noteContainer.rootItems():
            self.document.documentElement.appendChild(self.noteNode(note))
        if syncMLConfig:
            self.document.documentElement.appendChild(self.syncMLNode(syncMLConfig))
        if guid:
            self.document.documentElement.appendChild(self.textNode('guid', guid))
        self.document.writexml(self.__fd, newl='\n')

    def taskNode(self, task):
        node = self.baseCompositeNode(task, 'task', self.taskNode)
        node.setAttribute('status', str(task.getStatus()))
        if task.startDate() != date.Date():
            node.setAttribute('startdate', str(task.startDate()))
        if task.dueDate() != date.Date():
            node.setAttribute('duedate', str(task.dueDate()))
        if task.completionDate() != date.Date():
            node.setAttribute('completiondate', str(task.completionDate()))
        if task.recurrence():
            node.appendChild(self.recurrenceNode(task.recurrence()))
        if task.budget() != date.TimeDelta():
            node.setAttribute('budget', self.budgetAsAttribute(task.budget()))
        if task.priority() != 0:
            node.setAttribute('priority', str(task.priority()))
        if task.hourlyFee() != 0:
            node.setAttribute('hourlyFee', str(task.hourlyFee()))
        if task.fixedFee() != 0:
            node.setAttribute('fixedFee', str(task.fixedFee()))
        if task.reminder() != None:
            node.setAttribute('reminder', str(task.reminder()))
        if task.shouldMarkCompletedWhenAllChildrenCompleted != None:
            node.setAttribute('shouldMarkCompletedWhenAllChildrenCompleted', 
                              str(task.shouldMarkCompletedWhenAllChildrenCompleted))
        for effort in task.efforts():
            node.appendChild(self.effortNode(effort))
        for note in task.notes():
            node.appendChild(self.noteNode(note))
        for attachment in task.attachments():
            node.appendChild(self.attachmentNode(attachment))
        return node

    def recurrenceNode(self, recurrence):
        node = self.document.createElement('recurrence')
        node.setAttribute('unit', recurrence.unit)
        if recurrence.amount > 1:
            node.setAttribute('amount', str(recurrence.amount))
        if recurrence.count > 0:
            node.setAttribute('count', str(recurrence.count))
        if recurrence.max > 0:
            node.setAttribute('max', str(recurrence.max))
        if recurrence.sameWeekday:
            node.setAttribute('sameWeekday', 'True')
        return node

    def effortNode(self, effort):
        node = self.document.createElement('effort')
        formattedStart = self.formatDateTime(effort.getStart())
        node.setAttribute('status', str(effort.getStatus()))
        node.setAttribute('start', formattedStart)
        stop = effort.getStop()
        if stop != None:
            formattedStop = self.formatDateTime(stop)
            if formattedStop == formattedStart:
                # Make sure the effort duration is at least one second
                formattedStop = self.formatDateTime(stop + date.TimeDelta(seconds=1))
            node.setAttribute('stop', formattedStop)
        if effort.description():
            node.appendChild(self.textNode('description', effort.description()))
        return node
    
    def categoryNode(self, category, *categorizableContainers):
        def inCategorizableContainer(categorizable):
            for container in categorizableContainers:
                if categorizable in container:
                    return True
            return False
        node = self.baseCompositeNode(category, 'category', self.categoryNode, 
                                      categorizableContainers)
        if category.isFiltered():
            node.setAttribute('filtered', str(category.isFiltered()))
        for note in category.notes():
            node.appendChild(self.noteNode(note))
        for attachment in category.attachments():
            node.appendChild(self.attachmentNode(attachment))
        # Make sure the categorizables referenced are actually in the 
        # categorizableContainer, i.e. they are not deleted
        categorizableIds = ' '.join([categorizable.id() for categorizable in \
            category.categorizables() if inCategorizableContainer(categorizable)])
        if categorizableIds:            
            node.setAttribute('categorizables', categorizableIds)
        return node
    
    def noteNode(self, note):
        node = self.baseCompositeNode(note, 'note', self.noteNode)
        for attachment in note.attachments():
            node.appendChild(self.attachmentNode(attachment))
        return node

    def __baseNode(self, item, nodeName):
        node = self.document.createElement(nodeName)
        node.setAttribute('id', item.id())
        node.setAttribute('status', str(item.getStatus()))
        if item.subject():
            node.setAttribute('subject', item.subject())
        if item.description():
            node.appendChild(self.textNode('description', item.description()))
        return node

    def baseNode(self, item, nodeName):
        ''' Create a node and add the attributes that all composite domain
            objects share, such as id, subject, description. '''
        node = self.__baseNode(item, nodeName)
        if item.color():
            node.setAttribute('color', str(item.color()))
        return node

    def baseCompositeNode(self, item, nodeName, childNodeFactory, childNodeFactoryArgs=()):
        """Same as baseNode, but also create child nodes by means of
        the childNodeFactory."""
        node = self.__baseNode(item, nodeName)
        if item.color(recursive=False):
            node.setAttribute('color', str(item.color(recursive=False)))
        if item.expandedContexts():
            node.setAttribute('expandedContexts', 
                              str(tuple(sorted(item.expandedContexts()))))
        for child in item.children():
            node.appendChild(childNodeFactory(child, *childNodeFactoryArgs))
        return node

    def attachmentNode(self, attachment):
        node = self.baseNode(attachment, 'attachment')
        node.setAttribute('type', attachment.type_)
        data = attachment.data()
        if data is None:
            node.setAttribute('location', attachment.location())
        else:
            dataNode = self.textNode('data', data.encode('base64'))
            dataNode.setAttribute('extension',
                                  os.path.splitext(attachment.location())[-1])
            node.appendChild(dataNode)
        for note in attachment.notes():
            node.appendChild(self.noteNode(note))
        return node

    def syncMLNode(self, syncMLConfig):
        node = self.document.createElement('syncml')
        self.__syncMLNode(syncMLConfig, node)
        return node

    def __syncMLNode(self, cfg, node):
        for name, value in cfg.properties():
            child = self.textNode('property', value)
            child.setAttribute('name', name)
            node.appendChild(child)

        for childCfg in cfg.children():
            child = self.document.createElement(childCfg.name)
            self.__syncMLNode(childCfg, child)
            node.appendChild(child)

    def budgetAsAttribute(self, budget):
        return '%d:%02d:%02d'%budget.hoursMinutesSeconds()
                
    def textNode(self, nodeName, text):
        node = self.document.createElement(nodeName)
        textNode = self.document.createTextNode(text)
        node.appendChild(textNode)
        return node

    def formatDateTime(self, dateTime):
        return dateTime.strftime('%Y-%m-%d %H:%M:%S')


class TemplateXMLWriter(XMLWriter):
    def write(self, tsk):
        super(TemplateXMLWriter, self).write(task.TaskList([tsk]),
                   category.CategoryList(),
                   note.NoteContainer(),
                   None, None)

    def taskNode(self, task):
        node = super(TemplateXMLWriter, self).taskNode(task)

        today = date.Today()
        todayTime = date.DateTime(today.year, today.month, today.day)

        for name in ['startDate', 'dueDate', 'completionDate']:
            dt = getattr(task, name)()
            if dt != date.Date():
                node.removeAttribute(name.lower())
                delta = dt - today
                node.setAttribute(name.lower() + 'tmpl',
                                  'Today() + %s' % repr(delta))
        for name in ['reminder']:
            dt = getattr(task, name)()
            if dt is not None:
                node.removeAttribute(name.lower())
                delta = dt - todayTime
                node.setAttribute(name.lower() + 'tmpl',
                                  'DateTime(Today().year, Today().month, Today().day) + %s' % repr(delta))

        return node
