"""
Role tests
"""

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')

PG_VERSION = {
    'debian': {
        'jessie': '9.4',
    },
    'ubuntu': {
        'trusty': '9.3',
        'xenial': '9.5',
    },
}


def test_packages(host):
    """
    Check if packages are installed
    """

    packages = []
    os_distribution = host.system_info.distribution
    os_codename = host.system_info.codename
    pg_version = PG_VERSION[os_distribution][os_codename]

    if host.system_info.distribution in ('debian', 'ubuntu'):
        packages = [
            'ca-certificates',
            'locales',
            'postgresql-{}'.format(pg_version),
            'postgresql-common',
            'postgresql-client-{}'.format(pg_version),
            'postgresql-client-common',
            'postgresql-contrib-{}'.format(pg_version),
            'python-psycopg2',
        ]

    for package in packages:
        assert host.package(package).is_installed


def test_service(host):
    """
    Check if database service is started and enabled
    """

    service = ''

    if host.system_info.distribution in ('debian', 'ubuntu'):
        service = 'postgresql'

    assert host.service(service).is_enabled

    # Systemctl not available with Docker images
    if 'docker' != host.backend.NAME:
        assert host.service(service).is_running


def test_user(host):
    """
    Check if database user exists
    """

    if host.system_info.distribution in ('debian', 'ubuntu'):
        assert host.user('postgres').exists
        assert host.user('postgres').group == 'postgres'
        assert host.user('postgres').home == '/var/lib/postgresql'
        assert host.user('postgres').shell == '/bin/bash'


def test_config_files(host):
    """
    Check if configuration files exists
    """

    config_files = []
    os_distribution = host.system_info.distribution
    os_codename = host.system_info.codename
    pg_version = PG_VERSION[os_distribution][os_codename]

    if host.system_info.distribution in ('debian', 'ubuntu'):
        config_files = [
            '/etc/postgresql/{}/main/environment'.format(pg_version),
            '/etc/postgresql/{}/main/pg_ctl.conf'.format(pg_version),
            '/etc/postgresql/{}/main/pg_hba.conf'.format(pg_version),
            '/etc/postgresql/{}/main/pg_ident.conf'.format(pg_version),
            '/etc/postgresql/{}/main/postgresql.conf'.format(pg_version),
            '/etc/postgresql/{}/main/start.conf'.format(pg_version),
        ]

    for config_file in config_files:
        assert host.file(config_file).exists
        assert host.file(config_file).user == 'postgres'
        assert host.file(config_file).group == 'postgres'
        if 'ident' in config_file or 'hba' in config_file:
            assert host.file(config_file).mode == 0o640
        else:
            assert host.file(config_file).mode == 0o644
