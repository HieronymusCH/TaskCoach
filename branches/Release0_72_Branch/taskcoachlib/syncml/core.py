'''
Task Coach - Your friendly task manager
Copyright (C) 2008 Jerome Laheurte <fraca7@free.fr>

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

import sys, os

_BINBASE = os.path.join(os.path.split(__file__)[0], '..', 'bin.in')

if sys.platform == 'linux2':
    sys.path.insert(0, os.path.join(_BINBASE, 'linux'))
elif sys.platform == 'darwin':
    sys.path.insert(0, os.path.join(_BINBASE, 'macos'))
else:
    sys.path.insert(0, os.path.join(_BINBASE, 'windows'))

from _pysyncml import *
