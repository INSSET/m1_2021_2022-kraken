<?php

namespace Database\Seeders;

use App\Models\User\Permission;
use App\Models\User\Role;
use Illuminate\Database\Seeder;

class PermissionsSeeder extends Seeder
{

    public const ROLE_ADMIN = 'administrator';
    public const ROLE_DEFAULT = 'default';

    public const ACCESS_ADMINISTRATION_USERS = 'access_administration_users';

    public function run() {

        $this->roles();

    }

    private function roles() {

        $accessAdministrationUser = new Permission();
        $accessAdministrationUser->label = self::ACCESS_ADMINISTRATION_USERS;
        $accessAdministrationUser->description = "Administration des utilisateurs du panel";
        $accessAdministrationUser->save();

        $default = new Role();

        $default->label = self::ROLE_DEFAULT;
        $default->description = "Default account";
        $default->parent_id = null;

        $default->save();

        $admin = new Role();

        $admin->label = self::ROLE_ADMIN;
        $admin->description = "Full access";
        $admin->parent_id = null;
        $admin->can_bypass = true;
        $admin->rank = 100;

        $admin->save();

        $admin->permissions()->attach([
            $accessAdministrationUser->id
        ]);

    }

}
