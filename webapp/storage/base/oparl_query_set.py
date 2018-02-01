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

import dateutil
from flask import current_app
from mongoengine import Document, BooleanField, ReferenceField, DateTimeField, StringField, ListField, DecimalField, \
    GeoJsonBaseField
from mongoengine.queryset.queryset import QuerySet
from .oparl_result import OParlResult


class OParlQuerySet(QuerySet):
    def _get_as_pymongo(self, doc):
        doc = super(QuerySet, self)._get_as_pymongo(doc)
        doc = self.oparl_doc_modify(doc, self._document)
        return doc

    def resolve(self, page=False, raw=False, hide_inline=False):
        count = self.count()
        data = []
        args = self._document.get_mongodb_default_pipeline()
        if page != False:
            args.append({ "$limit": page * current_app.config['ITEMS_PER_PAGE'] })
            args.append({ "$skip": (page - 1) * current_app.config['ITEMS_PER_PAGE'] })
        rq = self.aggregate(*args, allowDiskUse=True)
        for item in rq:
            if raw:
                data.append(item)
            else:
                data.append(self.oparl_doc_modify(item, self._document, is_child=False, hide_inline=hide_inline))
        return OParlResult(data, count)

    @classmethod
    def oparl_doc_modify(self, doc, doc_obj, is_child=False, hide_inline=False):
        if hasattr(doc_obj, 'pre_doc_modify'):
            doc_obj.pre_doc_modify(doc)
        # transform id
        doc['id'] = "%s/%s/%s" % (current_app.config['PROJECT_URL'], doc_obj._object_db_name, doc['_id'])
        doc['type'] = doc_obj.type
        if 'body' in doc:
            doc['body_id'] = str(doc['body'])
        # delete all empty fields
        for field in list(doc):
            if doc[field] == None or doc[field] == []:
                del doc[field]
        # delete deleted if false
        if 'deleted' in doc:
            if doc['deleted'] == False:
                del doc['deleted']
        local_time_zone = dateutil.tz.gettz('Europe/Berlin')
        utc_time_zone = dateutil.tz.gettz('UTC')

        for field in doc_obj._fields:
            if field in doc:
                if hasattr(doc_obj._fields[field], 'delete_always'):
                    if doc_obj._fields[field].delete_always:
                        del doc[field]
                        continue
                # process all list of reference fields
                if doc_obj._fields[field].__class__.__name__ == 'ListField':
                    if doc_obj._fields[field].field.__class__.__name__ == 'ReferenceField':
                        if hasattr(doc_obj._fields[field].field, 'delete_inline') and (is_child or hide_inline):
                            if doc_obj._fields[field].field.delete_inline:
                                del doc[field]
                                continue
                        if doc_obj._fields[field].field.internal_output:
                            for i in range(0, len(doc[field])):
                                doc[field][i] = self.oparl_doc_modify(doc[field][i], doc_obj._fields[field].field.document_type, True)
                        else:
                            for i in range(0, len(doc[field])):
                                doc[field][i] = "%s/%s/%s" % (current_app.config['PROJECT_URL'], doc_obj._fields[
                                    field].field.document_type._object_db_name, doc[field][i])
                # process all reference fields
                elif doc_obj._fields[field].__class__.__name__ == 'ReferenceField':
                    if hasattr(doc_obj._fields[field], 'delete_inline') and (is_child or hide_inline):
                        if doc_obj._fields[field].delete_inline:
                            del doc[field]
                            continue
                    if doc_obj._fields[field].internal_output:
                        if is_child:
                            doc[field] = self.oparl_doc_modify(doc[field], doc_obj._fields[field].document_type, True)
                        else:
                            doc[field] = self.oparl_doc_modify(doc[field][0], doc_obj._fields[field].document_type, True)
                    else:
                        doc[field] = "%s/%s/%s" % (
                        current_app.config['PROJECT_URL'], doc_obj._fields[field].document_type._object_db_name,
                        doc[field])
                # process all datetime fields
                elif doc_obj._fields[field].__class__.__name__ == 'DateTimeField':
                    if type(doc[field]) == str:  # SHOULD NEVER HAPPEN!
                        doc[field] = dateutil.parser.parse(doc[field])
                    if doc_obj._fields[field].datetime_format == 'datetime':
                        doc[field] = doc[field].replace(tzinfo=utc_time_zone).astimezone(local_time_zone).isoformat()
                    elif doc_obj._fields[field].datetime_format == 'date':
                        doc[field] = doc[field].replace(tzinfo=utc_time_zone).astimezone(local_time_zone).strftime(
                            '%Y-%m-%d')
                # prefix everything which is vendor specific
                if hasattr(doc_obj._fields[field], 'vendor_attribute'):
                    if doc_obj._fields[field].vendor_attribute:
                        doc['%s:%s' % (current_app.config['VENDOR_PREFIX'], field)] = doc[field]
                        del doc[field]



        """
        for field in doc_obj._fields:
            if field in doc:
                # process all list of reference fields
                if doc_obj._fields[field].__class__.__name__ == 'ListField':
                    if doc_obj._fields[field].field.__class__.__name__ == 'ReferenceField':
                        if hasattr(doc_obj._fields[field].field, 'delete_inline') and (is_child or hide_inline):
                            if doc_obj._fields[field].field.delete_inline:
                                del doc[field]
                                continue
                        if doc_obj._fields[field].field.internal_output:
                            for i in range(0, len(doc[field])):
                                doc[field][i] = self.oparl_doc_modify(doc[field][i], doc_obj._fields[field].field.document_type, True)
                        else:
                            for i in range(0, len(doc[field])):
                                doc[field][i] = "%s/%s/%s" % (current_app.config['PROJECT_URL'], doc_obj._fields[
                                    field].field.document_type._object_db_name, doc[field][i])
                # process all reference fields
                elif doc_obj._fields[field].__class__.__name__ == 'ReferenceField':
                    if hasattr(doc_obj._fields[field], 'delete_inline') and (is_child or hide_inline):
                        if doc_obj._fields[field].delete_inline:
                            del doc[field]
                            continue
                    if doc_obj._fields[field].internal_output:
                        print(doc[field])
                        if len(doc[field]):
                            doc[field] = self.oparl_doc_modify(doc[field][0], doc_obj._fields[field].document_type, True)
                        else:
                            del doc[field]
                    else:
                        doc[field] = "%s/%s/%s" % (
                        current_app.config['PROJECT_URL'], doc_obj._fields[field].document_type._object_db_name,
                        doc[field])
                # process all datetime fields
                elif doc_obj._fields[field].__class__.__name__ == 'DateTimeField':
                    if type(doc[field]) == str:  # SHOULD NEVER HAPPEN!
                        doc[field] = dateutil.parser.parse(doc[field])
                    if doc_obj._fields[field].datetime_format == 'datetime':
                        doc[field] = doc[field].replace(tzinfo=utc_time_zone).astimezone(local_time_zone).isoformat()
                    elif doc_obj._fields[field].datetime_format == 'date':
                        doc[field] = doc[field].replace(tzinfo=utc_time_zone).astimezone(local_time_zone).strftime(
                            '%Y-%m-%d')
                # prefix everything which is vendor specific
                if hasattr(doc_obj._fields[field], 'vendor_attribute'):
                    if doc_obj._fields[field].vendor_attribute:
                        doc['%s:%s' % (current_app.config['VENDOR_PREFIX'], field)] = doc[field]
                        del doc[field]
        """
        # Objektspezifische Weiterverarbeitung (falls vorhanden)
        if hasattr(doc_obj, 'doc_modify'):
            doc_obj.doc_modify(doc)
        del (doc['_id'])
        if 'body_id' in doc:
            del (doc['body_id'])
        return doc
