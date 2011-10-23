import grok

from raptus.mailcone.layout.views import Page
from raptus.mailcone.layout.datatable import BaseDataTableSql
from raptus.mailcone.layout.interfaces import IOverviewMenu
from raptus.mailcone.layout.navigation import locatormenuitem

from raptus.mailcone.mails import _
from raptus.mailcone.mails import interfaces
from raptus.mailcone.mails.contents import Mail



grok.templatedir('templates')

class MailsDataTable(BaseDataTableSql):
    grok.context(interfaces.IMailContainer)
    interface_fields = interfaces.IMail
    select_fields = ['id', 'date', 'mail_from', 'subject', 'organisation', 'processed_on']
    model = Mail


class Mails(Page):
    grok.name('index')
    grok.context(interfaces.IMailContainer)
    locatormenuitem(IOverviewMenu, interfaces.IMailContainerLocator, _(u'Mails'))
    
    @property
    def mailstable(self):
        return MailsDataTable(self.context, self.request).html()