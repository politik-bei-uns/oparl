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

import math
from flask import current_app


class OParlResult(object):
    def __init__(self, data=None, count=None):
        self._data = data
        self._count = count

    def first(self):
        if self._data == None:
            return None
        if len(self._data) == 0:
            return None
        return self._data[0]

    def all(self):
        if self._data == None:
            return None
        if len(self._data) == 0:
            return None
        return self._data

    def page(self, base_url='', page=1, fastsync=0):
        total_pages = math.ceil(self._count / current_app.config['ITEMS_PER_PAGE'])
        result = {
            'data': self._data,
            'pagination': {
                "totalElements": self._count,
                "elementsPerPage": current_app.config['ITEMS_PER_PAGE'],
                "currentPage": page,
                "totalPages": total_pages
            },
            'links': {
                "first": base_url,
                "self": base_url + ('?page=' + str(page) if page > 1 else ''),
                "last": base_url + ('?page=' + str(total_pages) if total_pages > 1 else '')
            }
        }
        if page != 1:
            result['links']['prev'] = base_url + ('?page=' + str(page - 1) if page - 1 > 1 else '')
        if page != total_pages and total_pages != 0:
            result['links']['next'] = base_url + '?page=' + str(page + 1)
        return result
