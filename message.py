import telegram.message


class Message(telegram.message.Message):
    def save_message_local(self):
        """
        save this message to local storage
        :return:
        """
    @classmethod
    def from_message(cls,msg:telegram.message.Message):
        pass