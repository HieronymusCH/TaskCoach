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

import re

name = 'Task Coach'
description = 'Your friendly task manager'
version = '0.70.4'
release_month = 'September'
release_month_nr = '%02d'%(['January', 'February', 'March', 'April', 'May', 
                    'June', 'July', 'August', 'September', 'October', 
                    'November', 'December'].index(release_month) + 1)
release_day = '28'
release_day_nr = '%02d'%int(release_day)
release_year = '2008'
release_status = 'alpha'
date = release_month + ' ' + release_day + ', ' + release_year
long_description = 'Task Coach is a simple open source todo manager to manage' \
' personal tasks and todo lists. It grew out of a frustration that ' \
'well-known task managers, such as those provided with Outlook or Lotus ' \
'Notes, do not provide facilities for composite tasks. Often, tasks and ' \
'other things todo consist of several activities. Task Coach is designed ' \
'to deal with composite tasks. '
keywords = 'task manager, todo list, pim, time registration, track effort'
author_first = 'Frank' # Needed for PAD file
author_last = 'Niessink'# Needed for PAD file
author = '%s %s and Jerome Laheurte'%(author_first, author_last)
author_email = 'developers@taskcoach.org'
filename = 'TaskCoach'
filename_lower = filename.lower()
url = 'http://www.taskcoach.org/'
screenshot = url + 'screenshot-0.62-treeview.png'
icon = url + 'taskcoach.png'
pad = url + 'pad.xml'
download = url + 'download.html'
dist_download_prefix = 'http://downloads.sourceforge.net/%s'%filename_lower
copyright = 'Copyright (C) 2004-%s %s'%(release_year, author)
license_title = 'GNU General Public License'
license_version = '3'
license_title_and_version = '%s version %s'%(license_title, license_version) 
license = '%s or any later version'%license_title_and_version
license_title_and_version_abbrev = 'GPLv%s'%license_version
license_abbrev = '%s+'%license_title_and_version_abbrev
license_notice = '''Task Coach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Task Coach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

license_notice_html = '<p>%s</p>'%license_notice.replace('\n\n', '</p><p>')
license_notice_html = re.sub(r'<http([^>]*)>', r'<a href="http\1" target="_blank">http\1</a>', license_notice_html)

platform = 'Any'
pythonversion = '2.4'
wxpythonversion = '2.8.6.0-unicode'
languages = {
    'English': None, 
    'Breton': 'br',
    'Bulgarian': 'bg',
    'Chinese (Simplified)': 'zh_CN',
    'Chinese (Traditional)': 'zh_TW',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'Finnish': 'fi',
    'French': 'fr', 
    'Galician': 'gl',
    'German': 'de',
    'Greek': 'el',
    'Hebrew': 'he',
    'Hungarian': 'hu',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Latvian': 'lv',
    'Norwegian (Bokmal)': 'nb',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Portuguese (Brazilian)': 'pt_BR',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Slovak': 'sk',
    'Spanish': 'es',
    'Swedish': 'sv',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukranian': 'uk'}
languages_list = ','.join(languages.keys())

def __createDict(locals):
    ''' Provide the local variables as a dictionary for use in string
        formatting. '''
    metaDict = {}
    for key in locals:
        if not key.startswith('__'):
            metaDict[key] = locals[key]
    return metaDict

metaDict = __createDict(locals())

