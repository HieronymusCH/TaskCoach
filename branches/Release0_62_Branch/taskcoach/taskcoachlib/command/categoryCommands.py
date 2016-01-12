import base
from i18n import _
from domain import category

class NewCategoryCommand(base.BaseCommand):
    def name(self):
        return _('New category')

    def __init__(self, *args, **kwargs):
        super(NewCategoryCommand, self).__init__(*args, **kwargs)
        self.items = self.createNewCategories()
        
    def createNewCategories(self):
        return [category.Category(subject=_('New category'))]
        
    def do_command(self):
        self.list.extend(self.items)

    def undo_command(self):
        self.list.removeItems(self.items)

    def redo_command(self):
        self.list.extend(self.items)


class NewSubCategoryCommand(NewCategoryCommand):
    def name(self):
        return _('New subcategory')
            
    def createNewCategories(self):
        return [parent.newChild(subject=_('New subcategory')) for parent in self.items]


class EditCategoryCommand(base.EditCommand):
    def name(self):
        return _('Edit category')
    
    def getItemsToSave(self):
        return self.items
    
    
class DragAndDropCategoryCommand(base.DragAndDropCommand):
    def name(self):
        return _('Drag and drop category')
