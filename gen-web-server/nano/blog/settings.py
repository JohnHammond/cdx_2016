from django.conf import settings

# Optional support for django-tagging
TAGGING = None
try:
    if 'tagging' in settings.INSTALLED_APPS:
        import tagging as TAGGING
except ImportError:
    TAGGING = False

# Optional support for django-taggit
TAGGIT = None
try:
    if 'taggit' in settings.INSTALLED_APPS:
        import taggit as TAGGIT
except ImportError:
    TAGGIT = False

if TAGGIT:
    NANO_BLOG_TAGS = TAGGIT
elif TAGGING:
    NANO_BLOG_TAGS = TAGGING
else:
    NANO_BLOG_TAGS = None

# Explicit is better than implicit
if not getattr(settings, 'NANO_BLOG_USE_TAGS', False):
    NANO_BLOG_TAGS = False

NANO_BLOG_SPECIAL_TAGS = getattr(settings, 'NANO_BLOG_SPECIAL_TAGS', ('pinned',))
