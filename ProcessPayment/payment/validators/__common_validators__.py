import re
try:
    from urllib.parse import urlsplit, urlunsplit
except ImportError:  # Python 2
    from urlparse import urlsplit, urlunsplit

from django.core.validators import RegexValidator
from django.utils.encoding import force_text
from django.core.exceptions import ValidationError
from tastypie.validation import FormValidation
from django.core.exceptions import ImproperlyConfigured
from tastypie.fields import RelatedField
from tastypie.resources import ModelResource
from tastypie.bundle import Bundle

def validateZeroOrMore(val):
    if val < 0:
        raise ValidationError(u'%s is not a valid value - must be zero or more' % val)

class AaepCustomURLValidator(RegexValidator):
    regex = re.compile(
        r'^((?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r')?'  # -anto:2013NOV03- make host port part optional
        r'(?:'
        #r'/?|'
        #r'[/?]'
        r'\S+)$', re.IGNORECASE)

    def __call__(self, value):
        try:
            super(AaepCustomURLValidator, self).__call__(value)
        except ValidationError as e:
            # Trivial case failed. Try for possible IDN domain
            if value:
                value = force_text(value)
                scheme, netloc, path, query, fragment = urlsplit(value)
                try:
                    netloc = netloc.encode('idna').decode('ascii')  # IDN -> ACE
                except UnicodeError:  # invalid domain part
                    raise e
                url = urlunsplit((scheme, netloc, path, query, fragment))
                super(AaepCustomURLValidator, self).__call__(url)
            else:
                raise
        else:
            url = value


class ModelFormValidation(FormValidation):
    """
    Override tastypie's standard ``FormValidation`` since this does not care
    about URI to PK conversion for ``ToOneField`` or ``ToManyField``.
    """

    resource = ModelResource

    def __init__(self, **kwargs):
        if not 'resource' in kwargs:
            raise ImproperlyConfigured("You must provide a 'resource' to 'ModelFormValidation' classes.")

        self.resource = kwargs.pop('resource')

        super(ModelFormValidation, self).__init__(**kwargs)


    def _get_pk_from_resource_uri(self, resource_field, resource_uri):
        """ Return the pk of a resource URI """
        base_resource_uri = resource_field.to().get_resource_uri()
        if not resource_uri.startswith(base_resource_uri):
            raise Exception("Couldn't match resource_uri {0} with {1}".format(
                                        resource_uri, base_resource_uri))
        before, after = resource_uri.split(base_resource_uri)
        return after[:-1] if after.endswith('/') else after

    def form_args(self, bundle):
        import logging
        rsc = self.resource()
        kwargs = super(ModelFormValidation, self).form_args(bundle)

        for name, rel_field in rsc.fields.items():
            data = kwargs['data']
            if not issubclass(rel_field.__class__, RelatedField):
                continue # Not a resource field
            if name in data and data[name] is not None:
                #resource_uri = (data[name] if rel_field.full is False
                #                            else data[name]['resource_uri'])

                resource_uri = (data[name])
                logging.debug("kkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
                logging.debug(resource_uri)
                if isinstance(resource_uri,Bundle):
                    logging.debug("successss")
                    resource_uri = resource_uri.data['resource_uri']
                    logging.debug(resource_uri)
                pk = self._get_pk_from_resource_uri(rel_field, resource_uri)
                kwargs['data'][name] = pk

        return kwargs

