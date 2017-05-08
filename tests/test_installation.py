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


def test_system_user(host):
    """
    Check if system user exists
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


def test_databases_and_privileges(host):
    """
    Check databases exists
    """

    expected_databases = ['foo', 'bar', 'foobar']
    existing_databases = host.check_output("psql -U postgres -c '\l'")

    # Test databases
    for expected_database in expected_databases:
        assert ' {} '.format(expected_database) in existing_databases

    # Test privileges
    assert 'bar_user' in existing_databases
    assert 'foo_user' not in existing_databases
    assert 'foobar_user' not in existing_databases


def test_databases_extensions(host):
    """
    Check databases extensions exists
    """

    databases = ['foo', 'bar', 'foobar']
    psql_command = "psql -U postgres -c '\dx' {}"

    for database in databases:
        database_extensions = host.check_output(psql_command.format(database))
        if database == 'foo':
            assert ' cube ' in database_extensions
        else:
            assert ' cube ' not in database_extensions


def test_users(host):
    """
    Check users exists
    """

    expected_users = ['foo_user', 'bar_user', 'foobar_user']
    existing_users = host.check_output("psql -U postgres -c '\du'")

    for expected_user in expected_users:
        assert ' {} '.format(expected_user) in existing_users
