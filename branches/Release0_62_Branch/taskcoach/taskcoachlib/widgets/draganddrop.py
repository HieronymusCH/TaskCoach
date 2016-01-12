import wx, urlparse


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, onDropCallback=None, onDragOverCallback=None):
        wx.FileDropTarget.__init__(self)
        self.__onDropCallback = onDropCallback
        self.__onDragOverCallback = onDragOverCallback or self.__defaultDragOverCallback
        
    def OnDropFiles(self, x, y, filenames):
        if self.__onDropCallback:
            self.__onDropCallback(x, y, filenames)
            return True
        else:
            return False

    def OnDragOver(self, x, y, defaultResult):
        return self.__onDragOverCallback(x, y, defaultResult)
    
    def __defaultDragOverCallback(self, x, y, defaultResult):
        return defaultResult
    
    
class TextDropTarget(wx.TextDropTarget):
    def __init__(self, onDropCallback):
        wx.TextDropTarget.__init__(self)
        self.__onDropCallback = onDropCallback
        
    def OnDropText(self, x, y, text):
        self.__onDropCallback(text)
        

class DropTarget(wx.DropTarget):
    def __init__(self, onDropURLCallback, onDropFileCallback,
            onDropThunderbirdMailCallback):
        super(DropTarget, self).__init__()
        self.__onDropURLCallback = onDropURLCallback
        self.__onDropFileCallback = onDropFileCallback
        self.__onDropThunderbirdMailCallback = onDropThunderbirdMailCallback
        self.__compositeDataObject = wx.DataObjectComposite()
        self.__urlDataObject = wx.TextDataObject()
        self.__fileDataObject = wx.FileDataObject()
        self.__thunderbirdMailDataObject = wx.CustomDataObject('text/x-moz-message')
        for dataObject in self.__fileDataObject, self.__urlDataObject, \
                          self.__thunderbirdMailDataObject:
            # NB: First data object added is the preferred data object
            self.__compositeDataObject.Add(dataObject)
        self.SetDataObject(self.__compositeDataObject)
        
    def OnDrop(self, x, y):
        return True
    
    def OnData(self, x, y, result):
        self.GetData()
        if self.__urlDataObject.GetTextLength() > 1:
            url = self.__urlDataObject.GetText()
            scheme, server = urlparse.urlparse(url)[:2]
            if scheme and (scheme == 'file' or server):
                self.__onDropURLCallback(url)
            else:
                result = wx.DragNone
        elif self.__thunderbirdMailDataObject.GetData():
            data = self.__thunderbirdMailDataObject.GetData().decode('unicode_internal')
            self.__onDropThunderbirdMailCallback(data)
        else:
            self.__onDropFileCallback(self.__fileDataObject.GetFilenames())
        return result
