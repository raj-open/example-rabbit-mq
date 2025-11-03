#!/usr/bin/env bash
# ----------------------------------------------------------------
# Script for use with Rabbit MQ to register basic users
# ----------------------------------------------------------------

set -e
shopt -s expand_aliases

alias rabbit="rabbitmqctl --node rabbit@${HTTP_HOST_NAME_RABBIT}"

function create_user() {
    local user="$1"
    local pw="$2"
    rabbit delete_user "${user}" 2> /dev/null
    rabbit add_user "${user}" "${pw}"
}

function assign_basic_privileges() {
    local user="$1"
    local vhost="/"
    local options_conf=".*"
    local options_write=".*"
    local options_read=".*"
    # syntax: user conf write read
    # see <https://www.rabbitmq.com/docs/man/rabbitmqctl.8>
    rabbit set_permissions --quiet \
        --vhost "${vhost}" \
        "${user}" \
        "${options_conf}" "${options_write}" "${options_read}"
}

function assign_tags() {
    local user="$1"
    rabbit set_user_tags  --quiet "${user}" "${@:2}"
}

function create_basic_user() {
    local user="$1"
    local pw="$2"
    create_user "${user}" "${pw}"
    assign_basic_privileges "${user}"
    assign_tags "${user}" "basic"
}

function create_admin_user() {
    local user="$1"
    local pw="$2"
    create_user "${user}" "${pw}"
    assign_basic_privileges "${user}"
    assign_tags "${user}" "administrator"
}

# create admin
create_admin_user "${HTTP_ADMIN_USER_RABBIT}" "${HTTP_ADMIN_PASSWORD_RABBIT}"

# create guest
create_basic_user "${HTTP_GUEST_USER_RABBIT}" "${HTTP_GUEST_PASSWORD_RABBIT}"

# display users
rabbit list_users
