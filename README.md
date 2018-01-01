# postgresql

[![Build Status](https://img.shields.io/travis/infOpen/ansible-role-postgresql/master.svg?label=travis_master)](https://travis-ci.org/infOpen/ansible-role-postgresql)
[![Build Status](https://img.shields.io/travis/infOpen/ansible-role-postgresql/develop.svg?label=travis_develop)](https://travis-ci.org/infOpen/ansible-role-postgresql)
[![Updates](https://pyup.io/repos/github/infOpen/ansible-role-postgresql/shield.svg)](https://pyup.io/repos/github/infOpen/ansible-role-postgresql/)
[![Python 3](https://pyup.io/repos/github/infOpen/ansible-role-postgresql/python-3-shield.svg)](https://pyup.io/repos/github/infOpen/ansible-role-postgresql/)
[![Ansible Role](https://img.shields.io/ansible/role/17491.svg)](https://galaxy.ansible.com/infOpen/postgresql/)

Install postgresql package.

> **Note** This role use a *root* map to be able to run properly Ansible postgresql modules

## Requirements

This role requires Ansible 2.2 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Local and Travis tests run tests on Docker by default.
See molecule documentation to use other backend.

Currently, tests are done on:
- Debian Jessie
- Ubuntu Trusty
- Ubuntu Xenial

and use:
- Ansible 2.2.x
- Ansible 2.3.x
- Ansible 2.4.x

### Running tests

#### Using Docker driver

```
$ tox
```

## Role Variables

> Specific variables for **OS [*families|distribution|release*]** can be found
> in *vars* folder.

### Default role variables

``` yaml
# PostgreSQL installation
#------------------------------------------------------------------------------

# Repositories management
postgresql_cache_valid_time: 3600
postgresql_gpg_keys: "{{ _postgresql_gpg_keys }}"
postgresql_repositories: "{{ _postgresql_package_repositories }}"
postgresql_use_upstream: False

# Package management
postgresql_packages: "{{ _postgresql_packages }}"
postgresql_system_prerequisites: "{{ _postgresql_system_prerequisites }}"

# General
postgresql_version: "{{ _postgresql_version }}"

# Paths
postgresql_paths: "{{ _postgresql_paths }}"

# Service management
postgresql_services: "{{ _postgresql_services }}"

# System user and group
postgresql_system_user: "{{ _postgresql_system_user }}"
postgresql_system_group: "{{ _postgresql_system_group }}"


# PostgreSQL configuration
#------------------------------------------------------------------------------

# Environment
postgresql_config_environment: {}

# Main configuration file
postgresql_config_main: "{{ _postgresql_config_main }}"

# pg_ctl
postgresql_config_pg_ctl:
  pg_ctl_options: ''

# Client authentication
postgresql_config_pg_hba:
  - type: 'local'
    databases: 'all'
    user: 'postgres'
    address: ''
    method: 'peer map=root'
  - type: 'local'
    databases: 'all'
    user: 'all'
    address: ''
    method: 'peer'
  - type: 'host'
    databases: 'all'
    user: 'all'
    address: '127.0.0.1/32'
    method: 'md5'
  - type: 'host'
    databases: 'all'
    user: 'all'
    address: '::1/128'
    method: 'md5'

# User name maps
postgresql_config_pg_ident:
  - map_name: 'root'
    system_username: 'root'
    pg_username: 'postgres'
  - map_name: 'root'
    system_username: 'postgres'
    pg_username: 'postgres'

# Startup configuration
postgresql_config_start: 'auto'


# Databases and users management
#------------------------------------------------------------------------------

# Databases
postgresql_databases: []

# Databases extensions
postgresql_databases_extensions: []

# Users
postgresql_users: []

# Privileges
postgresql_privs: []
```

## Dependencies

None

## Example Playbook

``` yaml
- hosts: servers
  roles:
    - { role: infOpen.postgresql }
```

## License

MIT

## Author Information

Alexandre Chaussier (for Infopen company)
- http://www.infopen.pro
- a.chaussier [at] infopen.pro
