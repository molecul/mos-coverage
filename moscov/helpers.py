import fuelclient
import subprocess
import json


def _get_command_output(cmd):
    pp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    outp, err = pp.communicate()

    if pp.returncode != 0:
        raise RuntimeError('Process returned non-zero code %i' % pp.returncode)

    return outp.strip()


def get_nodes(env=0):
    nodes = fuelclient.get_client(resource="node").get_all()
    result = {}
    for node in nodes:
        if (env > 0) and (node['cluster'] == env):
            result[node['id']] = node['roles']
        else:
            result[node['id']] = node['roles']
    return result


def get_envs():
    nodes = fuelclient.get_client(resource="node").get_all()
    result = []
    for node in nodes:
        if node['cluster'] not in result:
            result.append(node['cluster'])
    return result


def run_command_on_node(node, command):
    result = _get_command_output(
        "mco rpc --agent execute_shell_command --action execute "
        "--argument cmd='%s' -I %s -j" % (command, node))
    return json.loads(result)[0]


def run_coverage(nodes, component):
    pass