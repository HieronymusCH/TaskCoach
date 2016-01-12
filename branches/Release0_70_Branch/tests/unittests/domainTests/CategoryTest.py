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

import test, wx
from taskcoachlib import patterns
from taskcoachlib.domain import category


class CategorizableCompositeObjectTest(test.TestCase):
    def setUp(self):
        self.categorizable = category.CategorizableCompositeObject('categorizable')
        self.category = category.Category('category')
        
    categoryAddedEventType = category.CategorizableCompositeObject.categoryAddedEventType()
    categoryRemovedEventType = category.CategorizableCompositeObject.categoryRemovedEventType()
    totalCategoryAddedEventType = category.CategorizableCompositeObject.totalCategoryAddedEventType()
    totalCategoryRemovedEventType = category.CategorizableCompositeObject.totalCategoryRemovedEventType()
    categorySubjectChangedEventType = category.CategorizableCompositeObject.categorySubjectChangedEventType()
    totalCategorySubjectChangedEventType = category.CategorizableCompositeObject.totalCategorySubjectChangedEventType()
    categoryColorChangedEventType = category.CategorizableCompositeObject.categoryColorChangedEventType()
        
    def testCategorizableDoesNotBelongToAnyCategoryByDefault(self):
        for recursive in False, True:
            self.failIf(self.categorizable.categories(recursive=recursive))
    
    def testCategorizableHasNoCategoryColorByDefault(self):
        self.assertEqual(None, self.categorizable.categoryColor())
    
    def testAddCategory(self):
        self.categorizable.addCategory(self.category)
        self.assertEqual(set([self.category]), self.categorizable.categories())

    def testAddCategoryNotification(self):
        self.registerObserver(self.categoryAddedEventType)
        self.categorizable.addCategory(self.category)
        self.assertEqual([patterns.Event(self.categorizable, 
            self.categoryAddedEventType, self.category)], self.events)    
        
    def testAddSecondCategory(self):
        self.categorizable.addCategory(self.category)
        cat2 = category.Category('category 2')
        self.categorizable.addCategory(cat2)
        self.assertEqual(set([self.category, cat2]), 
            self.categorizable.categories())
        
    def testAddSameCategoryTwice(self):
        self.categorizable.addCategory(self.category)
        self.categorizable.addCategory(self.category)
        self.assertEqual(set([self.category]), self.categorizable.categories())
        
    def testAddSameCategoryTwiceCausesNoNotification(self):
        self.categorizable.addCategory(self.category)
        self.registerObserver(self.categoryAddedEventType)
        self.categorizable.addCategory(self.category)
        self.failIf(self.events)
    
    def testAddCategoryViaConstructor(self):
        categorizable = category.CategorizableCompositeObject(categories=[self.category])
        self.assertEqual(set([self.category]), categorizable.categories())
        
    def testAddCategoriesViaConstructor(self):
        anotherCategory = category.Category('Another category')
        categories = [self.category, anotherCategory]
        categorizable = category.CategorizableCompositeObject(categories= \
            categories)
        self.assertEqual(set(categories), categorizable.categories())
        
    def testAddCategoryDoesNotAddCategorizableToCategory(self):
        self.categorizable.addCategory(self.category)
        self.assertEqual([], self.category.categorizables())
        
    def testAddParentToCategory(self):
        self.registerObserver(self.totalCategoryAddedEventType)
        child = category.CategorizableCompositeObject('child')
        self.categorizable.addChild(child)
        child.setParent(self.categorizable)
        cat = category.Category('Parent category')
        self.categorizable.addCategory(cat)
        self.assertEqual([patterns.Event(child, self.totalCategoryAddedEventType, 
            cat)], self.events)
        
    def testRemoveCategory(self):
        self.categorizable.addCategory(self.category)
        self.categorizable.removeCategory(self.category)
        self.assertEqual(set(), self.categorizable.categories())
        
    def testRemoveCategoryNotification(self):
        self.categorizable.addCategory(self.category)
        self.registerObserver(self.categoryRemovedEventType)
        self.categorizable.removeCategory(self.category)
        self.assertEqual(self.category, self.events[0].value())

    def testRemoveCategoryTwice(self):
        self.categorizable.addCategory(self.category)
        self.categorizable.removeCategory(self.category)
        self.categorizable.removeCategory(self.category)
        self.assertEqual(set(), self.categorizable.categories())

    def testRemoveCategoryTwiceNotification(self):
        self.categorizable.addCategory(self.category)
        self.registerObserver(self.categoryRemovedEventType)
        self.categorizable.removeCategory(self.category)
        self.categorizable.removeCategory(self.category)
        self.assertEqual(1, len(self.events))
        
    def testCategorySubjectChanged(self):
        self.registerObserver(self.categorySubjectChangedEventType)
        self.registerObserver(self.totalCategorySubjectChangedEventType)
        self.categorizable.addCategory(self.category)
        self.category.addCategorizable(self.categorizable)
        self.category.setSubject('New subject')
        # Expect categorySubjectChangedEventType and 
        # totalCategorySubjectChangedEventType:
        self.assertEqual(2, len(self.events)) 

    def testCategorySubjectChanged_NotifySubItemsToo(self):
        self.registerObserver(self.categorySubjectChangedEventType)
        self.registerObserver(self.totalCategorySubjectChangedEventType)
        self.categorizable.addChild(category.CategorizableCompositeObject())
        self.categorizable.addCategory(self.category)
        self.category.addCategorizable(self.categorizable)
        self.category.setSubject('New subject')
        # Expect categorySubjectChangedEventType and 2x 
        # totalCategorySubjectChangedEventType: 
        self.assertEqual(3, len(self.events))        

    def testColor(self):
        self.categorizable.addCategory(self.category)
        self.category.setColor(wx.RED)
        self.assertEqual(wx.RED, self.categorizable.categoryColor())

    def testColorWithTupleColor(self):
        self.categorizable.addCategory(self.category)
        self.category.setColor((255, 0, 0, 255))
        self.assertEqual(wx.RED, self.categorizable.categoryColor())
    
    def testSubItemUsesParentColor(self):
        self.categorizable.addCategory(self.category)
        child = category.CategorizableCompositeObject()
        self.categorizable.addChild(child)
        child.setParent(self.categorizable)
        self.category.setColor(wx.RED)
        self.assertEqual(wx.RED, child.categoryColor())
    
    def testColorChanged(self):
        self.categorizable.addCategory(self.category)
        self.category.addCategorizable(self.categorizable)
        self.registerObserver(self.categoryColorChangedEventType)
        self.category.setColor(wx.RED)
        self.assertEqual(1, len(self.events))

    def testColorChanged_NotifySubItemsToo(self):
        self.registerObserver(self.categoryColorChangedEventType)
        self.categorizable.addChild(category.CategorizableCompositeObject())
        self.categorizable.addCategory(self.category)
        self.category.addCategorizable(self.categorizable)
        self.category.setColor(wx.RED)
        self.assertEqual(2, len(self.events))
        
    def testParentColorChanged(self):
        self.registerObserver(self.categoryColorChangedEventType)
        subCategory = category.Category('Subcategory')
        self.category.addChild(subCategory)
        subCategory.setParent(self.category)
        self.categorizable.addCategory(subCategory)
        subCategory.addCategorizable(self.categorizable)
        self.category.setColor(wx.RED)
        self.assertEqual(1, len(self.events))
        
    def testAddCategoryWithColor(self):
        self.registerObserver(self.categoryColorChangedEventType)
        newCategory = category.Category('New category')
        newCategory.setColor(wx.RED)
        self.categorizable.addCategory(newCategory)
        self.assertEqual(1, len(self.events))
        
    def testAddCategoryWithParentWithColor(self):
        self.registerObserver(self.categoryColorChangedEventType)
        parentCategory = category.Category('Parent')
        parentCategory.setColor(wx.RED)
        childCategory = category.Category('Child')
        parentCategory.addChild(childCategory)
        childCategory.setParent(parentCategory)
        self.categorizable.addCategory(childCategory)
        self.assertEqual(1, len(self.events))
        
    def testRemoveCategoryWithColor(self):
        self.categorizable.addCategory(self.category)
        self.category.setColor(wx.RED)
        self.registerObserver(self.categoryColorChangedEventType)
        self.categorizable.removeCategory(self.category)
        self.assertEqual(1, len(self.events))
        
    def testColorWhenOneOutOfTwoCategoriesHasColor(self):
        self.categorizable.addCategory(self.category)
        self.categorizable.addCategory(category.Category('Another category'))
        self.category.setColor(wx.RED)
        self.assertEqual(wx.RED, self.categorizable.categoryColor())
        
    def testColorWhenBothCategoriesHaveSameColor(self):
        self.categorizable.addCategory(self.category)
        anotherCategory = category.Category('Another category')
        self.categorizable.addCategory(anotherCategory)
        for cat in [self.category, anotherCategory]:
            cat.setColor(wx.RED)
        self.assertEqual(wx.RED, self.categorizable.categoryColor())
                
    def testColorWhenBothCategoriesHaveDifferentColors(self):
        self.categorizable.addCategory(self.category)
        anotherCategory = category.Category('Another category')
        self.categorizable.addCategory(anotherCategory)
        self.category.setColor(wx.RED)
        anotherCategory.setColor(wx.BLUE)
        expectedColor = wx.Color(127, 0, 127, 255)
        self.assertEqual(expectedColor, self.categorizable.categoryColor())
                
    def testParentCategoryIncludedInChildRecursiveCategories(self):
        self.categorizable.addCategory(self.category)
        child = category.CategorizableCompositeObject()
        self.categorizable.addChild(child)
        self.assertEqual(set([self.category]), child.categories(recursive=True))

    def testParentCategoryNotIncludedInChildCategories(self):
        self.categorizable.addCategory(self.category)
        child = category.CategorizableCompositeObject()
        self.categorizable.addChild(child)
        self.assertEqual(set(), child.categories(recursive=False))
        
    def testGrandParentCategoryIncludedInGrandChildRecursiveCategories(self):
        self.categorizable.addCategory(self.category)
        child = category.CategorizableCompositeObject()
        self.categorizable.addChild(child)
        grandchild = category.CategorizableCompositeObject()
        child.addChild(grandchild)
        self.assertEqual(set([self.category]), 
                         grandchild.categories(recursive=True))
        
    def testGrandParentAndParentCategoriesIncludedInGrandChildRecursiveCategories(self):
        self.categorizable.addCategory(self.category)
        child = category.CategorizableCompositeObject()
        self.categorizable.addChild(child)
        grandchild = category.CategorizableCompositeObject()
        child.addChild(grandchild)
        childCategory = category.Category('Child category')
        child.addCategory(childCategory)
        self.assertEqual(set([self.category, childCategory]), 
            grandchild.categories(recursive=True))
        
    def testRemoveCategoryCausesChildNotification(self):
        self.categorizable.addCategory(self.category)
        child = category.CategorizableCompositeObject()
        self.categorizable.addChild(child)
        self.registerObserver(self.totalCategoryRemovedEventType)
        self.categorizable.removeCategory(self.category)
        self.assertEqual([patterns.Event(child, 
            self.totalCategoryRemovedEventType, self.category)], self.events)


