<?php

namespace App\Http\Controllers;

class IndexController extends Controller
{
    public function index() {
        return view('dashboard.index');
    }
}
