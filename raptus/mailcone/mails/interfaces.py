from zope import interface
from zope import interface, schema

from raptus.mailcone.core.interfaces import IContainer
from raptus.mailcone.core.interfaces import IContainerLocator

from raptus.mailcone.mails import _



class IMailContainer(IContainer):
    """ A container for all mails. Note that all
        mails came from a sql db! this container
        serve only as mount point for all mails
    """



class IMailContainerLocator(IContainerLocator):
    """ interface for locate the mails folder.
    """



class IMail(interface.Interface):
    """ A single mail
    """

    id =  schema.Int(title=_(u'Id'), required=True,)
    date =  schema.Date(title=_(u'Date'), required=True,)
    mail_from = schema.TextLine(title=_(u'Mail from'), required=True, max_length=250)
    mail_from_domain = schema.TextLine(title=_(u'Mail from Domain'), required=True, max_length=250)
    organisation = schema.TextLine(title=_(u'Organisation'), required=True, max_length=250)
    mail_to = schema.TextLine(title=_(u'Mail to'), required=True, max_length=250)
    mail_to_domain = schema.TextLine(title=_(u'Mail to domain'), required=True, max_length=250)
    mail_cc = schema.TextLine(title=_(u'Mail CC'), required=True, max_length=250)
    in_reply_to = schema.TextLine(title=_(u'In reply to'), required=True, max_length=250)
    mail_references = schema.Text(title=_(u'Mail References'), required=True,)
    header = schema.Text(title=_(u'Header'), required=True,)
    subject = schema.TextLine(title=_(u'Subject'), required=True, max_length=250)
    content = schema.Text(title=_(u'Content'), required=True,)
    path_to_attachments = schema.Text(title=_(u'Attachments'), required=True,)
    matched = schema.Bool(title=_(u'Matched'), required=True,)
    match_on = schema.Date(title=_(u'Match on'), required=True,)

