from abc import ABC, abstractmethod
from telegram.ext import CommandHandler


class Commander(object):

    def __init__(self, dispatcher):
        self.__dispatcher = dispatcher
        self.__list = list()
        self.__dispatcher.add_handler(CommandHandler('help', self.__print_help))

    def add_cmd(self, command):
        if not isinstance(command, Command):
            raise TypeError('Command must be command')
        self.__list.append(command)
        self.__dispatcher.add_handler(CommandHandler(command.cmd(), command.do))

    def __print_help(self, bot, update):
        update.message.reply_text('\n'.join(['/{} - {}'.format(cmd.cmd(), cmd.help()) for cmd in self.__list]))


class Command(ABC):

    @abstractmethod
    def cmd(self):
        pass

    @abstractmethod
    def help(self):
        pass

    @abstractmethod
    def do(self, bot, update):
        pass


class UserID(Command):

    def cmd(self):
        return 'user_id'

    def help(self):
        return 'Returns your user ID'

    def do(self, bot, update):
        update.message.reply_text('Your user id is {}'.format(update.effective_user.id))


class UserName(Command):

    def cmd(self):
        return 'user_name'

    def help(self):
        return 'Returns your user name'

    def do(self, bot, update):
        update.message.reply_text('Your user name is {}'.format(update.effective_user.username))


class PiUpdate(Command):

    def cmd(self):
        return 'pi_update'

    def help(self):
        return 'Update raspberry pi'

    def do(self, bot, update):
        update.message.reply_text()
