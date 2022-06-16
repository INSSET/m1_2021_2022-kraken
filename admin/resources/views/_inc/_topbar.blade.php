<section class="topbar">

    <a href="{{ route(\App\Helpers\RoutesDefinition::LOGOUT_NAME) }}">
        <i class="fa-duotone fa-arrow-right-from-bracket"></i>
    </a>

    <div class="user-profile">
        <div class="user-profile-informations">
            <h5>{{ auth()->user()->name }}</h5>
            <span>{{ ucfirst(__(auth()->user()->role->label))}}</span>
        </div>
    </div>

</section>
