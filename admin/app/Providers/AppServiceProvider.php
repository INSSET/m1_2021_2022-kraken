<?php

namespace App\Providers;

use App\Services\API\GroupsServices;
use App\Services\API\StudentService;
use GuzzleHttp\Client;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {

        $this->app->singleton(StudentService::class, function ($app) {
            return new StudentService(
                new Client()
            );
        });

        $this->app->singleton(GroupsServices::class, function ($app) {
            return new GroupsServices(
                $app->make(Client::class),
                $app->make(StudentService::class)
            );
        });

    }
}
