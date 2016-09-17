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
    command_line = "behave -f plain -o outputs.text"
    args = shlex.split(command_line)
    (out, err) = Popen(args, stdout=PIPE, stderr=PIPE).communicate()
    result_report_str = out.splitlines()
    result_summary = result_report_str[last_four_lines:]

    # Detail test results from outputs.text
    result_lines = []
    with open('outputs.text') as f:
        for line in f:
            result_lines.append(line)

    # read feature/scenario/steps passed/failed line
    feature_list = result_report_str[last_four_lines].split()
    total_features = int(feature_list[0]) + int(feature_list[3])
    if total_features > 0:
        feature_pass = int(feature_list[0]) * 100 / total_features
    else:
        feature_pass = 0
    feature_fail = 100 - feature_pass
    feature_passed_percentage = str(feature_pass) + "%"
    feature_failed_percentage = str(feature_fail) + "%"
    feature_passed_progress = "width: " + feature_passed_percentage
    feature_failed_progress = "width: " + feature_failed_percentage

    scenario_list = result_report_str[last_four_lines+1].split()
    total_scenario = int(scenario_list[0]) + int(scenario_list[3])
    if total_scenario > 0:
        scenario_pass = int(scenario_list[0]) * 100 / total_scenario
    else:
        scenario_pass = 0
    scenario_fail = 100 - scenario_pass
    scenario_passed_percentage = str(scenario_pass) + "%"
    scenario_failed_percentage = str(scenario_fail) + "%"
    scenario_passed_progress = "width: " + scenario_passed_percentage
    scenario_failed_progress = "width: " + scenario_failed_percentage

    step_list = result_report_str[last_four_lines+2].split()
    total_steps = int(step_list[0]) + int(step_list[3])
    if total_steps > 0:
        step_pass = int(step_list[0]) * 100 / total_steps
    else:
        step_pass = 0
    step_fail = 100 - step_pass
    step_passed_percentage = str(step_pass) + "%"
    step_failed_percentage = str(step_fail) + "%"
    step_passed_progress = "width: " + step_passed_percentage
    step_failed_progress = "width: " + step_failed_percentage

    context = {'result_lines': result_lines, 'result_summary': result_summary,
               'feature_passed_progress': feature_passed_progress,
               'feature_failed_progress': feature_failed_progress,
               'feature_passed_percentage': feature_passed_percentage,
               'feature_failed_percentage': feature_failed_percentage,
               'scenario_passed_progress': scenario_passed_progress,
               'scenario_failed_progress': scenario_failed_progress,
               'scenario_passed_percentage': scenario_passed_percentage,
               'scenario_failed_percentage': scenario_failed_percentage,
               'step_passed_progress': step_passed_progress,
               'step_failed_progress': step_failed_progress,
               'step_passed_percentage': step_passed_percentage,
               'step_failed_percentage': step_failed_percentage}
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
    command_line = "behave -f plain -o outputs.text -t="
    for scenario in scenario_list:
        if scenario.tag.startswith('./features'):
            command_line = "behave -f plain -o outputs.text " + scenario.tag
            break
        elif command_line.find(scenario.tag, 0, len(command_line)) is -1:
            if command_line != "behave -f plain -o outputs.text -t=":
                command_line += "," + scenario.tag
            else:
                command_line += scenario.tag
    args = shlex.split(command_line)
    (out, err) = Popen(args, stdout=PIPE, stderr=PIPE).communicate()
    result_report_str = out.splitlines()
    result_summary = result_report_str[last_four_lines:]

    # Detail test results from outputs.text
    result_lines = []
    with open('outputs.text') as f:
        for line in f:
            result_lines.append(line)

    # read feature/scenario/steps passed/failed line
    feature_list = result_report_str[last_four_lines].split()
    total_features = int(feature_list[0]) + int(feature_list[3])
    if total_features > 0:
        feature_pass = int(feature_list[0]) * 100 / total_features
    else:
        feature_pass = 0
    feature_fail = 100 - feature_pass
    feature_passed_percentage = str(feature_pass) + "%"
    feature_failed_percentage = str(feature_fail) + "%"
    feature_passed_progress = "width: " + feature_passed_percentage
    feature_failed_progress = "width: " + feature_failed_percentage

    scenario_list = result_report_str[last_four_lines + 1].split()
    total_scenario = int(scenario_list[0]) + int(scenario_list[3])
    if total_scenario > 0:
        scenario_pass = int(scenario_list[0]) * 100 / total_scenario
    else:
        scenario_pass = 0
    scenario_fail = 100 - scenario_pass
    scenario_passed_percentage = str(scenario_pass) + "%"
    scenario_failed_percentage = str(scenario_fail) + "%"
    scenario_passed_progress = "width: " + scenario_passed_percentage
    scenario_failed_progress = "width: " + scenario_failed_percentage

    step_list = result_report_str[last_four_lines + 2].split()
    total_steps = int(step_list[0]) + int(step_list[3])
    if total_steps > 0:
        step_pass = int(step_list[0]) * 100 / total_steps
    else:
        step_pass = 0
    step_fail = 100 - step_pass
    step_passed_percentage = str(step_pass) + "%"
    step_failed_percentage = str(step_fail) + "%"
    step_passed_progress = "width: " + step_passed_percentage
    step_failed_progress = "width: " + step_failed_percentage

    context = {'result_lines': result_lines, 'result_summary': result_summary,
               'feature_passed_progress': feature_passed_progress,
               'feature_failed_progress': feature_failed_progress,
               'feature_passed_percentage': feature_passed_percentage,
               'feature_failed_percentage': feature_failed_percentage,
               'scenario_passed_progress': scenario_passed_progress,
               'scenario_failed_progress': scenario_failed_progress,
               'scenario_passed_percentage': scenario_passed_percentage,
               'scenario_failed_percentage': scenario_failed_percentage,
               'step_passed_progress': step_passed_progress,
               'step_failed_progress': step_failed_progress,
               'step_passed_percentage': step_passed_percentage,
               'step_failed_percentage': step_failed_percentage}
    return render(request, 'tester/result.html', context)
