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

import urllib
from flask import (Blueprint, current_app, request, redirect, abort)
from ..common.response import make_oparl_response
from ..models import *
from .OParlHelper import generate_filter_kwargs

oparl = Blueprint('oparl', __name__)


@oparl.route('/')
def root_redirect():
    return redirect('/system')


@oparl.route('/system')
def oparl_system():
    data = {
        "id": "%s/system" % (current_app.config['PROJECT_URL']),
        "type": "https://schema.oparl.org/1.0/System",
        "oparlVersion": "https://schema.oparl.org/1.0/",
        "body": "%s/bodies" % (current_app.config['PROJECT_URL']),
        "name": current_app.config['OPARL_NAME'],
        "contactEmail": current_app.config['OPARL_CONTACT_EMAIL'],
        "contactName": current_app.config['OPARL_CONTACT_NAME'],
        "website": current_app.config['OPARL_WEBSITE'],
        "vendor": current_app.config['OPARL_VENDOR'],
        "product": current_app.config['OPARL_PRODUCT'],
        "created": current_app.config['OPARL_CREATED'],
        "modified": current_app.config['OPARL_MODIFIED'],
    }
    return make_oparl_response(data)


@oparl.route('/bodies')
def oparl_bodies():
    page = request.args.get('page', type=int, default=1)
    result = Body.objects(**generate_filter_kwargs())\
        .order_by('-modified')\
        .resolve(page)\
        .page(base_url='%s/bodies' % (current_app.config['PROJECT_URL']),page=page)
    return make_oparl_response(result)

@oparl.route('/body-by-id')
def oparl_body_id():
    original_id = urllib.parse.unquote_plus(request.args.get('id', None))
    if not original_id:
        abort(404)
    data = Body.objects(originalId=original_id).resolve().first()
    return make_oparl_response(data)

@oparl.route('/body/<string:id>')
def oparl_body(id):
    data = Body.objects(pk=id).resolve().first()
    return make_oparl_response(data)

@oparl.route('/body/<string:body_id>/legislative_term')
def oparl_body_legislative_term(body_id):
    page = request.args.get('page', type=int, default=1)
    fastsync = request.args.get('fastsync', type=int, default=0)
    result = LegislativeTerm.objects(**generate_filter_kwargs(body_id))\
        .order_by('-modified')\
        .resolve(page)\
        .page(base_url='%s/body/%s/legislative_term' % (current_app.config['PROJECT_URL'], body_id), page=page)
    return make_oparl_response(result)

@oparl.route('/body/<string:body_id>/organization')
def oparl_body_organization(body_id):
    page = request.args.get('page', type=int, default=1)
    result = Organization.objects(**generate_filter_kwargs(body_id))\
        .order_by('-modified')\
        .resolve(page)\
        .page(base_url='%s/body/%s/organization' % (current_app.config['PROJECT_URL'], body_id), page=page)
    return make_oparl_response(result)


@oparl.route('/body/<string:body_id>/person')
def oparl_body_person(body_id):
    page = request.args.get('page', type=int, default=1)
    result = Person.objects(**generate_filter_kwargs(body_id))\
        .order_by('-modified')\
        .resolve(page)\
        .page(base_url='%s/body/%s/person' % (current_app.config['PROJECT_URL'], body_id), page=page)
    return make_oparl_response(result)

@oparl.route('/body/<string:body_id>/membership')
def oparl_body_membership(body_id):
    page = request.args.get('page', type=int, default=1)
    result = Membership.objects(**generate_filter_kwargs(body_id))\
        .order_by('-modified')\
        .resolve(page)\
        .page(base_url='%s/body/%s/membership' % (current_app.config['PROJECT_URL'], body_id), page=page)
    return make_oparl_response(result)

@oparl.route('/body/<string:body_id>/meeting')
def oparl_body_meeting(body_id):
    page = request.args.get('page', type=int, default=1)
    result = Meeting.objects(**generate_filter_kwargs(body_id))\
        .order_by('-modified')\
        .resolve(page)\
        .page(base_url='%s/body/%s/meeting' % (current_app.config['PROJECT_URL'], body_id), page=page)
    return make_oparl_response(result)

