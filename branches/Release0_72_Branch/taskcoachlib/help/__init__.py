'''
Task Coach - Your friendly task manager
Copyright (C) 2004-2009 Frank Niessink <frank@niessink.com>

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

from taskcoachlib import meta
from taskcoachlib.i18n import _
from tips import showTips

_MSURL = "http://www.microsoft.com/downloadS/details.aspx?familyid=200B2FD9-AE1A-4A14-984D-389C36F85647&displaylang=en"

_TOC = _('''<h3>Table of contents</h3>
<ul>
<li><a href="#tasks">Tasks</a>
    <ul>
        <li><a href="#abouttasks">About tasks</a></li>
        <li><a href="#taskproperties">Task properties</a></li>
        <li><a href="#taskstates">Task states</a></li>
        <li><a href="#taskcolors">Task colors</a></li>
    </ul>
</li>
<li><a href="#effort">Effort</a>
    <ul>
        <li><a href="#abouteffort">About effort</a></li>
        <li><a href="#effortproperties">Effort properties</a></li>
    </ul>
</li>
<li><a href="#categories">Categories</a>
    <ul>
        <li><a href="#aboutcategories">About categories</a></li>
        <li><a href="#categoryproperties">Category properties</a></li>
    </ul>
</li>
<li><a href="#email">E-mail (Outlook &amp; Thunderbird) integration</a>
  <ul>
    <li><a href="#aboutemail">About e-mail integration</a></li>
    <li><a href="#emailattach">Attaching an e-mail to a task</a></li>
    <li><a href="#emailcreate">Creating a task from an e-mail</a></li>
  </ul>
</li>
<li><a href="#syncml">SyncML support</a>
  <ul>
    <li><a href="#aboutsyncml">What is SyncML</a></li>
    <li><a href="#syncmlsetup">Setup</a></li>
    <li><a href="#syncmllimits">Limitations</a></li>
    <li><a href="#syncmltrouble">Troubleshooting</a></li>
    <li><a href="#syncmlpurge">Purging deleted items</a></li>
  </ul>
</li>
<li><a href="#templates">Task templates</a>
  <ul>
    <li><a href="#abouttemplates">About templates</a></li>
    <li><a href="#usingtemplates">Using templates</a></li>
  </ul>
</li>
</ul>
''')

_taskSection = _('''<h3><a name="tasks">Tasks</a></h3>
''')

_aboutTasksSubsection = _('''<h4><a name="abouttasks">About tasks</a></h4>
 
<p>Tasks are the basic objects that you manipulate. Tasks can
represent anything from a simple little thing you have to do, like buying a gift
for your loved one, to a complete project, consisting of different phases, and
numerous activities.</p>
''')

_taskPropertiesSubsection = _('''<h4><a name="taskproperties">Task 
properties</a></h4>

<p>Tasks have the following properties you can change:
<ul>
<li>Subject: a single line that summarizes the task.</li>
<li>Description: a multi-line description of the task.</li>
<li>Due date: the date the task should be finished. This can be 'None' 
indicating that this task has no fixed due date.</li>
<li>Start date: the first date on which the task can be started. The start date 
defaults to the date the task is created. It can also be 'None' indicating that
you don't really want to start this task. This can be convenient for e.g. 
registering sick leave.</li>
<li>Completion date: this date is 'None' as long as the task has not been 
completed. It is set to the current date when you mark the task as completed. 
The completion date can also be entered manually.</li>
<li>Budget: amount of hours available for the task.</li>
<li>Hourly fee: the amount of money earned with the task per hour.</li>
<li>Fixed fee: the amount of money earned with the task regardless of the time
spent.</li>
</ul></p>

<p>The following properties are calculated from the properties above:
<ul>
<li>Days left: the number of days left until the due date.</li>
<li>Total budget: sum of task budget and the budgets of all subtasks of the 
task, recursively.</li>
<li>Time spent: effort spent on the task.</li>
<li>Total time spent: effort spent on the task and all subtasks, 
recursively.</li>
<li>Budget left: task budget minus time spent on the task.</li>
<li>Total budget left: total task budget minus total time spent.</li>
<li>Total fixed fee: sum of fixed fee of the task and the fixed fees of all 
subtasks of the task, recursively.</li>
<li>Revenue: hourly fee times hours spent plus fixed fee.</li>
<li>Total revenue: sum of task revenue and revenue of all subtasks, 
recursively.</li>
</ul></p>
''')

_taskStatesSubsection = _('''<h4><a name="taskstates">Task states</a></h4>

