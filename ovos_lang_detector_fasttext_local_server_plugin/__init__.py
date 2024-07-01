from ovos_plugin_manager.templates.language import LanguageDetector
from ovos_config.config import Configuration
from langcodes import standardize_tag
import requests


class FastTextLangServerDetectPlugin(LanguageDetector):
    """
    language detector that uses several other plugins and
    averages their predictions
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = Configuration().get(
            "FastTextLangServerDetectPlugin", {}).get(
                "url",
                "http://10.0.1.44:8000"
                )

    def detect(self, text):
        try:
            resp = requests.get(f"{self.url}/language_detect?text={text}")
            return standardize_tag(resp.json()[0][0])
        except requests.exceptions.RequestException as e:
            self.log.error("TTS Lang detect error: %s", e)
            return ""
        except KeyError as e:
            self.log.error(
                "%s\nTTS missing lang in reply: %s",
                (e, resp.json())
                )
            return False


if __name__ == "__main__":
    clf = FastTextLangServerDetectPlugin()
    print(clf.detect("olá mundo"))
