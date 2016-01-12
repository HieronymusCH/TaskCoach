import time, xml.dom.minidom, re
import domain.date as date
import domain.effort as effort
import domain.task as task
import domain.category as category

class XMLReader:
    def __init__(self, fd):
        self.__fd = fd

    def read(self):
        domDocument = xml.dom.minidom.parse(self.__fd)
        self.__tskversion = self.__parseTskVersionNumber(domDocument)
        tasks = self.__parseTaskNodes(domDocument.documentElement.childNodes)
        tasksAndAllChildren = tasks[:]
        for task in tasks:
            tasksAndAllChildren.extend(task.children(recursive=True))
        tasksById = dict([(task.id(), task) for task in tasksAndAllChildren])
        if self.__tskversion <= 13:
            categories = self.__parseCategoryNodesFromTaskNodes(domDocument, 
                                                                tasksById)
        else:
            categories = self.__parseCategoryNodes( \
                domDocument.documentElement.childNodes, tasksById)
        return tasks, categories

    def __parseTskVersionNumber(self, domDocument):
        processingInstruction = domDocument.firstChild.data
        matchObject = re.search('tskversion="(\d+)"', processingInstruction)
        return int(matchObject.group(1))
        
    def __parseTaskNodes(self, nodes):
        return [self.__parseTaskNode(node) for node in nodes \
                if node.nodeName == 'task']
                
    def __parseCategoryNodes(self, nodes, tasks):
        return [self.__parseCategoryNode(node, tasks) for node in nodes \
                if node.nodeName == 'category']

    def __parseCategoryNode(self, categoryNode, tasksById):        
        subject = categoryNode.getAttribute('subject')
        filtered = self.__parseBoolean(categoryNode.getAttribute('filtered'), 
                                       False)
        taskIds = categoryNode.getAttribute('tasks')
        if taskIds:
            # The category tasks attribute might contain id's that refer to tasks that
            # have been deleted (a bug in release 0.61.5), be prepared:
            categoryTasks = [tasksById[id] for id in taskIds.split(' ') if id in tasksById]
        else:
            categoryTasks = []
        children = self.__parseCategoryNodes(categoryNode.childNodes, tasksById)
        return category.Category(subject, categoryTasks, children, filtered)
                      
    def __parseCategoryNodesFromTaskNodes(self, document, tasks):
        taskNodes = document.getElementsByTagName('task')
        categoryMapping = self.__parseCategoryNodesWithinTaskNodes(taskNodes, tasks)
        subjectCategoryMapping = {}
        for taskId, categories in categoryMapping.items():
            for subject in categories:
                if subject in subjectCategoryMapping:
                    cat = subjectCategoryMapping[subject]
                else:
                    cat = category.Category(subject)
                    subjectCategoryMapping[subject] = cat
                cat.addTask(tasks[taskId])
        return subjectCategoryMapping.values()
    
    def __parseCategoryNodesWithinTaskNodes(self, taskNodes, tasks):
        categoryMapping = {}
        for node in taskNodes:
            taskId = node.getAttribute('id')
            categories = [self.__parseTextNode(node) for node in node.childNodes \
                          if node.nodeName == 'category']
            categoryMapping.setdefault(taskId, []).extend(categories)
        return categoryMapping
        
    def __parseTaskNode(self, taskNode):
        subject = taskNode.getAttribute('subject')
        id = taskNode.getAttribute('id')
        description = self.__parseDescription(taskNode)
        startDate = date.parseDate(taskNode.getAttribute('startdate'))
        dueDate = date.parseDate(taskNode.getAttribute('duedate'))
        completionDate = date.parseDate(taskNode.getAttribute('completiondate'))
        budget = date.parseTimeDelta(taskNode.getAttribute('budget'))
        priority = self.__parseInteger(taskNode.getAttribute('priority'))
        lastModificationTime = \
            self.__parseDateTime(taskNode.getAttribute('lastModificationTime'))
        hourlyFee = self.__parseFloat(taskNode.getAttribute('hourlyFee'))
        fixedFee = self.__parseFloat(taskNode.getAttribute('fixedFee'))
        reminder = self.__parseDateTime(taskNode.getAttribute('reminder'))
        attachments = self.__parseAttachmentNodes(taskNode.childNodes)
        shouldMarkCompletedWhenAllChildrenCompleted = \
            self.__parseBoolean(taskNode.getAttribute('shouldMarkCompletedWhenAllChildrenCompleted'))
        if self.__tskversion <= 13:
            categories = self.__parseCategoryNodesWithinTaskNode(taskNode.childNodes)
        else:
            categories = []
        children = self.__parseTaskNodes(taskNode.childNodes)
        efforts = self.__parseEffortNodes(taskNode.childNodes)
        parent = task.Task(subject, description, id_=id, startDate=startDate, 
            dueDate=dueDate, completionDate=completionDate, budget=budget, 
            priority=priority, lastModificationTime=lastModificationTime, 
            hourlyFee=hourlyFee, fixedFee=fixedFee, reminder=reminder, 
            categories=categories, attachments=attachments, children=children,
            efforts=efforts,
            shouldMarkCompletedWhenAllChildrenCompleted=\
                shouldMarkCompletedWhenAllChildrenCompleted)
        return parent        
        
    def __parseCategoryNodesWithinTaskNode(self, nodes):
        return [self.__parseTextNode(node) for node in nodes \
                if node.nodeName == 'category']
        
    def __parseAttachmentNodes(self, nodes):
        return [self.__parseTextNode(node) for node in nodes \
                if node.nodeName == 'attachment']

    def __parseEffortNodes(self, nodes):
        return [self.__parseEffortNode(node) for node in nodes \
                if node.nodeName == 'effort']
        
    def __parseEffortNode(self, effortNode):
        start = effortNode.getAttribute('start')
        stop = effortNode.getAttribute('stop')
        description = self.__parseDescription(effortNode)
        return effort.Effort(None, date.parseDateTime(start), 
            date.parseDateTime(stop), description)
        
    def __getNode(self, parent, tagName):
        for child in parent.childNodes:
            if child.nodeName == tagName:
                return child
        return None        
        
    def __parseDescription(self, node):
        if self.__tskversion <= 6:
            description = node.getAttribute('description')
        else:
            descriptionNode = self.__getNode(node, 'description')
            if descriptionNode and descriptionNode.firstChild:
                description = descriptionNode.firstChild.data
            else:
                description = ''
        return description
    
    def __parseTextNode(self, node):
        return node.firstChild.data
    
    def __parseInteger(self, integerText):
        return self.__parse(integerText, int, 0)

    def __parseFloat(self, floatText):
        return self.__parse(floatText, float, 0.0)
                    
    def __parseDateTime(self, dateTimeText):
        return self.__parse(dateTimeText, date.parseDateTime, None)
    
    def __parseBoolean(self, booleanText, defaultValue=None):
        def textToBoolean(text):
            if text in ['True', 'False']:
                return text == 'True'
            else:
                raise ValueError, "Expected 'True' or 'False'"
        return self.__parse(booleanText, textToBoolean, defaultValue)
        
    def __parse(self, text, parseFunction, defaultValue):
        try:
            return parseFunction(text)
        except ValueError:
            return defaultValue
