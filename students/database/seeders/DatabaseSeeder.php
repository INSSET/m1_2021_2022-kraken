<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        $permissionSeeder = new PermissionsSeeder();
        $permissionSeeder->run();

        $userSeeder = new UserSeeder();
        $userSeeder->run();
    }
}
