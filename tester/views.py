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

    # Decode feature/scenario/steps passed/failed numbers
    (passed_percentage, failed_percentage,
     passed_progress, failed_progress) = decode_test_summary(result_summary)

    context = {'result_lines': result_lines,
               'result_summary': result_summary,
               'passed_progress': passed_progress,
               'failed_progress': failed_progress,
               'passed_percentage': passed_percentage,
               'failed_percentage': failed_percentage}
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

    # Decode feature/scenario/steps passed/failed numbers
    (passed_percentage, failed_percentage,
     passed_progress, failed_progress) = decode_test_summary(result_summary)

    context = {'result_lines': result_lines,
               'result_summary': result_summary,
               'passed_progress': passed_progress,
               'failed_progress': failed_progress,
               'passed_percentage': passed_percentage,
               'failed_percentage': failed_percentage}
    return render(request, 'tester/result.html', context)


def decode_test_summary(summary):
    """
    Decode test result summary
    :param summary: list of test summary with features, scenarios and steps
    :return: passed/failed percentage and progress
    """
    passed_percentage = []
    failed_percentage = []
    passed_progress = []
    failed_progress = []
    pass_index = 0
    fail_index = 3

    # decode features
    feature_list = summary[0].split()
    total_features = int(feature_list[pass_index]) + int(feature_list[fail_index])
    if total_features > 0:
        pass_value = int(feature_list[pass_index]) * 100.0 / total_features
    else:
        pass_value = 0.0
    feature_pass = "{0:.2f}".format(pass_value)
    feature_fail = "{0:.2f}".format(100.0 - pass_value)
    passed_percentage.append(feature_pass + "%")
    failed_percentage.append(feature_fail + "%")
    passed_progress.append("width: " + feature_pass + "%")
    failed_progress.append("width: " + feature_fail + "%")

    # decode scenarios
    scenario_list = summary[1].split()
    total_scenario = int(scenario_list[pass_index]) + int(scenario_list[fail_index])
    if total_scenario > 0:
        pass_value = int(scenario_list[pass_index]) * 100.0 / total_scenario
    else:
        pass_value = 0.0
    scenario_pass = "{0:.2f}".format(pass_value)
    scenario_fail = "{0:.2f}".format(100.0 - pass_value)
    passed_percentage.append(scenario_pass + "%")
    failed_percentage.append(scenario_fail + "%")
    passed_progress.append("width: " + scenario_pass + "%")
    failed_progress.append("width: " + scenario_fail + "%")

    # decode steps
    step_list = summary[2].split()
    total_steps = int(step_list[pass_index]) + int(step_list[fail_index])
    if total_steps > 0:
        pass_value = int(step_list[pass_index]) * 100.0 / total_steps
    else:
        pass_value = 0.0
    step_pass = "{0:.2f}".format(pass_value)
    step_fail = "{0:.2f}".format(100.0 - pass_value)
    passed_percentage.append(step_pass + "%")
    failed_percentage.append(step_fail + "%")
    passed_progress.append("width: " + step_pass + "%")
    failed_progress.append("width: " + step_fail + "%")

    return passed_percentage, failed_percentage, passed_progress, failed_progress
