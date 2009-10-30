# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext as _
from django.template import RequestContext

from gestorpsi.util.views import get_object_or_None
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.client.models import Client
from gestorpsi.demographic.forms import EducationalLevelForm, ProfessionForm
from gestorpsi.demographic.models import EducationalLevel, Profession

@permission_required_with_403('client.client_read')
def home(request, object_id):
    object = get_object_or_404(Client, pk=object_id)
    return render_to_response('demographic/demographic_home.html', {
                                    'object': object,
                                    'demographic_menu': True,
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('client.client_read')
def education(request, object_id):
    object = get_object_or_404(Client, pk=object_id)
    if hasattr(object, 'educationallevel'):
        education_form = EducationalLevelForm(instance=object.educationallevel)
    else:
        education_form = EducationalLevelForm()

    return render_to_response('demographic/demographic_education.html', {
                                    'object': object,
                                    'demographic_menu': True,
                                    'education_form': education_form,
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('client.client_write')
def education_save(request, object_id):
    object = get_object_or_404(Client, pk=object_id)
    if hasattr(object, 'educationallevel'):
        education_form = EducationalLevelForm(request.POST, instance=object.educationallevel)
    else:
        education_form = EducationalLevelForm(request.POST, instance=EducationalLevel())
    education = education_form.save(commit=False)
    education.client = object
    education.save()
    request.user.message_set.create(message=_('Education saved successfully'))
    return render_to_response('demographic/demographic_education.html', {
                                        'object': object,
                                        'demographic_menu': True,
                                        'education_form': education_form,
                                        }, context_instance=RequestContext(request))

@permission_required_with_403('client.client_read')
def occupation(request, object_id, occupation_id=0):
    object = get_object_or_404(Client, pk=object_id)
    occupation_object = get_object_or_None(Profession, id=occupation_id) or Profession()
    profession_form = ProfessionForm(instance=occupation_object)
    professions = [p for p in object.profession_set.all()]
    return render_to_response('demographic/demographic_occupation.html', {
                                    'object': object,
                                    'demographic_menu': True,
                                    'professions': professions,
                                    'profession_form': profession_form,
                                    }, context_instance=RequestContext(request))

@permission_required_with_403('client.client_write')
def occupation_save(request, object_id, occupation_id=0):
    object = get_object_or_404(Client, pk=object_id)
    occupation_object = get_object_or_None(Profession, id=occupation_id) or Profession()
    profession_form = ProfessionForm(request.POST, instance=occupation_object)
    profession = profession_form.save(commit=False)
    profession.client = object
    profession.save()
    professions = [p for p in object.profession_set.all()]
    request.user.message_set.create(message=_('Occupation saved successfully'))
    return render_to_response('demographic/demographic_occupation.html', {
                                    'object': object,
                                    'demographic_menu': True,
                                    'professions': professions,
                                    'profession_form': profession_form,
                                    }, context_instance=RequestContext(request))