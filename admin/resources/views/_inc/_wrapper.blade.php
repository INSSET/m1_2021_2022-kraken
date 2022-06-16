@extends('_inc._app')

@section('content')

    <main>

        @include('_inc._menu')

        <section class="wrapper">

            @include('_inc._topbar')

            <div class="wrapper-content">

                @if(\App\Services\Breadcrumb::getList() !== null)

                    @include('_inc._breadcrumb')

                @endif

                @yield('wrapper')

            </div>

        </section>

    </main>

@endsection
