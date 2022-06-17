<?php

namespace App\Helpers;

class RoutesDefinition
{
    public const ROUTE_NAME_PREFIX = 'cardinal.';

    /*
     *  Root Routes
     */


    public const ROOT_NAME = self::ROUTE_NAME_PREFIX . 'root';
    public const ROOT_URL = '/';

    /*
     *  Authentication Routes
     */

    public const AUTH_URL = '/login';
    public const AUTH_NAME = 'login';

    public const LOGOUT_URL = '/logout';
    public const LOGOUT_NAME = 'logout';

    /*
     *  SSH Keys Routes
     */
    
    public const SSH_SHOW_URL = '/ssh/{student}';
    public const SSH_SHOW_NAME = self::ROUTE_NAME_PREFIX . 'ssh';

    public const SSH_ADD_KEY_URL = '/students/{student}/ssh/upload';
    public const SSH_ADD_KEY_NAME = self::ROUTE_NAME_PREFIX . 'students.ssh.upload';

    public const SSH_SHOW_KEYS_URL = '/students/{student}/keys';
    public const SSH_SHOW_KEYS_NAME = self::ROUTE_NAME_PREFIX . 'students.keys';

    /*
     *  Container Routes
     */

    public const CONTAINERS_INDEX_URL = '/containers/{student}';
    public const CONTAINERS_INDEX_NAME = self::ROUTE_NAME_PREFIX . 'containers';

    public const CONTAINERS_SEND_ACTION_URL = '/students/{student}/container/command/{action}';
    public const CONTAINERS_SEND_ACTION_NAME = self::ROUTE_NAME_PREFIX . 'containers.send.action';

}