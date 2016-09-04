import os
import shlex
from subprocess import Popen, PIPE
from django.shortcuts import render, get_object_or_404
from .models import Feature, UserData


# Create your views here.
def index(request):
    command_line = "find -name *.feature"
    args = shlex.split(command_line)
    (out, err) = Popen(args, stdout=PIPE, stderr=PIPE).communicate()
    feature_list_str = out.splitlines()
    # update database for feature list
    Feature.objects.all().delete()
    for line in feature_list_str:
        file_name = line.replace("./features/", "")
        feature = Feature(name=file_name, file_path=line)
        feature.save()
    feature_list = Feature.objects.order_by('name')
    # extract user data
    user_data = []
    start_user_data = False
    with open('behave.ini') as config_file:
        for line in config_file:
            if 'behave.userdata' in line:
                start_user_data = True
            elif start_user_data and "end of userdata" not in line:
                user_data.append(line)
            elif "end of userdata" in line:
                break
    # update database for user data
    UserData.objects.all().delete()
    for line in user_data:
        temp_list = line.split('=')
        user_data = UserData(name=temp_list[0], value=temp_list[1].strip())
        user_data.save()
    user_data_list = UserData.objects.all()
    context = {'feature_list': feature_list, 'user_data_list': user_data_list}
    return render(request, 'tester/index.html', context)


def result(request):
    last_four_lines = -4
    command_line = "behave"
    args = shlex.split(command_line)
    (out, err) = Popen(args, stdout=PIPE, stderr=PIPE).communicate()
    result_report_str = out.splitlines()
    result_summary = result_report_str[last_four_lines:]
    result_lines = result_report_str[:last_four_lines]
    # read scenario passed/failed line
    progress_list = result_report_str[last_four_lines+1].split()
    total_scenario = int(progress_list[0]) + int(progress_list[3])
    if total_scenario > 0:
        scenario_pass = int(progress_list[0]) * 100 / total_scenario
    else:
        scenario_pass = 0
    scenario_fail = 100 - scenario_pass
    pass_percentage = str(scenario_pass) + "%"
    fail_percentage = str(scenario_fail) + "%"
    pass_progress = "width: " + pass_percentage
    fail_progress = "width: " + fail_percentage
    context = {'result_lines': result_lines, 'result_summary': result_summary,
               'pass_progress': pass_progress, 'fail_progress': fail_progress,
               'pass_percentage': pass_percentage, 'fail_percentage': fail_percentage}
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
                if previous_line:
                    scenario = feature.scenario_set.create(name=line, tag=previous_line)
                else:
                    scenario = feature.scenario_set.create(name=line, tag=feature.file_path)
                scenario.save()
            else:
                previous_line = line
    context = {'feature': feature}
    return render(request, 'tester/detail.html', context)


def detailresult(request, feature_id):
    last_four_lines = -4
    feature = get_object_or_404(Feature, pk=feature_id)
    scenario_list = feature.scenario_set.all()
    command_line = "behave -t="
    for scenario in scenario_list:
        if scenario.tag.startswith('./features'):
            command_line = "behave " + scenario.tag
            break
        elif command_line.find(scenario.tag, 0, len(command_line)) is -1:
            if command_line != "behave -t=":
                command_line += "," + scenario.tag
            else:
                command_line += scenario.tag
    args = shlex.split(command_line)
    (out, err) = Popen(args, stdout=PIPE, stderr=PIPE).communicate()
    result_report_str = out.splitlines()
    result_summary = result_report_str[last_four_lines:]
    result_lines = result_report_str[:last_four_lines]
    # read scenario passed/failed line
    progress_list = result_report_str[last_four_lines+1].split()
    total_scenario = int(progress_list[0]) + int(progress_list[3])
    if total_scenario > 0:
        scenario_pass = int(progress_list[0]) * 100 / total_scenario
    else:
        scenario_pass = 0
    scenario_fail = 100 - scenario_pass
    pass_percentage = str(scenario_pass) + "%"
    fail_percentage = str(scenario_fail) + "%"
    pass_progress = "width: " + pass_percentage
    fail_progress = "width: " + fail_percentage
    context = {'result_lines': result_lines, 'result_summary': result_summary,
               'pass_progress': pass_progress, 'fail_progress': fail_progress,
               'pass_percentage': pass_percentage, 'fail_percentage': fail_percentage}
    return render(request, 'tester/result.html', context)