<p>Tasks always have exactly one of the following states:
<ul>
<li>Active: the start date is in the past and the due date in the future;</li>
<li>Inactive: the start date is in the future, or</li>
<li>Completed: the task has been completed.</li>
</ul></p>

<p>In addition, tasks can be referenced as:
<ul>
<li>Over due: the due date is in the past;</li>
<li>Due today: the due date is today;</li>
<li>Over budget: no buget left;</li>
<li>Under budget: still budget left;</li>
<li>No budget: the task has no budget.</li>
</ul></p>
 ''')

_taskColorsSubsection = _('''<h4><a name="taskcolors">Task colors</a></h4>

<p>The text of tasks is colored according to the following rules:
<ul>
<li>Over due tasks are red;</li>
<li>Tasks due today are orange;</li>
<li>Active tasks are black text with a blue icon;</li>
<li>Future tasks are gray, and</li>
<li>Completed tasks are green.</li>
</ul>
This all assumes you have not changed the text colors through the preferences 
dialog, of course.</p>
<p>The background color of tasks is determined by the categories the task
belongs to, see the section about 
<a href="#categoryproperties">category properties</a> below.</p>
''')

_effortSection = _('''<h3><a name="effort">Effort</a></h3>
''')

_aboutEffortSubsection = _('''<h4><a name="abouteffort">About effort</a></h4>

<p>Whenever you spent time on tasks, you can record the amount of time
spent by tracking effort. Select a task and invoke 'Start tracking effort' in
the Effort menu or the context menu or via the 'Start tracking effort' toolbar 
button.</p>
''')

_effortPropertiesSubsection = _('''<h4><a name="effortproperties">Effort
properties</a></h4>

<p>Effort records have the following properties you can change:
<ul>
<li>Task: the task the effort belongs to.</li>
<li>Start date/time: start date and time of the effort.</li>
<li>Stop date/time: stop date and time of the effort. This can be 'None' as 
long as you are still working on the task.</li>
<li>Description: a multi-line description of the effort.</li>
</ul></p>

<p>The following properties are calculated from the properties above:
<ul>
<li>Time spent: how much time you have spent working on the task.</li>
<li>Total time spent: sum of time spent on the task and all subtasks, 
recursively.</li>
<li>Revenue: money earned with the time spent.</li>
<li>Total revenue: money earned with the total time spent.</li>
</ul></p>
''')

_categorySection = _('''<h3><a name="categories">Categories</a></h3>
''')

_aboutCategoriesSubSection = _('''<h4><a name="aboutcategories">About 
categories</a></h4>

<p>Tasks may belong to one or more categories. First, you need to create the
category that you want to use via the 'Category' menu. Then, you can add a task to
one or more categories by editing the task and checking the relevant categories
for that task in the category pane of the task editor.</p>

<p>You can limit the tasks shown in the task viewers to one or more categories
by checking a category in the category viewer. For example, if you have a 
category 'phone calls' and you check that category, the task viewers will 
only show tasks belonging to that category; in other words the phone calls 
you need to make.</p>
''')

_categoryPropertiesSubSection = _('''<h4><a name="categoryproperties">Category 
properties</a></h4>

<p>Categories have a subject, a description, and a color. The color is used
to render the background of the category and the background of tasks that
belong to that category. If a category has no color of its own, but it has
a parent category with a color, the parent's color will be used.  
If a task belongs to multiple categories that each have a color associated with
them, a mixture of the colors will be used to render the background of that
task.</p>
''')

_emailSection = _('''<h3><a name="email">E-mail (Outlook &amp; Thunderbird) integration</a></h3>
''')

_aboutEmailSubsection = _('''<h4><a name="aboutemail">About e-mail integration</a></h4>

<p>%(name)s integrates with both Outlook and Thunderbird mail user
agents, through drag and drop. This has some limitations; e-mails are
copied in a directory next to the %(name)s file, as .eml files and are
later opened using whatever program is associated with this file type
on your system. On the other hand, this allows you to open these
e-mail attachments on a system which is different from the one you
created it first.</p>

<p>Due to a Thunderbird limitation, you can't drag and drop several
e-mails from Thunderbird. This does not apply to Outlook.</p>
''') % meta.metaDict

_emailAttachingSubsection = _('''<h4><a name="emailattach">Attaching an e-mail to a task</a></h4>

