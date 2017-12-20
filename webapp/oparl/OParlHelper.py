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

import dateutil.parser
import urllib.parse
from flask import current_app, request


def generate_filter_kwargs(body_id=None, additional_limits=None):
    created_since = request.args.get('created_since', default=None)
    created_until = request.args.get('created_until', default=None)
    modified_since = request.args.get('modified_since', default=None)
    modified_until = request.args.get('modified_until', default=None)
    kwargs = {}
    if body_id:
        kwargs['body'] = body_id
    if additional_limits != None:
        kwargs.update(additional_limits)
    if created_since:
        created_since = urllib.parse.unquote(created_since)
        kwargs['created__gte'] = dateutil.parser.parse(created_since)
    if created_until:
        created_until = urllib.parse.unquote(created_until)
        kwargs['created__lte'] = dateutil.parser.parse(created_until)
    if modified_since:
        modified_since = urllib.parse.unquote(modified_since)
        kwargs['modified__gte'] = dateutil.parser.parse(modified_since)
    if modified_until:
        modified_until = urllib.parse.unquote(modified_until)
        kwargs['modified__gte'] = dateutil.parser.parse(modified_until)
    return kwargs
