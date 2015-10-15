# -*- coding: utf-8-*-
import abc


class GenericPlugin(object):
    def __init__(self, info, config):
        self._plugin_config = config
        self._plugin_info = info

    @property
    def profile(self):
        # FIXME: Remove this in favor of something better
        return self._plugin_config

    @property
    def info(self):
        return self._plugin_info


class SpeechHandlerPlugin(GenericPlugin):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        GenericPlugin.__init__(self, *args, **kwargs)

        # Test if language is supported and raise error if not
        self._get_translations()

    def _get_translations(self):
        try:
            language = self.profile['language']
        except KeyError:
            language = 'en-US'

        if language not in self._plugin_info.translations:
            raise ValueError('Unsupported Language!')

        return self._plugin_info.translations[language]

    def gettext(self, *args, **kwargs):
        return self._get_translations().gettext(*args, **kwargs)

    def ngettext(self, *args, **kwargs):
        return self._get_translations().ngettext(*args, **kwargs)

    @abc.abstractmethod
    def get_phrases(self):
        pass

    @abc.abstractmethod
    def handle(text, mic):
        pass

    @abc.abstractmethod
    def is_valid(text):
        pass

    def get_priority(self):
        return 0
