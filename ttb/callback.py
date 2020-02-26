from tensorflow.keras import *
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
import telegram
import requests
import warnings
import os


class TelegramBotCallback(callbacks.Callback):
    def __init__(self, token: str, chat_id=None):
        warnings.filterwarnings("ignore")
        super(TelegramBotCallback, self).__init__()
        # define your bot
        self._bot = telegram.Bot(token=token)
        self._token = token
        self._chat_id = self._get_chat_id() if not chat_id else chat_id
        self._status_list = []
        self._previous_update = None

    def update_current_status(self, status_dict):
        self._status_list.append(status_dict)

    def send_message(self, text: str):
        self._bot.sendMessage(chat_id=self._chat_id, text=text)

    def step(self):
        update = self._bot.getUpdates()[-1]
        if not update == self._previous_update:
            self._previous_update = update
            if "/set " == update.message.text[:5]:
                self._set(update)
            else:
                if not self._status_list:
                    self.send_message("status is not ready. please be patient. and, read the instructions")
                    self._help()
                else:
                    if "/status " == update.message.text[:8]:
                        self._status(update)

                    elif "/plot " == update.message.text[:6]:
                        self._plot(update)
                    else:
                        self.send_message("invalid command usage")
                        self._help()
        else:
            pass

    def _status(self, update):
        args = update.message.text[8:].split(" ")
        if "all" in args:
            self._send_current_status(*list(self._current_status.keys()))
        else:
            if self._is_vaild_arguments(*args):
                self._send_current_status(*args)
            else:
                self._invalid_argument_message(*args)

    def _plot(self, update):
        args = update.message.text[6:].split(" ")
        if "all" in args:
            self._draw_plot(*list(self._current_status.keys()))
            self._send_plot()
        else:
            if self._is_vaild_arguments(*args):
                self._draw_plot(*args)
                self._send_plot()
            else:
                self._invalid_argument_message(*args)

    def _set(self, update):
        args = update.message.text[5:].split(" ")
        if args[0] == "lr":
            self._set_lr(float(args[1]))

    def _invalid_argument_message(self, *args):
        self.send_message(f"invalid argument {reduce(lambda x, y: x + ' ' + y, args)}")
        self._help()

    def _help(self):
        help_text = \
            """
            /help: shows this helpful message :D
            /status:
                usage:
                    /status arg1 arg2 arg3....: prints last value of arg1, arg2, arg3
                    /status all: prints last value of all arguments
            /plot:
                usage:
                    /plot arg1 arg2 arg3....: plots all value of arg1, arg2, arg3 in one figure
                    /plot all: plots all value of all argument in one figure
            if you can't get it, why don't you just try?
            """
        self.send_message(help_text)
        pass

    # gets chat id
    def _get_chat_id(self) -> str:
        updates = self._bot.getUpdates()
        chat_id = updates[-1].message.chat.id
        username = updates[-1].message.chat.username
        text = f"hello, {username}. TensorFlow Telegram Bot is just Started."
        self._bot.sendMessage(chat_id, text)
        return chat_id

    @property
    def _current_status(self):
        return self._status_list[-1]

    def _is_vaild_arguments(self, *args):
        return np.array(list(map(lambda x: x in self._current_status.keys(), args))).all()

    def _send_current_status(self, *args):
        text = reduce(lambda x, y: x + y, map(lambda x: f"{x}:{self._current_status[x]}\n", args))
        self.send_message(text)
        return True

    def _send_plot(self):
        if os.path.exists("./plot.png"):
            url = f"https://api.telegram.org/bot{self._token}/sendPhoto"
            files = {'photo': open('./plot.png', 'rb')}
            data = {'chat_id': self._chat_id}
            requests.post(url, files=files, data=data)
            self.send_message("here's your plot!")

    def _draw_plot(self, *args):
        for arg in args:
            plt.plot(list(map(lambda x: x[arg], self._status_list)), label=arg)
        plt.legend()
        plt.savefig("./plot.png")
        plt.clf()
        self.send_message("drawing plot")
        return True

    def on_train_begin(self, logs=None):
        self.send_message("""Hi, The model is Beginning Training.
                          after this, you can get learning status via using some commands
                          if you want to know more about that, use command /help
                          please enjoy your training""")

    def on_epoch_end(self, epoch, logs=None):
        logs["epoch"] = epoch
        self._status_list.append(logs)
        self.step()

    def on_predict_begin(self, logs=None):
        self.step()

    def on_train_end(self, logs=None):
        for arg in self._status_list[-1].keys():
            self._draw_plot(arg)
            self._send_plot()
        self._send_current_status(*list(self._status_list[-1].keys()))

    def _set_lr(self, value):
        prev_lr = self.model.optimizer.lr.numpy()
        backend.set_value(self.model.optimizer.lr, value)
        self.send_message(f"learning rate has changed \n ({prev_lr}->{self.model.optimizer.lr.numpy()})")
