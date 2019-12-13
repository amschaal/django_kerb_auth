from django.conf import settings
import datetime
# import logging
# logger = logging.getLogger('gcportal.debug.krbadmin')

try:
    import kadmin
except:
    pass
class KerberosAdmin(object):
#     This can be retained between requests, so we reinitialize it every so often: 
#     https://code.google.com/archive/p/modwsgi/wikis/ApplicationIssues.wiki
    kadmin = None
    initialized = None
    @staticmethod
    def __init__():
        if not KerberosAdmin.kadmin or not KerberosAdmin.initialized or KerberosAdmin.initialized < datetime.datetime.now() - datetime.timedelta(hours=1):
#             KerberosAdmin.instance = KerberosAdmin()
            print('Initializing kadmin with keytab: '+settings.KRB_KEYTAB)
            principal = "%s@%s"%(settings.KRB_PRINCIPAL,settings.KRB_REALM)
#             @todo: Log every time this happens
            KerberosAdmin.kadmin = kadmin.init_with_keytab(principal, settings.KRB_KEYTAB)
            KerberosAdmin.initialized = datetime.datetime.now()
#         return KerberosAdmin.instance
#     def initialize():
#         if not KerberosAdmin.kadmin:
# #             KerberosAdmin.instance = KerberosAdmin()
#             principal = "%s@%s"%(settings.KRB_PRINCIPAL,settings.KRB_REALM)
#             KerberosAdmin.kadmin = kadmin.init_with_keytab(principal, settings.KRB_KEYTAB)
#         return KerberosAdmin.instance
    def get_kadmin(self):
        return self.kadmin
    @staticmethod
    def fully_qualified_principal(name):
        if '@' in name:
            return name
        else:
            return "%s@%s" % (name,settings.KRB_REALM)
    def add_principal(self,user,password=None):
        principal = "%s@%s" % (user.username,settings.KRB_REALM)
        self.kadmin.addprinc(principal,password)
#         #Log.create(text="Principal '%s' created for '%s'"%(user.username,user),objects=[user])
        princ = self.kadmin.getprinc(principal)
        if princ:
            princ.policy = getattr(settings, 'KRB_DEFAULT_POLICY',None)
            princ.commit()
        return princ
#         #Log.create(text="Policy '%s' set for principal '%s'"%(princ.policy,princ.name),objects=[user])
    def get_user_principal(self,user):
        principal = "%s@%s" % (user.username,settings.KRB_REALM)
        return self.kadmin.getprinc(principal)
    def get_principal(self,name):
        principal = KerberosAdmin.fully_qualified_principal(name)
        return self.kadmin.getprinc(principal)
    def username_exists(self,username):
        principal = "%s@%s" % (username,settings.KRB_REALM)
        return self.kadmin.getprinc(principal) is not None

class Principal(object):
    def __init__(self,principal):
        if isinstance(principal, str):
            self.princ = KerberosAdmin().get_principal(principal)
        else:
            self.princ = principal
        if not self.princ:
            raise Exception("Unable to instantiate principal: %s"%str(principal))
    def is_active(self):
        return (not self.princ.expire or self.princ.expire > datetime.datetime.now())
    def password_expired(self):
        return self.princ.pwexpire and self.princ.pwexpire < datetime.datetime.now()
    def password_expires_in(self):
        return (self.princ.pwexpire - datetime.datetime.now()).days
    def set_password(self,password):
        self.princ.change_password(password)
    def set_expiration(self,date='NOW'):
        if date == 'NOW':
            date = datetime.datetime.now()
        self.princ.expire = date
        self.princ.commit()
#     def serialize(self):
#         from gcportal.api.serializers import PrincipalSerializer
#         return PrincipalSerializer(self.princ).data
