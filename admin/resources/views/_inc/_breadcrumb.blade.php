<ul class="breadcrumb-content">

    @foreach(\App\Services\Breadcrumb::getList() as $breadcrumbItem)

        @if($breadcrumbItem->hasParameters())

            <li class="breadcrumb-item">
                <a href="{{ route($breadcrumbItem->getRouteName(), $breadcrumbItem->getParameters()) }}">{{ ucfirst(__($breadcrumbItem->getLastParameterValue())) }}</a>
            </li>

        @else

            @if(\Illuminate\Support\Facades\Route::has($breadcrumbItem->getRouteName()))
                <li class="breadcrumb-item">
                    <a href="{{ route($breadcrumbItem->getRouteName()) }}">{{ ucfirst(__($breadcrumbItem->getRouteName())) }}</a>
                </li>
            @else
                <li class="breadcrumb-item">
                    <a href="javascript:void(0)">{{ ucfirst(__($breadcrumbItem->getRouteName())) }}</a>
                </li>
            @endif

        @endif

    @endforeach

</ul>
