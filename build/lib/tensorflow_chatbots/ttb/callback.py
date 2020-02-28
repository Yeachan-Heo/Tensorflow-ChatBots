from tensorflow_chatbots.tsb.callback import SlackBotCallback
import telegram
import requests
import warnings
import os


class TelegramBotCallback(SlackBotCallback):
    def __init__(self, token: str, chat_id=None):
        warnings.filterwarnings("ignore")
        super().__init__(None, None)
        # define your bot
        self._bot = telegram.Bot(token=token)
        self._token = token
        self._chat_id = self._get_chat_id() if not chat_id else chat_id

    def _send_message(self, **kwargs):
        self._bot.sendMessage(chat_id=self._chat_id, text=kwargs["title"] + "\n" + kwargs["text"])

    def _receive_message(self):
        updates = self._bot.getUpdates()
        if not updates:
            return None
        return updates[-1].message.text

    # gets chat id
    def _get_chat_id(self) -> str:
        updates = self._bot.getUpdates()
        chat_id = updates[-1].message.chat.id
        return chat_id

    def _send_plot(self, title):
        if os.path.exists("./plot.png"):
            url = f"https://api.telegram.org/bot{self._token}/sendPhoto"
            files = {'photo': open('plot.png', 'rb')}
            data = {'chat_id': self._chat_id}
            requests.post(url, files=files, data=data)

    def _send_file(self, file_path=None, **kwargs):
        url = f"https://api.telegram.org/bot{self._token}/sendDocument"
        try:
            files = {'document': open(file_path, 'rb')}
        except:
            files = None
            pass
        data = {'chat_id': self._chat_id}
        requests.post(url, files=files, data=data)
