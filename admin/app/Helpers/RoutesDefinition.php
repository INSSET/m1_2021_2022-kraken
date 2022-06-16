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

    /*
     * Groups Routes
     */

    public const GROUPS_LIST_URL = '/groups';
    public const GROUPS_LIST_NAME = self::ROUTE_NAME_PREFIX . 'groups';

    public const GROUPS_EDIT_URL = '/groups/{groupId}';
    public const GROUPS_EDIT_NAME = self::ROUTE_NAME_PREFIX . 'groups.edit';

    public const GROUPS_UPDATE_URL = '/groups/update/{groupId}';
    public const GROUPS_UPDATE_NAME = self::ROUTE_NAME_PREFIX . 'groups.update';

    public const GROUPS_ADD_URL = '/groups/add';
    public const GROUPS_ADD_NAME = self::ROUTE_NAME_PREFIX . 'groups.add';
    
    /*
     * Students Routes
     */

    public const STUDENT_SHOW_URL = '/students/{student}';
    public const STUDENT_SHOW_NAME = self::ROUTE_NAME_PREFIX . 'students.show';

    public const STUDENT_ADD_KEY_URL = '/students/{student}/add/key';
    public const STUDENT_ADD_KEY_NAME = self::ROUTE_NAME_PREFIX . 'students.add.key';

    public const STUDENT_SEND_ACTION_URL = '/students/{student}/send/{action}';
    public const STUDENT_SEND_ACTION_NAME = self::ROUTE_NAME_PREFIX . 'students.send.action';



}