@oparl.route('/body/<string:body_id>/agenda_item')
def oparl_body_agenda_item(body_id):
    page = request.args.get('page', type=int, default=1)
    result = AgendaItem.objects(**generate_filter_kwargs(body_id))\
        .order_by('-modified')\
        .resolve(page)\
        .page(base_url='%s/body/%s/agenda_item' % (current_app.config['PROJECT_URL'], body_id), page=page)
    return make_oparl_response(result)

@oparl.route('/body/<string:body_id>/paper')
def oparl_body_paper(body_id):
    page = request.args.get('page', type=int, default=1)
    result = Paper.objects(**generate_filter_kwargs(body_id))\
        .order_by('-modified')\
        .resolve(page)\
        .page(base_url='%s/body/%s/paper' % (current_app.config['PROJECT_URL'], body_id), page=page)
    return make_oparl_response(result)

@oparl.route('/body/<string:body_id>/consultation')
def oparl_body_consultation(body_id):
    page = request.args.get('page', type=int, default=1)
    result = Consultation.objects(**generate_filter_kwargs(body_id))\
        .order_by('-modified')\
        .resolve(page)\
        .page(base_url='%s/body/%s/consultation' % (current_app.config['PROJECT_URL'], body_id), page=page)
    return make_oparl_response(result)

@oparl.route('/body/<string:body_id>/location')
def oparl_body_location(body_id):
    page = request.args.get('page', type=int, default=1)
    kwargs = generate_filter_kwargs(body_id)
    kwargs['body__contains'] = body_id
    del kwargs['body']
    result = Location.objects(**kwargs)\
        .order_by('-modified')\
        .resolve(page)\
        .page(base_url='%s/body/%s/location' % (current_app.config['PROJECT_URL'], body_id), page=page)
    return make_oparl_response(result)

@oparl.route('/body/<string:body_id>/file')
def oparl_body_file(body_id):
    page = request.args.get('page', type=int, default=1)
    result = File.objects(**generate_filter_kwargs(body_id))\
        .order_by('-modified')\
        .resolve(page)\
        .page(base_url='%s/body/%s/file' % (current_app.config['PROJECT_URL'], body_id), page=page)
    return make_oparl_response(result)

@oparl.route('/legislative_term/<string:id>')
def oparl_legislative_term(id):
    data = LegislativeTerm.objects(pk=id).resolve().first()
    return make_oparl_response(data)


@oparl.route('/organization/<string:id>')
def oparl_organization(id):
    data = Organization.objects(pk=id).resolve().first()
    return make_oparl_response(data)

@oparl.route('/organization/<string:id>/meeting')
def oparl_organization_meeting(id):
    page = request.args.get('page', type=int, default=1)
    additional_limits = {'organization': id}
    result = Meeting.objects(**generate_filter_kwargs(body_id=False, additional_limits=additional_limits))\
        .order_by('-modified')\
        .resolve(page)\
        .page(base_url='%s/organization/%s/meeting' % (current_app.config['PROJECT_URL'], id), page=page)
    return make_oparl_response(result)


@oparl.route('/person/<string:id>')
def oparl_person(id):
    data = Person.objects(pk=id).resolve().first()
    return make_oparl_response(data)


@oparl.route('/membership/<string:id>')
def oparl_membership(id):
    data = Membership.objects(pk=id).resolve().first()
    return make_oparl_response(data)


@oparl.route('/meeting/<string:id>')
def oparl_meeting(id):
    data = Meeting.objects(pk=id).resolve().first()
    return make_oparl_response(data)


@oparl.route('/agenda_item/<string:id>')
def oparl_agenda_item(id):
    data = AgendaItem.objects(pk=id).resolve().first()
    return make_oparl_response(data)


@oparl.route('/paper/<string:id>')
def oparl_paper(id):
    data = Paper.objects(pk=id).resolve().first()
    return make_oparl_response(data)


@oparl.route('/consultation/<string:id>')
def oparl_consultation(id):
    data = Consultation.objects(pk=id).resolve().first()
    return make_oparl_response(data)


@oparl.route('/location/<string:id>')
def oparl_location(id):
    data = Location.objects(pk=id).resolve().first()
    return make_oparl_response(data)


@oparl.route('/file/<string:id>')
def oparl_file(id):
    data = File.objects(pk=id).resolve().first()
    return make_oparl_response(data)
