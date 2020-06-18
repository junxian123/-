from enum import Enum


class PendingStatus(Enum):
    Waiting = 1
    Reject = 2
    Cancel = 3
    Success = 4

    @classmethod
    def pending_str(cls, status, who):
        key_map = {
            cls.Waiting: {
                'requester': '等待对方邮寄',
                'gifter': '等待您邮寄'
            },
            cls.Reject: {
                'requester': '对方已拒绝',
                'gifter': '您已拒绝'
            },
            cls.Cancel: {
                'requester': '您已撤消',
                'gifter': '对方已撤消'
            },
            cls.Success: {
                'requester': '对方已邮寄，交易完成',
                'gifter': '您已邮寄，交易完成'
            }
        }
        return key_map[status][who]