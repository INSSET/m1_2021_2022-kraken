<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/png" href="{{ asset('image/logo/red.png') }}"/>

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
    />
    <link rel="stylesheet" href="https://cdn.datatables.net/1.12.0/css/jquery.dataTables.min.css">
    <!-- Fontawesome -->

    <link rel="stylesheet" href="{{ asset('fontawesome/fontawesome.min.css') }}">
    <link rel="stylesheet" href="{{ asset('fontawesome/all.min.css') }}">

    <link rel="stylesheet" href="{{ asset('css/app.css') }}">

    <title>Admin | GestProj - @yield('title')</title>
</head>
<body>

@if(session()->has('toaster'))

    @include(session()->get('toaster')->getTemplate(), ['toast' => session()->get('toaster')])

@endif

@yield('content')

<!-- BOOTSTRAP JS -->

<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.27.2/axios.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
<script
    src="https://code.jquery.com/jquery-3.6.0.min.js"
    integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4="
    crossorigin="anonymous"></script>
<script src="https://cdn.datatables.net/1.12.0/js/jquery.dataTables.min.js"></script>
<script src="https://unpkg.com/set-interval-async"></script>
<!-- VENDOR JS -->

<script>

    window.cardinal = {
        "internal": "/internal"
    };

</script>

@yield('cardinalJS')

<script src="{{ asset('js/app.js') }}"></script>

@yield('scripts')

</body>
</html>
