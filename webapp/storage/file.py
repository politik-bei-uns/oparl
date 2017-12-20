# encoding: utf-8

"""
Copyright (c) 2012 - 2016, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from flask import current_app
from mongoengine import Document, BooleanField, ReferenceField, DateTimeField, StringField, ListField, DecimalField, \
    GeoJsonBaseField, IntField, DictField
from .base.oparl_document import OParlDocument


class File(Document, OParlDocument):
    meta = {
        'indexes': [
            {
                'fields': ['$name', "$text", 'body'],
                'default_language': 'english',
                'weights': {'name': 10, 'text': 2}
            }
        ]
    }

    type = 'https://schema.oparl.org/1.0/File'
    body = ReferenceField('Body', dbref=False, internal_output=False)
    name = StringField()
    fileName = StringField()
    mimeType = StringField()
    date = DateTimeField(datetime_format='date')
    size = DecimalField()
    sha1Checksum = StringField()
    text = StringField()
    accessUrl = StringField()
    downloadUrl = StringField()
    externalServiceUrl = StringField()
    masterFile = ReferenceField('File', dbref=False, internal_output=False)
    derivativeFile = ListField(ReferenceField('File', dbref=False, internal_output=False), default=[])
    fileLicense = StringField()
    meeting = ListField(ReferenceField('Meeting', dbref=False, internal_output=False, delete_inline=True), default=[])
    agendaItem = ListField(ReferenceField('AgendaItem', dbref=False, internal_output=False, delete_inline=True), default=[])
    paper = ListField(ReferenceField('Paper', dbref=False, internal_output=False, delete_inline=True), default=[])
    license = StringField()
    keyword = ListField(StringField(), default=[])
    created = DateTimeField(datetime_format='datetime')
    modified = DateTimeField(datetime_format='datetime')
    web = StringField()
    deleted = BooleanField()

    # Politik bei Uns Felder
    originalId = StringField(vendor_attribute=True)
    originalWeb = StringField(vendor_attribute=True)
    originalAccessUrl = StringField(vendor_attribute=True)
    originalDownloadUrl = StringField(vendor_attribute=True)
    textGenerated = DateTimeField(datetime_format='datetime', vendor_attribute=True)
    textStatus = StringField(vendor_attribute=True)
    thumbnailGenerated = DateTimeField(datetime_format='datetime', vendor_attribute=True)
    thumbnailStatus = StringField(vendor_attribute=True)
    georeferencesGenerated = DateTimeField(datetime_format='datetime', vendor_attribute=True)
    georeferencesStatus = StringField(vendor_attribute=True)
    thumbnail = DictField(vendor_attribute=True)
    pages = IntField(vendor_attribute=True)

    # Felder zur Verarbeitung
    _object_db_name = 'file'
    _attribute = 'file'

    # Verarbeitet Einzelergebnis vor Ausgabe
    def to_mongo(self):
        doc = super(Document, self).to_mongo()
        # doc = oparl_doc_modify(doc, self)
        return doc

    @classmethod
    def doc_modify(self, doc):
        if 'body_id' in doc:
            doc['accessUrl'] = '%s/%s/%s/view' % (current_app.config['PROJECT_CDN_URL'], doc['body_id'], doc['_id'])
            doc['downloadUrl'] = '%s/%s/%s/download' % (
            current_app.config['PROJECT_CDN_URL'], doc['body_id'], doc['_id'])
        return doc

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<File %r>' % self.name
