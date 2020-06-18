from datetime import datetime

from lin.db import MixinJSONSerializer


class Base(MixinJSONSerializer):


    @staticmethod
    def create_time(create_time):
        if create_time:
            return datetime.fromtimestamp(create_time).strftime('%Y-%m-%d')
        else:
            return None