<p>There are two ways to attach an e-mail to a task; you can

<ul>
  <li>Drop it on a task either in the task tree or the task list.</li>
  <li>Drop it in the attachment pane in the task editor.</li>
</ul>

</p>
''')

_emailCreatingSubsection = _('''<h4><a name="emailcreate">Creating a task from an e-mail</a></h4>

<p>Dropping an e-mail on an empty part of the task tree or task list
creates a new task. Its subject is the subject of the mail, its
description is its content. Additionnaly, the mail is automatically
attached to the newly created task.</p>
''')

_syncmlSection = _('''<h3><a name="syncml">SyncML support</a></h3>
''')

_aboutSyncmlSubsection = _('''<h4><a name="aboutsyncml">What is SyncML</a></h4>

<p>This feature is optional and off by default. In order to turn it on,
go to the preferences dialog and check it in the Features page.</p>

<p>SyncML  is   an  XML  protocol  designed   to  synchronize  several
applications  with  a  server.  A  popular open-source  server  is  <a
href="http://www.funambol.com/">Funambol</a>.  Synchronization clients
are available  for many devices and applications  (Outlook, Pocket PC,
iPod, iPhone,  Evolution, etc...),  as well as  so-called "connectors"
which allow the server  to synchronize with Exchange, Google Calendar,
etc.</p>

<p>%(name)s has built-in SyncML client support. This means you can
setup %(name)s to synchronize with the same SyncML server you
synchronize with with Outlook and have all Outlook tasks and notes in
your %(name)s file, as well as %(name)s tasks and notes in Outlook. Or
your Pocket PC.</p>

''') % meta.metaDict

_syncmlSetupSubsection = _('''<h4><a name="syncmlsetup">Setup</a></h4>

<p>To setup SyncML, edit the SyncML preferences in Edit/SyncML preferences.
Fill in the synchronization URL, your ID on the server and choose which
items to synchronize (tasks and/or notes). The URL depends on the server
you choose; some examples are:

<ul>
  <li><a href="http://www.scheduleworld.com/">ScheduleWorld</a>: http://sync.scheduleworld.com/funambol/ds</li>
  <li><a href="http://memotoo.com">MemoToo</a>: http://sync.memotoo.com/syncml</li>
</ul>

The database names are pretty standard; the default values should work.</p>

<p>Each task file has its own client ID, so that two different task files
will de considered different "devices" by the server.</p>''')

_syncmlLimitsSubsection = _('''<h4><a name="syncmllimits">Limitations</a></h4>

<p>Some limitations are due to the fact that, the underlying data type being vcalendar, some TaskCoach features cannot be presented to the server.

  <ul>
    <li>Task and category hierarchy are lost to the server.</li>
    <li>Recurrence and reminders are not supported yet.</li>
    <li>Note categories are lost to the server.</li>
    <li>The conflict detection/resolution system is a work around a Funambol
        limitation. It should work in most cases, but if many applications
        synchronize with the same server at the same time, problems may rise.</li>
    <li>Probably some others...</li>
  </ul>
</p>
''')

_syncmlTroubleSubsection = _('''<h4><a name="syncmltrouble">Troubleshooting</a></h4>

<p>The SyncML menu items are only present if your platform is supported.
Currently supported platforms are:

  <ul>
    <li>Windows, 32 bits (see below)</li>
    <li>Linux, 32 bits</li>
    <li>Mac OS 10.3 and later, both Intel and PPC</li>
  </ul>

You may experience problems under Windows if you don't have the Microsoft
Visual 8 runtime installed. You can download it on the
<a target="_blank" href="%s">
Microsoft download site</a>.
</p>
''') % _MSURL

_syncmlPurgeSubsection = _('''<h4><a name="syncmlpurge">Purging deleted items</a></h4>

<p>When SyncML is enabled, deleting a task or a note does not actually
delete it, but rather mark it as deleted. The deleted task or note is
actually removed from the task or note list on the next
synchronization. For this reason, if you happen to use the SyncML
feature, then disable it without having done a sync, there may be some
deleted notes or tasks in your task file. This is not a problem, but
takes a little more disk space.</p>

<p>In this case, the "Purge deleted items" menu item in the File menu can
be used to actually delete these tasks. It is only enabled when you
need it, that is when there are items to purge. Be aware that after doing this,
if you re-enable SyncML and make a sync with the same server you used
previously, all those items will reappear, as the server
doesn't know they're deleted.</p>

