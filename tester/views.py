import os
import shlex
from subprocess import Popen, PIPE
from django.shortcuts import render, get_object_or_404
from .models import Feature, Scenario, UserData


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
        user_data_entry = UserData(name=temp_list[0].strip(), value=temp_list[1].strip())
        user_data_entry.save()
    user_data_list = UserData.objects.all()

    context = {'feature_list': feature_list, 'user_data_list': user_data_list}
    return render(request, 'tester/index.html', context)


def result(request):
    message_error = None
    last_four_lines = -4
    out = ""
    err = ""

    # read parameters
    user_data_list = UserData.objects.all()
    options = ""
    for user_data in user_data_list:
        options += " -D " + user_data.name + "=" + request.POST[user_data.name]

    # update configuration file behave.ini
    new_lines = []
    with open('behave.ini', 'r') as config_file:
        for line in config_file:
            new_lines.append(line)
            if 'behave.userdata' in line:
                break
    for user_data in user_data_list:
        new_lines.append(user_data.name + "=" + request.POST[user_data.name] + '\n')
    with open('behave.ini', 'w') as config_file:
        config_file.writelines(new_lines)

    # put together the command line string
    command_line = "behave -f plain -o outputs.text" + options
    try:
        (out, err) = Popen(shlex.split(command_line), stdout=PIPE, stderr=PIPE).communicate()
        result_report_str = out.splitlines()
        result_summary = result_report_str[last_four_lines:]

        # Detail test results from outputs.text
        result_lines = []
        with open('outputs.text') as output_file:
            for line in output_file:
                result_lines.append(line)

        # Decode feature/scenario/steps passed/failed numbers
        (passed_percentage, failed_percentage) = decode_test_summary(result_summary)
    except Exception as error:
        result_summary = [out, err]
        result_lines = [out, err]
        passed_percentage = 0
        failed_percentage = 0
        message_error = error

    context = {'result_lines': result_lines,
               'result_summary': result_summary,
               'passed_percentage': passed_percentage,
               'failed_percentage': failed_percentage,
               'message_error': message_error}
    return render(request, 'tester/result.html', context)


def detail(request, feature_id):
    feature = get_object_or_404(Feature, pk=feature_id)
    feature.scenario_set.all().delete()

    # update scenarios to database for a selected feature
    previous_line = ''
    with open(os.path.join(feature.file_path)) as feature_file:
        for line in feature_file:
            line = line.strip()
            if line.startswith('Scenario', 0, len(line)):
                if previous_line:
                    scenario = feature.scenario_set.create(name=line, tag=previous_line)
                else:
                    scenario = feature.scenario_set.create(name=line, tag=feature.file_path)
                scenario.save()
            else:
                previous_line = line

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
        user_data_entry = UserData(name=temp_list[0].strip(), value=temp_list[1].strip())
        user_data_entry.save()
    user_data_list = UserData.objects.all()

    context = {'feature': feature, 'user_data_list': user_data_list}
    return render(request, 'tester/detail.html', context)


def detailresult(request, feature_id):
    message_error = None
    last_four_lines = -4
    out = ""
    err = ""

    # read parameters
    user_data_list = UserData.objects.all()
    options = ""
    for user_data in user_data_list:
        options += " -D " + user_data.name + "=" + request.POST[user_data.name]

    # update configuration file behave.ini
    new_lines = []
    with open('behave.ini', 'r') as config_file:
        for line in config_file:
            new_lines.append(line)
            if 'behave.userdata' in line:
                break
    for user_data in user_data_list:
        new_lines.append(user_data.name + "=" + request.POST[user_data.name] + '\n')
    with open('behave.ini', 'w') as config_file:
        config_file.writelines(new_lines)

    # put together the command line string
    feature = get_object_or_404(Feature, pk=feature_id)
    command_line = "behave -f plain -o outputs.text " + feature.file_path + options
    try:
        (out, err) = Popen(shlex.split(command_line), stdout=PIPE, stderr=PIPE).communicate()
        result_report_str = out.splitlines()
        result_summary = result_report_str[last_four_lines:]

        # Detail test results from outputs.text
        result_lines = []
        with open('outputs.text') as output_file:
            for line in output_file:
                result_lines.append(line)

        # Decode feature/scenario/steps passed/failed numbers
        (passed_percentage, failed_percentage) = decode_test_summary(result_summary)
    except Exception as error:
        result_summary = [out, err]
        result_lines = [out, err]
        passed_percentage = 0
        failed_percentage = 0
        message_error = error

    context = {'result_lines': result_lines,
               'result_summary': result_summary,
               'passed_percentage': passed_percentage,
               'failed_percentage': failed_percentage,
               'message_error': message_error}
    return render(request, 'tester/result.html', context)


