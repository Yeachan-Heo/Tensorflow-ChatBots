from tensorflow_chatbots.variableholder.variableholder import VariableHolder
from tensorflow.keras import *
from slacker import Slacker
from functools import reduce

import matplotlib.pyplot as plt
import subprocess as sp
import numpy as np
import os
import re


class SlackBotCallback(callbacks.Callback):
    def __init__(self, token="", channel="#general"):
        super().__init__()
        self._bot = Slacker(token)
        self._bot.chat.update
        self._channel = channel
        self._status_list = []
        self._variable_holder: VariableHolder or None = None
        self._previous_message = None

    def set_variable_holder(self, vh: VariableHolder):
        self._variable_holder = vh

    def add_status(self, status: dict):
        self._status_list.append(status)

    def step(self):
        message = self._receive_message()
        if not self._is_updaten(message):
            return
        if re.match("/status ", message):
            self._command_status(message)
        elif re.match("/plot ", message):
            self._command_plot(message)
        elif re.match("/set ", message):
            self._command_set(message)
        elif re.match("/get ", message):
            self._command_get(message)
        elif re.match("/bash ", message):
            self._command_bash(message)
        elif re.match("/start", message):
            self._command_start()
        elif re.match("/help", message):
            self._command_help()
        else:
            self._command_invalid(message)

    @property
    def _current_status(self):
        return self._status_list[-1]

    def _is_updaten(self, message):
        updaten = False \
            if message == self._previous_message \
            else True
        self._previous_message = message
        return updaten

    def _receive_message(self) -> str:
        return self._bot.conversations.history(channel=self._channel)[-1]["text"]

    def _send_message(self, **attachments) -> None:
        self._bot.chat.post_message(channel=self._channel, text=None, attachments=[attachments], as_user=True)

    def _send_invalid_argument_message(self, arguments):
        text = self._generate_invalid_argument_text(arguments)
        title = self._generate_invalid_argument_title()
        self._send_message(text=text, title=title)

    def _send_variable_changed_message(self, variable_name, prev_value, current_value):
        text = self._generate_variable_changed_text(prev_value, current_value)
        title = self._generate_variable_changed_title(variable_name)
        self._send_message(text=text, title=title)

    def _send_file(self, file_path=None, **kwargs):
        # chaneels, file, title, filetype
        # reference: https://talkingaboutme.tistory.com/entry/TIP-message-sending-file-uploading-with-slackclient
        self._bot.files.upload(channels=self._channel, file=file_path)

    def _generate_invalid_argument_text(self, arguments):
        invalid_argument_text = f"{reduce(lambda x, y: x + ' ' + y, arguments)}"
        return invalid_argument_text

    def _generate_variable_changed_text(self, prev_value, current_value):
        variable_changed_text = f"({round(prev_value, 4)}->{round(current_value, 4)})"
        return variable_changed_text

    def _generate_invalid_argument_title(self):
        invalid_argument_title = f"Invalid Arguments Occured"
        return invalid_argument_title

    def _generate_variable_changed_title(self, variable_name):
        variable_changed_title = f"{variable_name} has changed"
        return variable_changed_title

    def _is_valid_arguments(self, arguments):
        return np.array(list(map(lambda x: x in self._current_status.keys(), arguments))).all()

    def _command_status(self, message):
        if re.match("/status all", message):
            arguments = list(self._current_status.keys())
        else:
            arguments = message[re.match("/status ", message).end():].split(" ")
        self._send_status_message(arguments) \
            if self._is_valid_arguments(arguments) \
            else self._send_invalid_argument_message(arguments)

    def _send_status_message(self, arguments):
        text = self._generate_status_text(arguments)
        title = self._generate_status_title(arguments)
        self._send_message(text=text, title=title)

    def _generate_status_text(self, arguments):
        status_string = reduce(lambda x, y: x + y, map(lambda x: f"{x}:{self._current_status[x]}\n", arguments))
        return status_string

    def _generate_status_title(self, arguments):
        status_title = "Status All" \
            if arguments == list(self._current_status.keys()) \
            else f"Status About {reduce(lambda x, y: x + ' ' + y, arguments)}"
        return status_title

    def _command_plot(self, message):
        arguments = list(self._current_status.keys()) \
            if re.match("/plot all", message) \
            else message[re.match("/plot ", message).end():].split(" ")
        title = self._generate_plot_title(arguments)
        self._draw_and_send_plot(data_list=self._get_plot_datas(arguments), labels=arguments, title=title) \
            if self._is_valid_arguments(arguments) \
            else self._send_invalid_argument_message(arguments)

    def _send_plot(self, title):
        self._send_file(file_="plot.png", filetype="image", title=title)

    def _generate_plot_title(self, arguments):
        plot_title = "All Plots" \
            if arguments == list(self._current_status) \
            else f"Plots About {reduce(lambda x, y: x + ' ' + y, arguments)}"
        return plot_title

    def _draw_and_save_plot(self, data_list, labels):
        for data, label in zip(data_list, labels):
            plt.plot(data, label=label)
        plt.legend()
        plt.savefig("plot.png")
        plt.clf()

    def _draw_and_send_plot(self, data_list, labels, title):
        self._draw_and_save_plot(data_list, labels)
        self._send_plot(title)

    def _get_plot_datas(self, arguments):
        return list(map(lambda x: list(map(lambda y: y[x], self._status_list)), arguments))

    def _command_set(self, message):
        arguments = message[re.match("/set ", message).end():].split(" ")
        if len(arguments) is not 2:
            self._send_message(text="Invalid message. use /help to see description")
        elif arguments[0] == "lr":
            self._set_lr(float(arguments[1]))
        else:
            self._set_variable(variable_name=arguments[0], value=float(arguments[1]))

    def _set_lr(self, value):
        prev_lr = self.model.optimizer.lr.numpy()
        backend.set_value(self.model.optimizer.lr, value)
        self._send_variable_changed_message("learning rate", prev_lr, value)

    def _set_variable(self, variable_name, value):
        success, prev_value = self._variable_holder.set_value(variable_name, value)
        if not success:
            self._send_invalid_argument_message([variable_name])
            return
        self._send_variable_changed_message(variable_name, prev_value, value)

    def _command_start(self):
        self._send_start_message()

    def _send_start_message(self):
        text = self._generate_start_text()
        title = self._generate_start_title()
        self._send_message(text=text, title=title)

    def _generate_start_text(self):
        start_text = "Welcome To TensorFlow Slack Bot! type /help to know about commands!"
        return start_text

    def _generate_start_title(self):
        start_title = "Greetings!"
        return start_title

    def _command_help(self):
        self._send_help_message()

    def _send_help_message(self):
        text = self._generate_help_text()
        title = self._generate_help_title()
        self._send_message(text=text, title=title)

    def _generate_help_text(self):
        help_text = """
        /help: shows this helpful message :D
        /status:
            usage:
                /status arg1 arg2 arg3....: prints last value of arg1, arg2, arg3
                /status all: prints last value of all arguments
        /plot:
            usage:
                /plot arg1 arg2 arg3....: plots all value of arg1, arg2, arg3 in one figure
                /plot all: plots all value of all argument in one figure
        /set:
            usage:
                /set lr <value>: sets learning rate
                /set <variable_name> <value>: sets variable in the variable holder
        /get:
            usage:
                /get <filepath>: sends file
        /bash:
            usage:
                /bash <bash commands>: executes bash command and send output
        if you can't get it, why don't you just try?
        """
        return help_text

    def _generate_help_title(self):
        help_message_title = "Help Message"
        return help_message_title

    def _command_invalid(self, message):
        self._send_invalid_message(message)

    def _send_invalid_message(self, message):
        text = self._generate_invalid_text(message)
        title = self._generate_invalid_title()
        self._send_message(text=text, title=title)

    def _generate_invalid_text(self, message):
        invalid_text = f"command usage {message} is invalid. use command /help to see help message"
        return invalid_text

    def _generate_invalid_title(self):
        invalid_title = "Invalid Command Usage"
        return invalid_title

    def _command_get(self, message):
        arguments = message[re.match("/get ", message).end():].split(" ")
        for file_path in arguments:
            self._send_file(file_path) \
                if os.path.exists(file_path) \
                else self._send_invalid_file_message(file_path)

    def _send_invalid_file_message(self, file_path):
        text = self._generate_invalid_file_text(file_path)
        title = self._generate_invalid_file_title()
        self._send_message(text=text, title=title)

    def _generate_invalid_file_text(self, file_path):
        invalid_file_text = f"{file_path} doesn't exists"
        return invalid_file_text

    def _generate_invalid_file_title(self):
        invalid_file_title = "Invalid File"
        return invalid_file_title

    def _command_bash(self, message):
        command = message[re.match("/bash ", message).end():]
        self._send_bash_message(command)

    def _send_bash_message(self, command):
        text = self._generate_bash_text(command)
        title = self._generate_bash_title(command)
        self._send_message(text=text, title=title)

    def _generate_bash_text(self, command):
        try:
            bash_text = sp.check_output(command, shell=True).decode("cp949")
        except Exception as e:
            bash_text = str(e)
        return bash_text

    def _generate_bash_title(self, command):
        bash_title = f"Executed command {command}"
        return bash_title

    def on_train_begin(self, logs=None):
        self._command_start()

    def on_predict_begin(self, logs=None):
        self.step()

    def on_epoch_end(self, epoch, logs=None):
        logs["epoch"] = epoch
        self.add_status(logs)
        self.step()

    def on_train_end(self, logs=None):
        for x in list(self._current_status.keys()):
            self._command_plot(message=f"/plot {x}")
        self._command_status(message="/status all")
