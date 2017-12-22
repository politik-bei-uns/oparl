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

from .file import File
from mongoengine import Document, BooleanField, ReferenceField, DateTimeField, StringField, ListField, DecimalField, \
    GeoJsonBaseField
from .base.oparl_document import OParlDocument
from bson.objectid import ObjectId


class AgendaItem(Document, OParlDocument):
    type = 'https://schema.oparl.org/1.0/AgendaItem'
    body = ReferenceField('Body', dbref=False, internal_output=False, delete_inline=True)
    meeting = ReferenceField('Meeting', dbref=False, internal_output=False, delete_inline=True)
    number = StringField()
    name = StringField()
    public = BooleanField()
    consultation = ReferenceField('Consultation', dbref=False, internal_output=False)
    result = StringField()
    resolutionText = StringField()
    resolutionFile = ReferenceField('File', dbref=False, internal_output=True)
    auxiliaryFile = ListField(ReferenceField('File', dbref=False, internal_output=True), default=[])
    start = DateTimeField(datetime_format='datetime')
    end = DateTimeField(datetime_format='datetime')
    license = StringField()
    keyword = ListField(StringField(), default=[])
    created = DateTimeField(datetime_format='datetime')
    modified = DateTimeField(datetime_format='datetime')
    web = StringField()

    # Politik bei Uns Felder
    originalId = StringField(vendor_attribute=True)
    mirrorId = StringField(vendor_attribute=True)

    # Felder zur Verarbeitung
    _object_db_name = 'agenda_item'
    _attribute = 'agendaItem'

    @classmethod
    def pre_doc_modify(self, doc):
        # ugly bugfix for missing double join
        if 'resolutionFile' in doc:
            if type(doc['resolutionFile']) == ObjectId:
                doc['resolutionFile'] = File.objects(pk=str(doc['resolutionFile'])).resolve(raw=True).first()
        if 'auxiliaryFile' in doc:
            for i in range(0, len(doc['auxiliaryFile'])):
                if type(doc['auxiliaryFile']) == ObjectId:
                    doc['auxiliaryFile'][i] = File.objects(pk=str(doc['resolutionFile'][i])).resolve(raw=True).first()
        return doc

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<AgendaItem %r>' % self.name
