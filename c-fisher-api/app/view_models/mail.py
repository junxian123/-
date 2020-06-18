from app.view_models.base import Base


class MailViewModel(Base):
    _fields = ['nickname', 'phone', 'address']

    def __init__(self, mail):
        self.nickname = mail.nickname
        self.phone = mail.phone
        self.address = mail.province + mail.city + mail.address