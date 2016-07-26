import fuelclient
import subprocess


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
            result[node['ip']] = node['roles']
        else:
            result[node['ip']] = node['roles']
    return result


def get_envs():
    nodes = fuelclient.get_client(resource="node").get_all()
    result = []
    for node in nodes:
        if node['cluster'] not in result:
            result.append(node['cluster'])
    return result


def run_command_on_node(node, command):
    return _get_command_output("ssh -o LogLevel=quiet %s '%s'" % (node,
                                                                  command))
