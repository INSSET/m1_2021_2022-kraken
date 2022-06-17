<section class="menu">

    <div class="menu-brand">

        <h3 class="brand-title">GestProj</h3>

    </div>

    <div class="menu-container">

        <div class="menu-section">

            <h6 class="menu-section-title">Etudiants</h6>

            <ul class="menu-section-list">

                <li class="menu-section-item">
                    <a href="{{ route(\App\Helpers\RoutesDefinition::SSH_SHOW_NAME, ['student' => explode("@", auth()->user()->email)[0]]) }}"><i class="fa-duotone fa-folder-open"></i>   Mes Clés</a>
                </li>

            </ul>

        </div>

        <div class="menu-section">

            <h6 class="menu-section-title">VMs</h6>

            <ul class="menu-section-list">

                <li class="menu-section-item">
                    <a href="#"><i class="fa-brands fa-docker"></i>   Dockerfile</a>
                </li>

            </ul>

        </div>

    </div>

</section>
