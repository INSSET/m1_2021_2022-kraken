<?php

use App\Helpers\RoutesDefinition;
use App\Http\Controllers\AuthenticationController;
use App\Http\Controllers\IndexController;
use App\Http\Controllers\StudentController;
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

    Route::controller(StudentController::class)->group(static function (){
        Route::get(RoutesDefinition::SSH_SHOW_URL, 'show')->name(RoutesDefinition::SSH_SHOW_NAME); 
        Route::post(RoutesDefinition::SSH_ADD_KEY_URL, 'uploadSshKey')->name(RoutesDefinition::SSH_ADD_KEY_NAME);    
        Route::get(RoutesDefinition::CONTAINERS_INDEX_URL, 'show_containers')->name(RoutesDefinition::CONTAINERS_INDEX_NAME);
        Route::post(RoutesDefinition::CONTAINERS_SEND_ACTION_URL, 'sendContainerCommand')->name(RoutesDefinition::CONTAINERS_SEND_ACTION_NAME);   
    });

});
