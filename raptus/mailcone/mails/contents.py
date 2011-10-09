import grok

from megrok import rdb

from sqlalchemy import Column, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
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


class Attachment(rdb.Model):
    grok.implements(interfaces.IAttachment)
    database.schema(interfaces.IAttachment)
    rdb.metadata(database.create_metadata)
    rdb.tablename('attachments')
    
    id = Column(Integer, primary_key=True)
    mail_id = Column(Integer, ForeignKey('mails.id'))


class Mail(rdb.Model):
    grok.implements(interfaces.IMail)
    database.schema(interfaces.IMail)
    rdb.metadata(database.create_metadata)
    rdb.tablename('mails')
    
    # all other attributes are set with the directive database.schema()
    id = Column ('id', Integer, Sequence('mail_id_seq'), primary_key=True)
    attachments = relationship(Attachment)



