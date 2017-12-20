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
    GeoJsonBaseField
from .base.oparl_document import OParlDocument


class Body(Document, OParlDocument):
    type = 'https://schema.oparl.org/1.0/Body'
    shortName = StringField()
    name = StringField()
    website = StringField()
    license = StringField()
    licenseValidSince = DateTimeField(datetime_format='date')
    oparlSince = DateTimeField(datetime_format='date')
    ags = StringField()
    rgs = StringField()
    equivalent = ListField(StringField(), default=[])
    contactEmail = StringField()
    contactName = StringField()
    legislativeTerm = ListField(ReferenceField('LegislativeTerm', dbref=False, internal_output=True), default=[])
    classification = StringField()
    location = ReferenceField('Location', dbref=False, internal_output=True)
    keyword = ListField(StringField(), default=[])
    created = DateTimeField(datetime_format='datetime')
    modified = DateTimeField(datetime_format='datetime')
    web = StringField()
    deleted = BooleanField()

    # Politik bei Uns Felder
    originalId = StringField(vendor_attribute=True)
    lastSync = DateTimeField(datetime_format='datetime', vendor_attribute=True)
    storageId = StringField(vendor_attribute=True)

    # Felder zur Verarbeitung
    _object_db_name = 'body'
    _attribute = 'body'

    @classmethod
    def doc_modify(self, doc):
        doc['legislativeTerm'] = "%s/body/%s/legislative_term" % (current_app.config['PROJECT_URL'], doc['_id'])
        doc['organization'] = "%s/body/%s/organization" % (current_app.config['PROJECT_URL'], doc['_id'])
        doc['membership'] = "%s/body/%s/membership" % (current_app.config['PROJECT_URL'], doc['_id'])
        doc['person'] = "%s/body/%s/person" % (current_app.config['PROJECT_URL'], doc['_id'])
        doc['meeting'] = "%s/body/%s/meeting" % (current_app.config['PROJECT_URL'], doc['_id'])
        doc['agendaItem'] = "%s/body/%s/agenda_item" % (current_app.config['PROJECT_URL'], doc['_id'])
        doc['paper'] = "%s/body/%s/paper" % (current_app.config['PROJECT_URL'], doc['_id'])
        doc['consultation'] = "%s/body/%s/consultation" % (current_app.config['PROJECT_URL'], doc['_id'])
        doc['location'] = "%s/body/%s/location" % (current_app.config['PROJECT_URL'], doc['_id'])
        doc['file'] = "%s/body/%s/file" % (current_app.config['PROJECT_URL'], doc['_id'])
        return doc

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Body %r>' % self.name
