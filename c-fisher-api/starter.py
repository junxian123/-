"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from app.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
