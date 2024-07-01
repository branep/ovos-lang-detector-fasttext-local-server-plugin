from ovos_plugin_manager.templates.language import LanguageDetector
import requests


class FastTextLangServerDetectPlugin(LanguageDetector):
    """
    language detector that uses several other plugins and
    averages their predictions
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def detect(self, text):
        url = self.settings.get(
            "language_detect_fqdn",
            "http://10.0.1.44:8000"
            )
        try:
            resp = requests.get(f"{url}/language_detect?text={text}")
            return resp.json()[0][0]
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
