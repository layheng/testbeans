from django.shortcuts import render, get_object_or_404

# Create your views here.

import os
import shlex
from subprocess import Popen, PIPE

from django.http import HttpResponse
from .models import Feature

def index(request):
    command_line = "find -name *.feature"
    args = shlex.split(command_line)
    (out, err) = Popen(args, stdout=PIPE, stderr=PIPE).communicate()
    feature_list_str = out.splitlines()
    feature_list = Feature.objects.order_by('name')

    # update database automatically for any new features
    if (len(feature_list_str) != feature_list.count()):
        Feature.objects.all().delete()
        for line in feature_list_str:
            file_name = line.replace("./features/", "")
            feaute = Feature(name=file_name, file_path=line)
            feaute.save()
        feature_list = Feature.objects.order_by('name')

    context = {'feature_list': feature_list}
    return render(request, 'tester/index.html', context)

def result(request):
    last_four_lines = -4
    command_line = "behave" # -t=-bios -t=-switch_port_speed"
    args = shlex.split(command_line)
    (out, err) = Popen(args, stdout=PIPE, stderr=PIPE).communicate()
    result_report_str = out.splitlines()
    result_summary = result_report_str[last_four_lines:]
    result_lines = result_report_str[:last_four_lines]
    context = {'result_lines': result_lines, 'result_summary': result_summary}
    return render(request, 'tester/result.html', context)

def detail(request, feature_id):
    feature = get_object_or_404(Feature, pk=feature_id)
    feature.scenario_set.all().delete()

    # update scenarios to database for a selected feature
    previous_line = ''
    with open(os.path.join(feature.file_path)) as file:
        for line in file:
            line = line.strip()
            if line.startswith('Scenario', 0, len(line)):
                senario = feature.scenario_set.create(name=line, tag=previous_line)
                senario.save()
            else:
                previous_line = line

    context = {'feature': feature}
    return render(request, 'tester/detail.html', context)

def detailresult(request, feature_id):
    last_four_lines = -4
    feature = get_object_or_404(Feature, pk=feature_id)
    scenario_list = feature.scenario_set.all()
    command_line = "behave"
    for scenario in scenario_list:
        if (command_line.find(scenario.tag, 0, len(command_line)) is -1):
            command_line += " -t=" + scenario.tag
    args = shlex.split(command_line)
    (out, err) = Popen(args, stdout=PIPE, stderr=PIPE).communicate()
    result_report_str = out.splitlines()
    result_summary = result_report_str[last_four_lines:]
    result_lines = result_report_str[:last_four_lines]

    context = {'result_lines': result_lines, 'result_summary': result_summary}
    return render(request, 'tester/result.html', context)
