import os
import grok
from megrok import rdb

from zope import component
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.http import IResult

from raptus.mailcone.layout.views import Page, DisplayForm, DeleteForm
from raptus.mailcone.layout.datatable import BaseDataTableSql
from raptus.mailcone.layout.interfaces import IOverviewMenu
from raptus.mailcone.layout.navigation import locatormenuitem

from raptus.mailcone.mails import _
from raptus.mailcone.mails import interfaces
from raptus.mailcone.mails import contents


grok.templatedir('templates')





class MailsDataTable(BaseDataTableSql):
    grok.context(interfaces.IMailContainer)
    interface_fields = interfaces.IMail
    select_fields = ['id', 'date', 'mail_from', 'subject', 'organisation', 'processed_on']
    model = contents.Mail
    actions = ( dict( title = _('delete'),
                      cssclass = 'ui-icon ui-icon-trash ui-modal-minsize ui-datatable-ajaxlink',
                      link = 'deletemailform'),)


class Mails(Page):
    grok.name('index')
    grok.context(interfaces.IMailContainer)
    locatormenuitem(IOverviewMenu, interfaces.IMailContainerLocator, _(u'Mails'))
    
    @property
    def mailstable(self):
        return MailsDataTable(self.context, self.request).html()



class MailDisplayForm(DisplayForm):
    grok.name('mail_display_form')
    grok.context(interfaces.IMail)
    form_fields = grok.Fields(interfaces.IMail).omit('attachments', 'content', 'multiparts', 'tags')



class Mail(grok.View):
    grok.name('index')
    grok.context(interfaces.IMail)

    @property
    def displayform(self):
        return component.getMultiAdapter((self.context, self.request), name='mail_display_form')()
    
    @property
    def content(self):
        return self.context.content.replace('\n', '<br/>')
    
    @property
    def attachments(self):
        li = list()
        for attachment in self.context.attachments:
            di = dict(id=attachment.id,
                      file=os.path.basename(attachment.path),
                      path=attachment.path,
                      size=self.sizeof_fmt(attachment.filesize),
                      url=self.url(name='attachment', data=dict(attachment_id=attachment.id)))
            li.append(di)
        return li
    
    def sizeof_fmt(self, num):
        """  http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
        """
        for x in ['bytes','KB','MB','GB','TB']:
            if num < 1024.0:
                return "%3.1f%s" % (num, x)
            num /= 1024.0


class DeleteMailForm(DeleteForm):
    grok.context(interfaces.IMail)
    grok.require('zope.View')
    
    def item_title(self):
        return _('Mail ${id}', mapping=dict(id=self.context.id))


class File(object):
    grok.implements(IResult)
    
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        f = open(self.path)
        for i in f:
            yield i
        f.close()



class Attachment(grok.View):
    grok.name('attachment')
    grok.context(interfaces.IMail)

    def headers(self, path):
        self.request.response.setHeader('Content-Disposition', 'attachment; filename=%s' % os.path.basename(path))
        self.request.response.setHeader('Content-Length', os.path.getsize(path))

    def render(self, attachment_id):
        attachment = rdb.Session().query(contents.Attachment).get(attachment_id)
        path = attachment.path

        if not os.path.exists(path):
            raise NotFound(self, 'File missing at %s' % path)
        file = File(path)
        self.headers(path)
        return file




