import grok

from zope.schema import vocabulary

from zope.schema.interfaces import IList

from raptus.mailcone.mails import _
from raptus.mailcone.mails import interfaces





register = vocabulary.getVocabularyRegistry().register
def vocabulary_mailattributes(context):
    terms = list()
    for field in grok.AutoFields(interfaces.IMail):
        if IList.providedBy(field.field):
            name = '%s %s' % (field.field.title, _('(List)'),)
        else:
            name = field.field.title
        terms.append(vocabulary.SimpleTerm(value=field.field.getName(), title=name))
    return vocabulary.SimpleVocabulary(terms)
register('raptus.mailcone.mails.mailattributes', vocabulary_mailattributes)
