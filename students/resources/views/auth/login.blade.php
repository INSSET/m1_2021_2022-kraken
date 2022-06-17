@extends('_inc._app')

@section('title', 'Connexion à Cardinal - Hyrisia')

@section('blank', 'true')

@section('content')

    <section class="hyr-auth-container">

        <div class="hyr-auth-content">

            <a href="{{ route(\App\Helpers\RoutesDefinition::ROOT_NAME) }}" class="">
                <h3>Gestproj - Espace de connexion</h3>
            </a>

            @if($errors->any())
                <p class="alert alert-error">{{$errors->first()}}</p>
            @endif

            <section>
                <div class="hyr-auth-form">

                    <div class="hyr-auth-loader" style="display: none">
                        <i class="fa-duotone fa-spinner-third fa-spin-pulse"></i>
                    </div>

                    <div class="hyr-auth-title">
                        <hr>
                        <h6>{{ __('Admin') }}</h6>
                        <hr>
                    </div>

                    <form method="post">

                        @csrf

                        <div class="form-group">

                            <input class="hyr-input" type="text" name="email" id="email" placeholder="{{ __('Email') }}">

                        </div>

                        <div class="form-group">

                            <input class="hyr-input" type="password" name="password" id="password" placeholder="{{ __('Password') }}">

                        </div>

                        <div class="d-flex justify-content-between">

                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" name="remember_token" id="remember_token">
                                <label class="form-check-label" for="remember_token">
                                    {{ __('Stay online') }}
                                </label>
                            </div>

                            <a href="#" class="forgot-password">{{ __('Forgot password ?') }}</a>

                        </div>

                        <div class="form-group">

                            <button type="submit" class="hyr-button-primary">{{__('Sign in') }}</button>

                        </div>

                    </form>

                </div>

            </section>

        </div>

    </section>

@endsection
