from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

# Create your models here.
USER_MODEL = settings.AUTH_USER_MODEL


# Customize User model
class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """

    username = models.CharField(_('username'), max_length=100, unique=True,
                                help_text=_('TÉ™lÉ™b olunur. 75 simvol vÉ™ ya az. HÉ™rflÉ™r, RÉ™qÉ™mlÉ™r vÉ™ '
                                            '@/./+/-/_ simvollar.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$',
                                                              _('DÃ¼zgÃ¼n istifadÉ™Ã§i adÄ± daxil edin.'),
                                                              'yanlÄ±ÅŸdÄ±r')
                                ])
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), max_length=255)

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    """
        Important non-field stuff
    """
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'

    def get_full_name(self):
        """
            Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
            Returns the short name for the user.
        """
        return self.first_name


class Alphabed(models.Model):
    title = models.CharField(max_length=255, default="Elifba")
    letters = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s" % self.title

    def get_alphabet_letters(self):
        return self.title


class DecodeHelper(models.Model):
    encode = models.TextField(null=True, blank=True)
    token = models.TextField(null=True, blank=True)
    hidden_token = models.TextField(null=True, blank=True)