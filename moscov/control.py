from oslo_log import log
from oslo_config import cfg

from cliff.command import Command

from moscov import helpers

CONF = cfg.CONF
LOG = log.getLogger(__name__)
log.register_options(CONF)
log.setup(CONF, 'moscov')

components = ['glance', 'sahara']


class Init(Command):
    "initialization workspace for coverage collecting"

    def take_action(self, parsed_args):
        LOG.info('Starting initialization.')
        LOG.debug('Getting nodes list')
        nodes = helpers.get_nodes()
        LOG.debug('Have a %i nodes.' % len(nodes))
        for node in nodes:
            LOG.debug('On %s node installing coverage app.' % node)
            helpers.run_command_on_node(node, 'easy_install coverage==4.0a5')
            LOG.debug('On %s node create dirs tree.' % node)
            helpers.run_command_on_node(node, 'mkdir -p /coverage/rc;'
                                              'chmod 777 /coverage')
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
