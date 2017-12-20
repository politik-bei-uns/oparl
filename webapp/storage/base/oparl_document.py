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

from mongoengine import Document, BooleanField, ReferenceField, DateTimeField, StringField, ListField, DecimalField, \
    GeoJsonBaseField
from .oparl_query_set import OParlQuerySet


class OParlDocument(object):
    meta = {'queryset_class': OParlQuerySet}

    @classmethod
    def get_mongodb_default_pipeline(cls):
        pipeline = []
        pipeline_group = {
            "_id": "$_id"
        }
        for field in cls._fields:
            if cls._fields[field].__class__.__name__ == 'ListField':
                if cls._fields[field].field.__class__.__name__ == 'ReferenceField':
                    if cls._fields[field].field.internal_output:
                        pipeline.append({
                            "$unwind": {
                                "path": "$" + field,
                                "preserveNullAndEmptyArrays": True
                            }
                        })
                        pipeline.append({
                            "$lookup": {
                                "from": cls._fields[field].field.document_type._object_db_name,
                                "localField": field,
                                "foreignField": "_id",
                                "as": field
                            }
                        })
                        pipeline.append({
                            "$unwind": {
                                "path": "$" + field,
                                "preserveNullAndEmptyArrays": True
                            }
                        })
                        pipeline_group[field] = {
                            "$addToSet": "$" + field
                        }
            elif cls._fields[field].__class__.__name__ == 'ReferenceField':
                if cls._fields[field].internal_output:
                    pipeline.append({
                        "$lookup": {
                            "from": cls._fields[field].document_type._object_db_name,
                            "localField": field,
                            "foreignField": "_id",
                            "as": field
                        }
                    })
                    pipeline.append({
                        "$unwind": {
                            "path": "$" + field,
                            "preserveNullAndEmptyArrays": True
                        }
                    })
                    pipeline_group[field] = {
                        "$first": "$" + field
                    }
        pipeline.append({
            '$group': pipeline_group
        })
        for field_name, field in cls._fields.items():
            output_field = True
            if isinstance(field, ReferenceField):
                if field.internal_output:
                    output_field = False
            elif isinstance(field, ListField):
                if isinstance(field.field, ReferenceField):
                    if hasattr(field, 'external_list'):
                        if field.external_list:
                            output_field = False
                    if field.field.internal_output:
                        output_field = False
            if output_field:
                pipeline[-1]['$group'][field_name] = {
                    "$first": "$" + field_name
                }
        return pipeline

    """
    @classmethod
    def get_mongodb_default_pipeline(cls):
      pipeline = []
      pipeline_group = {
        "_id": "$_id"
      }
      for field in cls._do_deref_field:
        if cls._fields[field].__class__.__name__ == 'ReferenceField':
          pipeline.append({
            "$lookup": {
              "from": cls._fields[field].document_type._object_db_name,
              "localField": field,
              "foreignField": "_id",
              "as": field
            }
          })
          pipeline.append({
            "$unwind": {
              "path": "$" + field,
              "preserveNullAndEmptyArrays": True
            }
          })
          pipeline_group[field] = {
            "$first": "$" + field
          }
        elif cls._fields[field].__class__.__name__ == 'ListField':
          pipeline.append({
            "$unwind": {
              "path": "$" + field,
              "preserveNullAndEmptyArrays": True
            }
          })
          pipeline.append({
            "$lookup": {
              "from": cls._fields[field].field.document_type._object_db_name,
              "localField": field,
              "foreignField": "_id",
              "as": field
            }
          })
          pipeline.append({
            "$unwind": {
              "path": "$" + field,
              "preserveNullAndEmptyArrays": True
            }
          })
          pipeline_group[field] = {
            "$addToSet": "$" + field
          }
      pipeline.append({
        '$group': pipeline_group
      })
      for field_name, field in cls._fields.items():
        if not (isinstance(field, ReferenceField) or isinstance(field, ListField) or field_name == '_id'):
          pipeline[-1]['$group'][field_name] = {
            "$first": "$" + field_name
          }
      return pipeline
    """