def detailscenario(request, feature_id, scenario_id):
    feature = get_object_or_404(Feature, pk=feature_id)
    scenario = feature.scenario_set.get(pk=scenario_id)

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
    if UserData.objects.all():
        UserData.objects.all().delete()
    for line in user_data:
        temp_list = line.split('=')
        user_data_entry = UserData(name=temp_list[0].strip(), value=temp_list[1].strip())
        user_data_entry.save()
    user_data_list = UserData.objects.all()

    context = {'feature': feature, 'scenario': scenario, 'user_data_list': user_data_list}
    return render(request, 'tester/detailscenario.html', context)


def detailscenarioresult(request, scenario_id):
    message_error = None
    last_four_lines = -4
    out = ""
    err = ""

    # read parameters
    user_data_list = UserData.objects.all()
    options = ""
    for user_data in user_data_list:
        options += " -D " + user_data.name + "=" + request.POST[user_data.name]

    # update configuration file behave.ini
    new_lines = []
    with open('behave.ini', 'r') as config_file:
        for line in config_file:
            new_lines.append(line)
            if 'behave.userdata' in line:
                break
    for user_data in user_data_list:
        new_lines.append(user_data.name + "=" + request.POST[user_data.name] + '\n')
    with open('behave.ini', 'w') as config_file:
        config_file.writelines(new_lines)

    # put together the command line string
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    scenario_name_list = scenario.name.split()
    command_line = "behave -f plain -o outputs.text -n " + scenario_name_list[1] + options
    try:
        (out, err) = Popen(shlex.split(command_line), stdout=PIPE, stderr=PIPE).communicate()
        result_report_str = out.splitlines()
        result_summary = result_report_str[last_four_lines:]

        # Detail test results from outputs.text
        result_lines = []
        with open('outputs.text') as output_file:
            for line in output_file:
                result_lines.append(line)

        # Decode feature/scenario/steps passed/failed numbers
        (passed_percentage, failed_percentage) = decode_test_summary(result_summary)
    except Exception as error:
        result_summary = [out, err]
        result_lines = [out, err]
        passed_percentage = 0
        failed_percentage = 0

    context = {'result_lines': result_lines,
               'result_summary': result_summary,
               'passed_percentage': passed_percentage,
               'failed_percentage': failed_percentage,
               'message_error': message_error}
    return render(request, 'tester/result.html', context)


def decode_test_summary(summary):
    """
    Decode test result summary
    :param summary: list of test summary with features, scenarios and steps
    :return: passed/failed percentage and progress
    """
    pass_index = 0
    fail_index = 3
    total_features = 0
    total_scenario = 0
    total_steps = 0
    passed_percentage = []
    failed_percentage = []

    # decode features
    if len(summary) > 0:
        feature_list = summary[0].split()
        total_features = int(feature_list[pass_index]) + int(feature_list[fail_index])

    if total_features > 0:
        passed_value = float(feature_list[pass_index]) / total_features
    else:
        passed_value = 0.0
    failed_value = 1.0 - passed_value
    passed_percentage.append(passed_value)
    failed_percentage.append(failed_value)

    # decode scenarios
    if len(summary) > 1:
        scenario_list = summary[1].split()
        total_scenario = int(scenario_list[pass_index]) + int(scenario_list[fail_index])

    if total_scenario > 0:
        passed_value = float(scenario_list[pass_index]) / total_scenario
    else:
        passed_value = 0.0
    failed_value = 1.0 - passed_value
    passed_percentage.append(passed_value)
    failed_percentage.append(failed_value)

    # decode steps
    if len(summary) > 2:
        step_list = summary[2].split()
        total_steps = int(step_list[pass_index]) + int(step_list[fail_index])

    if total_steps > 0:
        passed_value = float(step_list[pass_index]) / total_steps
    else:
        passed_value = 0.0
    failed_value = 1.0 - passed_value
    passed_percentage.append(passed_value)
    failed_percentage.append(failed_value)

    return passed_percentage, failed_percentage
