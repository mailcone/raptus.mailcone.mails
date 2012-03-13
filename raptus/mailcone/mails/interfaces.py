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


class IStringList(interface.Interface):
    """ reprencent a list with string
    """
    id =  schema.Int(title=_(u'Id'), required=True,)
    value = schema.TextLine(title=_(u'Value of this list'), required=True,)


class IAttachment(interface.Interface):
    """ attachment path
    """
    id =  schema.Int(title=_(u'Id'), required=True,)
    mail_id = schema.Int(title=_(u'Id'), required=True,)
    path =  schema.TextLine(title=_(u'Path to attachment'), required=True,)
    filesize = schema.Int(title=_(u'File size'), required=True,)



class ITag(interface.Interface):
    id =  schema.Int(title=_(u'Id'), required=True,)
    name =  schema.TextLine(title=_(u'Tag name'), required=True,)



class IMail(interface.Interface):
    """ A single mail
    """

    id =  schema.Int(title=_(u'Id'), required=True,)
    date =  schema.Date(title=_(u'Date'), required=True,)
    mail_from = schema.TextLine(title=_(u'Mail from'), required=True, max_length=250)
    mail_from_domain = schema.TextLine(title=_(u'Mail from Domain'), required=True, max_length=250)
    organisation = schema.TextLine(title=_(u'Organisation'), required=True, max_length=250)
    subject = schema.TextLine(title=_(u'Subject'), required=True, max_length=250)
    mail_to = schema.List(title=_(u'Mail to'),
                          required=True,
                          value_type=schema.TextLine(title=_(u'Mail to'), required=True, max_length=250))
    mail_to_domain = schema.List(title=_('Mail To Domain'),
                                 required=True,
                                 value_type=schema.TextLine(title=_(u'Mail To Domain'), required=True, max_length=250))
    mail_cc = schema.List(title=_(u'Mail CC'),
                          required=True,
                          value_type=schema.TextLine(title=_(u'Mail CC'), required=True, max_length=250))
    mail_cc_domain = schema.List(title=_('Mail CC Domain'),
                                 required=True,
                                 value_type=schema.TextLine(title=_(u'Mail CC Domain'), required=True, max_length=250))
    mail_bbc = schema.List(title=_(u'Mail BBC'),
                          required=True,
                          value_type=schema.TextLine(title=_(u'Mail BBC'), required=True, max_length=250))
    mail_bbc_domain = schema.List(title=_('Mail BBC Domain'),
                                 required=True,
                                 value_type=schema.TextLine(title=_(u'Mail BBC Domain'), required=True, max_length=250))
    precedence = schema.TextLine(title=_(u'Precedence'), required=True, max_length=250)
    received = schema.List(title=_(u'Received'),
                          required=True,
                          value_type=schema.TextLine(title=_(u'Received'), required=True, max_length=1000))
    reply_to = schema.TextLine(title=_(u'Reply-To'), required=True, max_length=250)
    sender = schema.TextLine(title=_(u'Sender'), required=True, max_length=250)
    content = schema.Text(title=_(u'Content'), required=True,)
    attachments = schema.List(title=_(u'Attachments'),
                              required=True,
                              value_type=schema.Object(schema=IAttachment))
    header = schema.Text(title=_(u'Header'), required=True,)
    mime_version = schema.Text(title=_(u'Mime Version'), required=True,)
    x_source_ip = schema.TextLine(title=_(u'X-SourceIP'), required=True, max_length=250)
    
    processed_on = schema.Date(title=_('Processed on'), required=True,)




