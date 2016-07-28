import yaml

from oslo_log import log
from oslo_config import cfg

from cliff.command import Command

from moscov import helpers

CONF = cfg.CONF
LOG = log.getLogger(__name__)
log.register_options(CONF)
log.setup(CONF, 'moscov')

components = [
    'nova',
    'murano',
    'glance',
    'cinder',
    'sahara',
    'ceilometer',
    'ironic'
]


class Init(Command):
    "initialization workspace for coverage collecting"

    def take_action(self, parsed_args):
        LOG.info('Starting initialization.')
        LOG.debug('Getting nodes list')
        nodes = helpers.get_nodes()
        LOG.debug('Have a %i nodes.' % len(nodes))
        for node in nodes:
            LOG.info('On node-%s installing coverage app.' % node)
            r = helpers.run_command_on_node(node, 'easy_install '
                                                  'coverage==4.0a5')
            LOG.debug(r)
            LOG.info('On node-%s create dirs tree.' % node)
            r = helpers.run_command_on_node(node, 'mkdir -p /coverage/rc; '
                                                  'chmod 777 /coverage')
            LOG.debug(r)
        LOG.info('Initialization was finished.')


class Start(Command):
    "start coverage collecting"

    def get_parser(self, prog_name):
        parser = super(Start, self).get_parser(prog_name)
        parser.add_argument(
            type=int,
            help='fuel environment id, avaliable: %s' % helpers.get_envs(),
            dest='env_id'
            )
        parser.add_argument(
            type=str,
            help='target name component for coverage collecting, '
                 'supported: %s' % components,
            dest='component'
            )
        return parser

    def take_action(self, parsed_args):
        valid_fuel_envs = helpers.get_envs()
        current_component = parsed_args.component.lower()
        if parsed_args.env_id not in valid_fuel_envs:
            LOG.error('Current cluster not available.')
            return False
        if current_component not in components:
            LOG.error('Current component `%s` was not supported.' %
                      current_component)
            return False
        nodes = helpers.get_nodes(env=parsed_args.env_id)
        LOG.info('Selected a %s node(s).' % len(nodes))
        enabled_services = helpers.run_command_on_node(
            nodes.keys()[0], 'cat /etc/hiera/astute.yaml')
        enabled_services = yaml.load(enabled_services['data']['stdout'])
        if current_component not in enabled_services:
            LOG.error('Current component `%s` was not supported.' %
                      current_component)
            return False
        else:
            if 'enabled' in enabled_services[current_component]:
                if not enabled_services[current_component].get('enable'):
                    LOG.error('Current component `%s` was disabled in current '
                              'environment.' % current_component)
                    return False
        LOG.info('Target `%s` component.' % current_component)

        for node in nodes:
            result = helpers.run_command_on_node(
                node,
                "ps -e -o comm | grep %s" % current_component)['data']['stdout']
            current_services = []
            for i in result.split("\n"):
                if current_component in i:
                    if i not in current_services:
                        current_services.append(i)
            LOG.info('Get service list on node-%s: %s' % (
                node,
                str(current_services)))

            for current_service in current_services:
                cmdline = helpers.run_command_on_node(
                    node,
                    'xargs -0 < /proc/$(ps ax | grep %s | grep -v grep '
                    '| grep -oP "^\s*[0-9]*(?= )" | tr -d " "'
                    '| head -1)/cmdline' %
                    current_service)['data']['stdout'].strip()
                LOG.info("Service %s run by: %s" % (current_service, cmdline))
