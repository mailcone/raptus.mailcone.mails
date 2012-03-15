import grok

from megrok import rdb

from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, String, Date, Text, Boolean

from raptus.mailcone.core import bases
from raptus.mailcone.core import database
from raptus.mailcone.core.interfaces import IMailcone, ISearchable
from raptus.mailcone.mails import interfaces



class MailContainer(bases.QueryContainer):
    grok.implements(interfaces.IMailContainer)
    
    def query(self):
        return self.session.query(Mail)

@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_mails_container(obj, event):
    obj['mails'] = MailContainer()

class MailContainerLocator(bases.BaseLocator):
    splitedpath = ['mails']
grok.global_utility(MailContainerLocator, provides=interfaces.IMailContainerLocator)



class Attachment(bases.ORMModel):
    grok.implements(interfaces.IAttachment)
    database.schema(interfaces.IAttachment)
    rdb.metadata(database.create_metadata)
    rdb.tablename('attachments')
    
    id = Column(Integer, primary_key=True)
    mail_id = Column(Integer, ForeignKey('mails.id'))



class Tag(bases.ORMModel):
    grok.implements(interfaces.ITag)
    database.schema(interfaces.ITag)
    rdb.metadata(database.create_metadata)
    rdb.tablename('tags')
    
    id = Column(Integer, primary_key=True)
    mail_id = Column(Integer, ForeignKey('mails.id'))


class Mail(bases.ORMModel):
    grok.implements(interfaces.IMail)
    database.schema(interfaces.IMail)
    rdb.metadata(database.create_metadata)
    rdb.tablename('mails')
    
    # all other attributes are set with the directive database.schema()
    id = Column (Integer, primary_key=True, unique=True)
    index_searchable = Column(String, index=True)
    attachments = relation(Attachment, lazy='immediate')
    tags = relation(Tag, lazy='immediate')

indexes = ('id', 'date', 'mail_from', 'subject', 'organisation', 'processed_on',)
@grok.subscribe(interfaces.IMail, grok.IObjectModifiedEvent)
def mails_index_searchable(obj, event):
    obj.index_searchable = ''
    for i in indexes:
        obj.index_searchable += ' ' +str(getattr(obj, i))







