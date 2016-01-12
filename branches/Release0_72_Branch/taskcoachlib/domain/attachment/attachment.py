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

import os, shutil, urlparse
from taskcoachlib import patterns, mailer
from taskcoachlib.domain import base
from taskcoachlib.thirdparty import desktop
from taskcoachlib.i18n import _
from taskcoachlib.domain.note.noteowner import NoteOwner


def getRelativePath(path, base=os.getcwd()):
    """Tries to guess the relative version of 'path' from 'base'. If
    not possible, return absolute 'path'. Both 'path' and 'base' must
    be absolute."""

    path = os.path.realpath(os.path.normpath(path))
    base = os.path.realpath(os.path.normpath(base))

    drv1, pth1 = os.path.splitdrive(path)
    drv2, pth2 = os.path.splitdrive(base)

    # No relative path is possible if the two are on different drives.
    if drv1 != drv2:
        return path

    if pth1.startswith(pth2):
        if pth1 == pth2:
            return ''

        if pth2 == os.path.sep:
            return pth1[1:]

        return pth1[len(pth2) + 1:]

    pth1 = pth1.split(os.path.sep)
    pth2 = pth2.split(os.path.sep)

    while pth1 and pth2 and pth1[0] == pth2[0]:
        pth1.pop(0)
        pth2.pop(0)

    while pth2:
        pth1.insert(0, '..')
        pth2.pop(0)

    return os.path.join(*pth1)


class Attachment(base.Object, NoteOwner):
    ''' Abstract base class for attachments. '''

    type_ = 'unknown'

    def __init__(self, location, *args, **kwargs):
        if not kwargs.has_key('subject'):
            kwargs['subject'] = location

        super(Attachment, self).__init__(*args, **kwargs)

        self.__location = location

    def data(self):
        return None

    def setParent(self, parent):
        # FIXME: We  shouldn't assume that pasted  items are composite
        # in PasteCommand.
        pass

    def location(self):
        return self.__location

    def setLocation(self, location):
        if location != self.__location:
            self.__location = location
            self.notifyObservers(patterns.Event(self, self.locationChangedEventType(), 
                                                location))

    @classmethod
    def locationChangedEventType(class_):
        return '%s.location'%class_
    
    def open(self, workingDir=None):
        raise NotImplementedError

    def __cmp__(self, other):
        try:
            return cmp(self.location(), other.location())
        except AttributeError:
            return 1

    def __getstate__(self):
        try:
            state = super(Attachment, self).__getstate__()
        except AttributeError:
            state = dict()
        state.update(dict(location=self.location()))
        return state

    def __setstate__(self, state):
        try:
            super(Attachment, self).__setstate__(state)
        except AttributeError:
            pass
        self.setLocation(state['location'])

    def __getcopystate__(self):
        return self.__getstate__()

    def __unicode__(self):
        return self.subject()
    
    @classmethod
    def modificationEventTypes(class_):
        eventTypes = super(Attachment, class_).modificationEventTypes()
        return eventTypes + [class_.locationChangedEventType()]


class FileAttachment(Attachment):
    type_ = 'file'

    def open(self, workingDir=None, openAttachment=desktop.open):
        location = self.location()
        if self.isLocalFile():
            if workingDir and not os.path.isabs(location):
                location = os.path.join(workingDir, location)
            location = os.path.normpath(location)
        return openAttachment(location)

    def isLocalFile(self):
        return urlparse.urlparse(self.location())[0] == ''


class URIAttachment(Attachment):
    type_ = 'uri'

    def open(self, workingDir=None):
        return desktop.open(self.location())


class MailAttachment(Attachment):
    type_ = 'mail'

    def __init__(self, location, *args, **kwargs):
        self._readMail = kwargs.pop('readMail', mailer.readMail)
        subject, content = self._readMail(location)

        kwargs.setdefault('subject', subject)
        kwargs.setdefault('description', content)

        super(MailAttachment, self).__init__(location, *args, **kwargs)

    def open(self, workingDir=None):
        return mailer.openMail(self.location())

    def read(self):
        return self._readMail(self.location())

    def data(self):
        return file(self.location(), 'rb').read()


def AttachmentFactory(location, type_=None, *args, **kwargs):
    if type_ is None:
        if location.startswith('URI:'):
            return URIAttachment(location[4:], subject=location[4:], description=location[4:])
        elif location.startswith('FILE:'):
            return FileAttachment(location[5:], subject=location[5:], description=location[5:])
        elif location.startswith('MAIL:'):
            return MailAttachment(location[5:], subject=location[5:], description=location[5:])

        return FileAttachment(location, subject=location, description=location)

    try:
        return { 'file': FileAttachment,
                 'uri': URIAttachment,
                 'mail': MailAttachment }[type_](location, *args, **kwargs)
    except KeyError:
        raise TypeError, 'Unknown attachment type: %s' % type_
