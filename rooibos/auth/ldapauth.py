from __future__ import absolute_import
import logging

from django.contrib.auth.models import User
from django.conf import settings

import ldap

from .baseauth import BaseAuthenticationBackend

log = logging.getLogger(__name__)


class LdapAuthenticationBackend(BaseAuthenticationBackend):
    """
        Django Middleware class to facilitate using LDAP to authenticate users
        Note that "class has no __init__ method" errors from pep-8 linting can be safely ignored
            see: https://docs.djangoproject.com/en/1.6/topics/http/middleware/#init
    """
    def authenticate(self, username=None, password=None):
        for ldap_auth in settings.LDAP_AUTH:
            log.debug('logging in %s' % username)

            try:
                username = username.strip()
                l = ldap.initialize(ldap_auth['uri'])
                l.protocol_version = ldap_auth['version']
                for option, value in ldap_auth['options'].iteritems():
                    l.set_option(getattr(ldap, option), value)

                if ldap_auth.get('bind_user'):
                    dn = get_dn(username)
                    if dn:
                        if type(dn) in (tuple, list):
                            dn = dn[0]

                    log.debug('using bind user %s to bind' % ldap_auth['bind_user'])
                else:
                    dn = '%s=%s,%s' % (ldap_auth['cn'],
                                       username, ldap_auth['base'])

                if user_bind(dn, password):
                    # if the dn/password combination matches, get attributes
                    result = l.search_s(ldap_auth['base'],
                                        ldap_auth['scope'],
                                        '%s=%s' % (ldap_auth['cn'], username),
                                        attrlist=ldap_auth['attributes'])
                    if len(result) != 1:
                        continue
                    attributes = result[0][1]
                    for attr in ldap_auth['attributes']:
                        if attr in attributes:
                            if not type(attributes[attr]) in (tuple, list):
                                attributes[attr] = (attributes[attr],)
                        else:
                            attributes[attr] = []
                    try:
                        user = User.objects.get(username=username)
                    except User.DoesNotExist:
                        user = self._create_user(username,
                                                 None,
                                                 ' '.join(attributes[ldap_auth['firstname']]),
                                                 ' '.join(attributes[ldap_auth['lastname']]),
                                                 attributes[ldap_auth['email']][0])
                    if not self._post_login_check(user, attributes):
                        continue
                    return user
            # except ldap.LDAPError, error_message:
            except Exception as e:
                log.debug('LDAP error: %s' % e)
            finally:
                if l in locals():
                    l.unbind_s()
        return None


def get_dn(user_name, dn=None):
    """
    Takes a user name and search LDAP using the bind user defined in settings_LDAP_AUTH
    :param user_name: a username (as input on a login form)
    :param dn:  the corresponding dn for the username (set to None by default)
    :return: dn, which should either be a valid dn for a user bind or None
    """
    for ldap_auth in settings.LDAP_AUTH:
        ldap_object = ldap.initialize(ldap_auth['uri'])
        ldap_object.protocol_version = ldap_auth['version']
        base = ldap_auth['base']
        scope = ldap_auth['scope']
        cn = ldap_auth['cn']
        dn_label = ldap_auth['dn']
        bind_user = ldap_auth['bind_user']
        bind_pass = ldap_auth['bind_password']
        for option, value in ldap_auth['options'].iteritems():
            ldap_object.set_option(getattr(ldap, option), value)

        # login as bind user to search for user attempting to login
        try:
            ldap_object.simple_bind(bind_user, bind_pass)
            search = '%s=%s' % (cn, user_name)
            nic = ldap_object.search_s(base, scope, search, [dn_label])
            dn_value = nic[0][1][dn_label][0]
            dn = '%s=%s,%s' % (dn_label, dn_value, base)
            if settings.DEBUG:
                log.debug('binding with bind_user %s' % bind_user)
                log.debug('search = %s, nic = %s' % (search, nic))
                log.debug('dn_value = %s, dn = %s' % (dn_value, dn))
                log.debug('returning dn for %s: \'%s\'' % (user_name, dn))
        except Exception as e:
            log.exception(e)

    return dn


def user_bind(dn, password, authentication_result=False):
    log.debug('dn: \'%s\'' % dn)
    # set up ldap connection
    for ldap_auth in settings.LDAP_AUTH:

        user_bind = ldap.initialize(ldap_auth['uri'])
        user_bind.protocol_version = ldap_auth['version']
        for option, value in ldap_auth['options'].iteritems():
            user_bind.set_option(getattr(ldap, option), value)

            # simple_bind returns an int, which is used to lookup the result using the LDAP object,
            # in this case user_bind.result(int)
            # which returns the tuple (97, []) with a successful userid/credential pairing]
        try:
            log.debug('bind dn = %s' % dn)
            ldap_response = user_bind.simple_bind(dn, password)
            bind_result = user_bind.result(ldap_response)

            if bind_result[0] == 97:
                authentication_result = True
            else:
                log.info('login failed for %s - LDAP response: %s' % (dn, user_bind.result(ldap_response)))
        # this should probably be ldap.Exception - but it's throwing errors?
        except ldap.LDAPError as e:
            log.debug('error binding %s' % dn)
            log.exception(e)

    # authentication_result is false unless the simple_bind() returns (97, []) as a result
    return authentication_result


def ldap_init(ldap_settings=settings.LDAP_AUTH):
    """
    TODO: figure out why this doesn't work
    ... it would be nice to be DRY with initializing an LDAP object
    but I get connection errors and timeouts when I try to use this function
    I'm thinking it might be the python-ldap feature that auto-closes the connection?
    :return: ldap_object that doesn't work
    """
    for ldap_auth in settings.LDAP_AUTH:
        ldap_object = ldap.initialize(ldap_auth['uri'])
        ldap_object.protocol_version = ldap_auth['version']

        for key in ldap_auth:
            setattr(ldap_object, key, ldap_auth[key])
            # the resulting object will have the LDAP settings as attributes,
            # i.e.
            #     lo = ldap_init();
            #     lo.uri  #  will be the value of settings.LDAP_AUTH['uri']

        # if ldap_auth.get('bind_user'):
        #     ldap_object.bind_user = ldap_auth.get('bind_user')
        #     ldap_object.bind_password = ldap_auth.get('bind_password')
        for option, value in ldap_auth['options'].iteritems():
            ldap_object.set_option(getattr(ldap, option), value)

        return ldap_object

