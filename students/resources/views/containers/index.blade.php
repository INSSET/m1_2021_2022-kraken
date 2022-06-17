@extends('_inc._wrapper')

@section('title', 'Containers de ' . $student->getName())

@section('wrapper')

<div class="col-12">

    <div class="card">

        <h4 class="card-title">Containers de {{ $student->getFormattedName() }}</h4>

        @if($containers->count() < 1)

            <h6 class="text-center">Aucuns conteneur n'est lancé.</h6>

        @else

            <div class="row">

                @foreach($containers as $container)

                    <div class="col-12 col-md-3">

                        <div class="vm-container">

                            <h4 class="vm-name">{{ $container->getContainerName() }}</h4>

                            <div class="vm-body">

                                <div class="vm-item">
                                    <span>Status</span>
                                    <span class="vm-status {{ $container->getStatus() }}"><small>{{ $container->getStatus() }}</small></span>
                                </div>

                                <div class="vm-item">
                                    <span>Version</span>
                                    <strong class="vm-version">{{ $container->getId() }}</strong>
                                </div>

                                <div class="vm-item">
                                    <span>Lien</span>
                                    <a href="#" target="_blank">LIEN</a>
                                </div>

                                <div class="vm-item">
                                    <span>Actions</span>
                                    <div class="vm-actions">
                                        <a href="{{ route(\App\Helpers\RoutesDefinition::STUDENT_SEND_ACTION_NAME, ['student' => $student->getId(), 'action' => 'up']) }}" class="vm-apply up" title="Démarrer"><i class="fa-duotone fa-play"></i></a>
                                        <a href="{{ route(\App\Helpers\RoutesDefinition::STUDENT_SEND_ACTION_NAME, ['student' => $student->getId(), 'action' => 'down']) }}" class="vm-apply stop" title="Stopper"><i class="fa-duotone fa-stop"></i></a>
                                        <a href="{{ route(\App\Helpers\RoutesDefinition::STUDENT_SEND_ACTION_NAME, ['student' => $student->getId(), 'action' => 'restart']) }}" class="vm-apply unknown" title="Redémarrer"><i class="fa-duotone fa-repeat"></i></a>
                                        <a class="vm-apply" title="Logs"><i class="fa-duotone fa-list"></i></a>
                                    </div>
                                </div>

                            </div>

                        </div>

                    </div>

                @endforeach

            </div>

        @endif

    </div>

</div>
@endsection