<p>In addition, prior to version 0.71.4 of %(name)s, these deleted
tasks and notes were kept around even with the SyncML feature
disabled, so tasks and notes were never actually deleted. the "Purge
deleted items" menu item can be used when upgrading to 0.71.4 to clear
all these unwanted items.</p>
''') % meta.metaDict

_templatesSection = _('''<h3><a name="templates">Task templates</a></h3>
''')

_aboutTemplatesSubsection = _('''<h4><a name="abouttemplates">About templates</a></h4>
<p>Templates are blueprints for new tasks. Right now, the only task properties that
can be "parameterized" are the dates. When instantiating a template, the created
task has its dates replaced with dates relative to the current date.</p>
''')

_usingTemplatesSubsection = _('''<h4><a name="usingtemplates">Using templates</a></h4>
<p>One can create a template by selecting a task (only one) and click on the
"Save task as template" item in the File menu. All subtasks, notes and attachments
are part of the template. Only categories are not saved.</p>

<p>You can also create a new template from a pre-made template file (.tsktmpl);
just select "Add template" in the File menu and select the file. Template files
are stored in a subdirectory of the directory where %(name)s.ini is.</p>

<p>In order to instantiate a task template, use the "New task from template" menu
in the Task menu, or the equivalent toolbar button. When the task is created, the
due, start and completion dates, if applicable, are reevaluated relatively to the
current date. That means that if you create a template from a task starting today
and due tomorrow, every time the template is instantiated, the start date will be
replaced by the current date and the due date by the current date plus one day.</p>
''') % meta.metaDict

helpHTML = _TOC + _taskSection + _aboutTasksSubsection + \
    _taskPropertiesSubsection + _taskStatesSubsection + _taskColorsSubsection + \
    _effortSection + _aboutEffortSubsection + _effortPropertiesSubsection + \
    _categorySection + _aboutCategoriesSubSection + _categoryPropertiesSubSection + \
    _emailSection + _aboutEmailSubsection + _emailAttachingSubsection + _emailCreatingSubsection + \
    _syncmlSection + _aboutSyncmlSubsection + _syncmlSetupSubsection + \
    _syncmlLimitsSubsection + _syncmlTroubleSubsection + _syncmlPurgeSubsection + \
    _templatesSection + _aboutTemplatesSubsection + _usingTemplatesSubsection

aboutHTML = _('''<h4>%(name)s - %(description)s</h4>
<h5>Version %(version)s, %(date)s</h5>
<p>By %(author)s &lt;%(author_email)s&gt;<p>
<p><a href="%(url)s" target="_blank">%(url)s</a></p>
<p>%(copyright)s</p>
<p>%(license_notice_html)s</p>
''')%meta.metaDict

doubleline = '================================================================\n'

header = doubleline + '%(name)s - %(description)s\n'%meta.metaDict + doubleline

aboutText = header + _('''
Version %(version)s, %(date)s

By %(author)s <%(author_email)s>

%(url)s

%(copyright)s
%(license)s

''')%meta.metaDict + doubleline

installText = header + '''

--- Prerequisites ----------------------------------------------

You need Python version %(pythonversion)s or higher and wxPython 
version %(wxpythonversion)s or higher.


--- Testing ----------------------------------------------------

Before installing, you may want to run the unittests included.
Issue the following command:

  cd tests; python test.py

If all goes well, you should see a number of dots appearing and
the message 'Ran X tests in Y seconds. OK'. If not, you'll get
one or more failed tests. In that case, please run the tests
again, redirecting the output to a textfile, like this:

  python test.py 2> errors.txt

Please mail me the errors.txt file and your platform information
(operating system version, Python version and wxPython version).


--- Installation -----------------------------------------------

There are two options to install %(name)s: 

First, you can simply move this directory to some suitable 
location and run taskcoach.py (or taskcoach.pyw if you are on 
the Windows platform) from there.

Alternatively, you can use the Python distutils setup script
to let Python install %(name)s for you. In that case run the
following command:

  python setup.py install

If you have a previous version of %(name)s installed, you may
need to force old files to be overwritten, like this:

  python setup.py install --force

'''%meta.metaDict + doubleline

buildText = header + '''

--- Building ---------------------------------------------------

To be done.

'''%meta.metaDict + doubleline