class CategoryTest(test.TestCase):
    def setUp(self):
        self.category = category.Category('category')
        self.subCategory = category.Category('subcategory')
        self.categorizable = category.CategorizableCompositeObject('parent')
        self.child = category.CategorizableCompositeObject('child')
        
    def testGetState_Subject(self):
        self.assertEqual('category', self.category.__getstate__()['subject'])
        
    def testGetState_Description(self):
        self.assertEqual('', self.category.__getstate__()['description'])
        
    def testGetState_Color(self):
        self.assertEqual(None, self.category.__getstate__()['color'])
        
    def testCreateWithSubject(self):
        self.assertEqual('category', self.category.subject())
    
    def testSetSubject(self):
        self.category.setSubject('New')
        self.assertEqual('New', self.category.subject())
        
    def testSetSubjectNotification(self):
        eventType = category.Category.subjectChangedEventType()
        self.registerObserver(eventType)
        self.category.setSubject('New')
        self.assertEqual([patterns.Event(self.category, eventType, 'New')], 
            self.events)
        
    def testSetSubjectCausesNoNotificationWhenNewSubjectEqualsOldSubject(self):
        eventType = category.Category.subjectChangedEventType()
        self.registerObserver(eventType)
        self.category.setSubject(self.category.subject())
        self.failIf(self.events)
        
    def testCreateWithDescription(self):
        aCategory = category.Category('subject', description='Description')
        self.assertEqual('Description', aCategory.description())

    def testNoCategorizablesAfterCreation(self):
        self.assertEqual([], self.category.categorizables())
      
    def testAddCategorizable(self):
        self.category.addCategorizable(self.categorizable)
        self.assertEqual([self.categorizable], self.category.categorizables())
        
    def testAddCategorizableDoesNotAddCategoryToCategorizable(self):
        self.category.addCategorizable(self.categorizable)
        self.assertEqual(set([]), self.categorizable.categories())
        
    def testAddCategorizableTwice(self):
        self.category.addCategorizable(self.categorizable)
        self.category.addCategorizable(self.categorizable)
        self.assertEqual([self.categorizable], self.category.categorizables())
        
    def testRemoveCategorizable(self):
        self.category.addCategorizable(self.categorizable)
        self.category.removeCategorizable(self.categorizable)
        self.failIf(self.category.categorizables())
        self.failIf(self.categorizable.categories())
        
    def testRemovecategorizableThatsNotInThisCategory(self):
        self.category.removeCategorizable(self.categorizable)
        self.failIf(self.category.categorizables())
        self.failIf(self.categorizable.categories())
    
    def testCreateWithCategorizable(self):
        cat = category.Category('category', [self.categorizable])
        self.assertEqual([self.categorizable], cat.categorizables())
        
    def testCreateWithCategorizableDoesNotSetCategorizableCategories(self):
        cat = category.Category('category', [self.categorizable])
        self.assertEqual(set([]), self.categorizable.categories())
    
    def testAddCategorizableToSubCategory(self):
        self.category.addChild(self.subCategory)
        self.subCategory.addCategorizable(self.categorizable)
        self.assertEqual([self.categorizable], 
                         self.category.categorizables(recursive=True))
     
    def testAddSubCategory(self):
        self.category.addChild(self.subCategory)
        self.assertEqual([self.subCategory], self.category.children())
    
    def testCreateWithSubCategories(self):
        cat = category.Category('category', children=[self.subCategory])
        self.assertEqual([self.subCategory], cat.children())
     
    def testParentOfSubCategory(self):
        self.category.addChild(self.subCategory)
        self.assertEqual(self.category, self.subCategory.parent())
        
    def testParentOfRootCategory(self):
        self.assertEqual(None, self.category.parent())
        
    def testEquality_SameSubjectAndNoParents(self):
        self.assertNotEqual(category.Category(self.category.subject()), 
                            self.category)
        self.assertNotEqual(self.category,
                            category.Category(self.category.subject()))
                     
    def testEquality_SameSubjectDifferentParents(self):
        self.category.addChild(self.subCategory)
        self.assertNotEqual(category.Category(self.subCategory.subject()), 
                            self.subCategory)
   
    def testNotFilteredByDefault(self):
        self.failIf(self.category.isFiltered())
        
    def testSetFilteredOn(self):
        self.category.setFiltered()
        self.failUnless(self.category.isFiltered())
        
    def testSetFilteredOff(self):
        self.category.setFiltered(False)
        self.failIf(self.category.isFiltered())
    
    def testSetFilteredViaConstructor(self):
        filteredCategory = category.Category('test', filtered=True)
        self.failUnless(filteredCategory.isFiltered())
        
    def testSetFilteredOnTurnsOffFilteringForChild(self):
        self.category.addChild(self.subCategory)
        self.subCategory.setFiltered()
        self.category.setFiltered()
        self.failIf(self.subCategory.isFiltered())

    def testSetFilteredOnTurnsOffFilteringForGrandChild(self):
        self.category.addChild(self.subCategory)
        grandChild = category.Category('grand child')
        self.subCategory.addChild(grandChild)
        grandChild.setFiltered()
        self.category.setFiltered()
        self.failIf(grandChild.isFiltered())
        
    def testSetFilteredOnForChildTurnsOffFilteringForParent(self):
        self.category.setFiltered()
        self.category.addChild(self.subCategory)
        self.subCategory.setFiltered()
        self.failIf(self.category.isFiltered())

    def testSetFilteredOnForGrandChildTurnsOffFilteringForGrandParent(self):
        self.category.setFiltered()
        self.category.addChild(self.subCategory)
        grandChild = category.Category('grand child')
        self.subCategory.addChild(grandChild)
        grandChild.setFiltered()
        self.failIf(self.category.isFiltered())
        
    def testContains_NoCategorizables(self):
        self.failIf(self.category.contains(self.categorizable))
        
    def testContains_CategorizablesInCategory(self):
        self.category.addCategorizable(self.categorizable)
        self.failUnless(self.category.contains(self.categorizable))
        
    def testContains_CategorizableInSubCategory(self):
        self.subCategory.addCategorizable(self.categorizable)
        self.category.addChild(self.subCategory)
        self.failUnless(self.category.contains(self.categorizable))
        
    def testContains_ParentInCategory(self):
        self.category.addCategorizable(self.categorizable)
        self.categorizable.addChild(self.child)
        self.failUnless(self.category.contains(self.child))
        
    def testContains_ParentInSubCategory(self):
        self.subCategory.addCategorizable(self.categorizable)
        self.category.addChild(self.subCategory)
        self.categorizable.addChild(self.child)
        self.failUnless(self.category.contains(self.child))
    
    def testContains_ChildInCategory(self):
        self.categorizable.addChild(self.child)
        self.category.addCategorizable(self.child)
        self.failIf(self.category.contains(self.categorizable))
        
    def testContains_ChildInSubCategory(self):
        self.categorizable.addChild(self.child)
        self.subCategory.addCategorizable(self.child)
        self.category.addChild(self.subCategory)
        self.failIf(self.category.contains(self.categorizable))
        
    def testRecursiveContains_ChildInCategory(self):
        self.categorizable.addChild(self.child)
        self.category.addCategorizable(self.child)
        self.failUnless(self.category.contains(self.categorizable, treeMode=True))
        
    def testRecursiveContains_ChildInSubcategory(self):
        self.categorizable.addChild(self.child)
        self.subCategory.addCategorizable(self.child)
        self.category.addChild(self.subCategory)
        self.failUnless(self.category.contains(self.categorizable, treeMode=True))
        
    def testCopy_SubjectIsCopied(self):
        self.category.setSubject('New subject')
        copy = self.category.copy()
        self.assertEqual(copy.subject(), self.category.subject())
        
    def testCopy_SubjectIsDifferentFromOriginalSubject(self):
        self.subCategory.setSubject('New subject')
        self.category.addChild(self.subCategory)
        copy = self.category.copy()
        self.subCategory.setSubject('Other subject')
        self.assertEqual('New subject', copy.children()[0].subject())
        
    def testCopy_FilteredStatusIsCopied(self):
        self.category.setFiltered()
        copy = self.category.copy()
        self.assertEqual(copy.isFiltered(), self.category.isFiltered())
        
    def testCopy_CategorizablesAreCopied(self):
        self.category.addCategorizable(self.categorizable)
        copy = self.category.copy()
        self.assertEqual(copy.categorizables(), self.category.categorizables())
        
    def testCopy_CategorizablesAreCopiedIntoADifferentList(self):
        copy = self.category.copy()
        self.category.addCategorizable(self.categorizable)
        self.failIf(self.categorizable in copy.categorizables())

    def testCopy_ChildrenAreCopied(self):
        self.category.addChild(self.subCategory)
        copy = self.category.copy()
        self.assertEqual(self.subCategory.subject(), copy.children()[0].subject())

    def testAddTaskNotification(self):
        eventType = category.Category.categorizableAddedEventType()
        self.registerObserver(eventType)
        self.category.addCategorizable(self.categorizable)
        self.assertEqual(1, len(self.events))
        
    def testRemoveTaskNotification(self):
        eventType = category.Category.categorizableRemovedEventType()
        self.registerObserver(eventType)
        self.category.addCategorizable(self.categorizable)
        self.category.removeCategorizable(self.categorizable)
        self.assertEqual(1, len(self.events))
        
    def testGetDefaultColor(self):
        self.assertEqual(None, self.category.color())
        
    def testSetColor(self):
        self.category.setColor(wx.RED)
        self.assertEqual(wx.RED, self.category.color())
        
    def testCopy_ColorIsCopied(self):
        self.category.setColor(wx.RED)
        copy = self.category.copy()
        self.assertEqual(wx.RED, copy.color())
        
    def testColorChangeNotification(self):
        eventType = category.Category.colorChangedEventType()
        self.registerObserver(eventType)
        self.category.setColor(wx.RED)
        self.assertEqual(1, len(self.events))
        
    def testSubCategoryWithoutColorHasParentColor(self):
        self.category.addChild(self.subCategory)
        self.category.setColor(wx.RED)
        self.assertEqual(wx.RED, self.subCategory.color())
        
    def testSubCategoryWithoutColorHasNoOwnColor(self):
        self.category.addChild(self.subCategory)
        self.category.setColor(wx.RED)
        self.assertEqual(None, self.subCategory.color(recursive=False))
                
    def testParentColorChangeNotification(self):
        eventType = category.Category.colorChangedEventType()
        self.registerObserver(eventType)
        self.category.addChild(self.subCategory)
        self.category.setColor(wx.RED)
        self.assertEqual(2, len(self.events))
