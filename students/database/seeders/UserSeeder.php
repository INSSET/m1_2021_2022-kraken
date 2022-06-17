<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\User\Role;
use Illuminate\Database\Seeder;

class UserSeeder extends Seeder
{

    public function run() {

        if(env('APP_ENV') !== 'production') {

            $user = new User();

            $user->name = "Laurent";
            $user->email = "john.doe@u-picardie.fr";
            $user->password = password_hash("admin", PASSWORD_DEFAULT);
            $user->role_id = Role::find(2)->id;
            $user->save();

        }

    }

}
