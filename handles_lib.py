import os
import urllib.request
import json
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

handle_server = os.getenv('HANDLE_SERVER')
handle_client_path = os.getenv('HANDLE_CLIENT_PATH')
handle_log_path = os.getenv('HANDLE_LOG_PATH')
handle_key = os.getenv('HANDLE_KEY')
handle_passphrase = os.getenv('HANDLE_PASSPHRASE')
handle_user = os.getenv('HANDLE_USER')
handle_id = os.getenv('HANDLE_ID')
handle_target = os.getenv('HANDLE_TARGET')
handle_commands_path = os.getenv('HANDLE_COMMANDS_PATH')


def construct_auth():
    """
    Constructs auth command
    :return: String
    """

    auth_command = 'AUTHENTICATE PUBKEY:' + handle_user + handle_id + '\n'
    auth_command += handle_key + '|' + handle_passphrase + '\n'
    return auth_command


def get_handle(uuid):
    """
    Gets handle by uuid
    :param uuid:
    :return:
    """

    try:
        request = handle_server + handle_id + '/' + uuid
        response = urllib.request.urlopen(request).read()
        return json.loads(response)

    except urllib.error.HTTPError as e:
        print('Handle server response error ' + e)
        return e

    except urllib.error.URLError as e:
        print('Handle server is offline ' + e)
        return e


def create_handle(uuid):
    """
    Creates handle
    @param uuid
    @returns Boolean
    """

    command = construct_auth()
    command += '\n'
    command += 'CREATE ' + handle_id + '/' + uuid + '\n'
    command += '2 URL 86400 1110 UTF8 ' + handle_target + uuid + '\n'
    command += '\n'

    command_file = create_command_file('create', command)
    log_file = create_log_file('create', '', uuid)

    if command_file is False or log_file is False:
        print('Unable to create supporting file')
        return False

    command = handle_commands_path + command_file
    log = handle_log_path + log_file
    execute_command(command, log)
    delete_command_file(command_file)


def update_handle(uuid, new_handle_target):
    """
    Updates handle
    @param uuid
    @param new_handle_target
    @returns log
    """

    command = construct_auth()
    command += '\n'
    command += 'MODIFY ' + handle_id + '/' + uuid + '\n'
    command += '2 URL 86400 1110 UTF8 ' + new_handle_target + uuid + '\n'
    command += '\n'

    command_file = create_command_file('update', command)
    log_file = create_log_file('update', '', uuid)

    if command_file is False or log_file is False:
        print('Unable to create supporting file')
        return False

    command = handle_commands_path + command_file
    log = handle_log_path + log_file
    execute_command(command, log)
    delete_command_file(command_file)


def delete_handle(uuid):
    """
    Deletes handle
    @param uuid
    @returns log
    """

    command = construct_auth()
    command += '\n'
    command += 'DELETE ' + handle_id + '/' + uuid + '\n'
    command += '\n'

    command_file = create_command_file('delete', command)
    log_file = create_log_file('delete', '', uuid)

    if command_file is False or log_file is False:
        print('Unable to create supporting file')
        return False

    command = handle_commands_path + command_file
    log = handle_log_path + log_file
    execute_command(command, log)
    delete_command_file(command_file)


def execute_command(command, log):
    """
    Executes handle client command
    @param command
    @param log
    :return: Boolean
    """
    try:
        handle_client_exec = handle_client_path + 'bin/hdl-genericbatch '
        handle_cmd_exec = 'sh ' + handle_client_exec + ' ' + command + ' ' + log + ' -verbose'
        os.system(handle_cmd_exec)
        return True
    except Exception as e:
        print(e)
        return False


def create_command_file(action, command):
    """
    Creates the command file used by the handle client
    @param action
    @param command
    :return: Boolean
    """
    try:
        file = 'du_' + action + '_handle.txt'
        handle_command = open(handle_commands_path + file, 'a+')
        handle_command.write(command)
        return file
    except Exception as e:
        print(e)
        print('ERROR: Unable to create handle command file')
        return False


def create_log_file(action, uuid):
    """
    Creates the log file used by the handle client
    @param action
    @param uuid
    :return: String
    """
    try:
        file = 'du_' + action + '_handle_' + uuid + '.log'
        f = open(handle_log_path + file, 'a+')
        return file
    except Exception as e:
        print(e)
        print('ERROR: Unable to create handle log file')


def delete_command_file(command_file):
    """
    Deletes command file
    @param command_file
    :return: Boolean
    """
    try:
        if os.path.exists(handle_commands_path + command_file):
            os.remove(handle_commands_path + command_file)

        return True

    except Exception as e:
        print(e)
        print('ERROR: Unable to delete handle command file')
        return False
