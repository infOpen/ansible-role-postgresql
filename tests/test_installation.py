"""
Role tests
"""

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')

POSTGRESQL_VERSION = {
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
    postgresql_version = POSTGRESQL_VERSION[os_distribution][os_codename]

    if host.system_info.distribution in ('debian', 'ubuntu'):
        packages = [
            'ca-certificates',
            'postgresql-{}'.format(postgresql_version),
            'postgresql-common',
            'postgresql-client-{}'.format(postgresql_version),
            'postgresql-client-common',
            'postgresql-contrib-{}'.format(postgresql_version),
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
