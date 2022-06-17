<section class="topbar">

    <a href="#">
        <i class="fa-duotone fa-gear"></i>
    </a>

    <a href="{{ route(\App\Helpers\RoutesDefinition::LOGOUT_NAME) }}">
        <i class="fa-duotone fa-arrow-right-from-bracket"></i>
    </a>

    <div class="user-profile">
        <img src="https://minotar.net/avatar/{{ auth()->user()->name }}/40" width="40" alt="{{ auth()->user()->name }}" title="{{ auth()->user()->name }}" class="img-fluid">
        <div class="user-profile-informations">
            <h5>{{ auth()->user()->name }}</h5>
        </div>
    </div>

</section>
