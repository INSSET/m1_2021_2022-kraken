<?php

use App\Helpers\RoutesDefinition;
use App\Http\Controllers\AuthenticationController;
use App\Http\Controllers\Groups\GroupsController;
use App\Http\Controllers\IndexController;
use App\Http\Controllers\Students\StudentsController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get(RoutesDefinition::AUTH_URL, [AuthenticationController::class, 'index'])->name(RoutesDefinition::AUTH_NAME);
Route::post(RoutesDefinition::AUTH_URL, [AuthenticationController::class, 'index'])->name(RoutesDefinition::AUTH_NAME);

Route::middleware(['auth'])->prefix('/')->group(static function () {

    Route::get(RoutesDefinition::ROOT_URL, [IndexController::class, 'index'])->name(RoutesDefinition::ROOT_NAME);
    Route::get(RoutesDefinition::LOGOUT_URL, [AuthenticationController::class, 'logout'])->name(RoutesDefinition::LOGOUT_NAME);

    Route::controller(GroupsController::class)->group(static function () {
        Route::get(RoutesDefinition::GROUPS_LIST_URL, 'index')->name(RoutesDefinition::GROUPS_LIST_NAME);
        Route::get(RoutesDefinition::GROUPS_EDIT_URL, 'edit')->name(RoutesDefinition::GROUPS_EDIT_NAME);

        Route::post(RoutesDefinition::GROUPS_ADD_URL, 'add')->name(RoutesDefinition::GROUPS_ADD_NAME);
        Route::post(RoutesDefinition::GROUPS_UPDATE_URL, 'update')->name(RoutesDefinition::GROUPS_UPDATE_NAME);
    });

});
