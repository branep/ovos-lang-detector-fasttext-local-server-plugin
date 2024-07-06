from ovos_plugin_manager.templates.language import LanguageDetector
from langcodes import standardize_tag
import requests


class FastTextLangServerDetectPlugin(LanguageDetector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = self.config.get(
            "url",
            "http://10.0.1.44:8000"
        )

    def detect(self, text):
        try:
            resp = requests.get(f"{self.url}/language_detect?text={text}")
            return standardize_tag(resp.json()[0][0])
        except requests.exceptions.RequestException as e:
            self.log.error("Lang detect error: %s", e)
            return ""
        except KeyError as e:
            self.log.error(
                "%s\nMissing lang in reply: %s",
                (e, resp.json())
                )
            return False


if __name__ == "__main__":
    clf = FastTextLangServerDetectPlugin()
    print(clf.detect("olá mundo"))
