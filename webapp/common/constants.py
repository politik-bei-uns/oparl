# encoding: utf-8

"""
Copyright (c) 2017, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os


class BaseConfig:
    INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

    PROJECT_NAME = "politik-bei-uns-oparl"
    PROJECT_VERSION = '2.1.0'

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    LOG_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir, 'logs'))

    DEBUG = False
    TESTING = False
    S3_DEBUG = False

    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True

    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_DB = 'oparl'

    OPARL_NAME = ''
    OPARL_CONTACT_NAME = ''
    OPARL_CONTACT_EMAIL = ''
    OPARL_WEBSITE = ''
    OPARL_VENDOR = ''
    OPARL_PRODUCT = ''
    OPARL_CREATED = ''
    OPARL_MODIFIED = ''

    ITEMS_PER_PAGE = 100
    VENDOR_PREFIX = 'oparl'
