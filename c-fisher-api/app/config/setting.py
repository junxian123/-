"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from datetime import timedelta
import random
# 分页配置
COUNT_DEFAULT = 10
PAGE_DEFAULT = 0

# 令牌配置
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

# 屏蔽 sql alchemy 的 FSADeprecationWarning
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 插件模块暂时没有开启，以下配置可忽略
# plugin config写在字典里面
PLUGIN_PATH = {
    'poem': {'path': 'app.plugins.poem', 'enable': True, 'version': '0.0.1', 'limit': 20},
    'oss': {'path': 'app.plugins.oss', 'enable': True, 'version': '0.0.1', 'access_key_id': 'not complete', 'access_key_secret': 'not complete', 'endpoint': 'http://oss-cn-shenzhen.aliyuncs.com', 'bucket_name': 'not complete', 'upload_folder': 'app', 'allowed_extensions': ['jpg', 'gif', 'png', 'bmp']}
}

# 鱼豆
BEAN_NUMBER = 0.5

# token 过期
EXPIRATION = 3600

# 分页
PRE_PAGE_COUNT = 8
