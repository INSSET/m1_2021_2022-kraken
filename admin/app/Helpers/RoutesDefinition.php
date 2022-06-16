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

    public const LOGOUT_URL = 'logout';
    public const LOGOUT_NAME = 'logout';

}
