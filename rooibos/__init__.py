import logging
import os, sys
from django.conf import settings
import config.settings_local

if settings.DEBUG:
    log = logging.getLogger('rooibos')

    log.info('\n\n\n\n====== MDID Startup ===============================================================================')
    log.info('Important Directories')
    log.info('MDID3 root:     %s', settings.PROJECT_ROOT)
    log.info('config dir:     %s', os.path.dirname(config.settings_local.__file__))
    log.info('rooibos dir:    %s', settings.ROOIBOS_ROOT)
    log.info('media root:     %s', settings.MEDIA_ROOT)
    log.info('static files:   %s', settings.STATIC_ROOT)
    log.info('scratch dir:    %s', settings.SCRATCH_DIR)
    log.info('auto-storage:   %s', settings.AUTO_STORAGE_DIR)
    try:
        log.info('log file:       %s', settings.LOGGING['handlers']['rooibos']['filename'])
    except Exception as e:
        try:
            log.info('log file:       %s', settings.LOGGING['handlers']['file']['filename'])
        except Exception as e:
            log.exception('log setup is not LOGGING[\'handlers\'][\'file\'][\'filename\']')
            pass
        pass

    log.info('====end startup messages======================================================\n')
