<?php

namespace App\Http\Controllers;

use App\Helpers\RoutesDefinition;
use App\Models\User;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\View\Factory;
use Illuminate\Contracts\View\View;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Routing\Redirector;
use Illuminate\Support\Facades\Auth;

class AuthenticationController extends Controller
{

    /**
     * @param Request $request
     * @return Application|Factory|View|RedirectResponse
     */
    public function index(Request $request): View|Factory|RedirectResponse|Application
    {

        if($request->isMethod("POST")) {

            $credentials = $request->validate([
                'email' => ['required', 'email:rfc'],
                'password' => ['required', 'string'],
                'remember_token' => ['nullable']
            ]);

            if($remember = $this->isSetRememberToken($credentials)) {

                unset($credentials['remember_token']);
            }

            if(Auth::attempt($credentials, $remember)) {

                $user = User::where(['email' => $credentials['email']])->first();

                if($user->enabled == false) {

                    return back()->withErrors([
                        'credentials' => __('Your account has been suspended.'),
                    ]);

                }

                $request->session()->regenerate();
                return redirect()->intended(route(RoutesDefinition::ROOT_NAME));
            }

            return back()->withErrors([
                'credentials' => __('The provided credentials do not match our records.'),
            ]);

        }

        return view('auth.login');

    }

    /**
     * @return Application|RedirectResponse|Redirector
     */
    public function logout(): Redirector|RedirectResponse|Application
    {
        auth()->logout();
        return redirect(route(RoutesDefinition::ROOT_NAME));
    }

    /**
     * @param $credentials
     * @return bool
     */
    private function isSetRememberToken($credentials): bool
    {
        return isset($credentials['remember_token']);
    }


}
