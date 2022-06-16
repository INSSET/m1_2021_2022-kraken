@extends('_inc._wrapper')

@section('title', 'Profil de ' . $student->getName())

@section('wrapper')

    <div class="row">

        <div class="col-12">

            <div class="card">

                <h4 class="card-title">Profil de {{ $student->getFormattedName() }}</h4>

                <div class="row">

                    <div class="col-12 col-md-6">

                        <div class="sub-card">

                            <ul>
                                <li><strong>ID</strong> : {{ strtolower($student->getId()) }}</li>
                                <li><strong>Login</strong> : {{ strtolower($student->getName()) }}</li>
                                <li><strong>Groupe</strong> : {{ $student->getGroup()->getName() }}</li>
                            </ul>

                        </div>

                    </div>

                    <div class="col-12 col-md-6">

                        <div class="sub-card">

                            @if($sshKeys->count() < 1)

                                <h6 class="text-center">Aucune clé ssh n'a été enregistré pour cet étudiant.</h6>
                                <hr>

                            @else
                                @foreach($sshKeys as $sshKey)

                                    <p>{{ $sshKey }}</p>
                                    <hr>

                                @endforeach
                            @endif

                            <form method="post"
                                  action="{{ route(\App\Helpers\RoutesDefinition::STUDENT_ADD_KEY_NAME, ['student' => $student->getId()]) }}">

                                @csrf

                                <div class="form-group">
                                    <label for="ssh">Nouvelle clé SSH</label>
                                    <textarea class="form-control" id="ssh" name="ssh"
                                              placeholder="ssh-rsa AAAA...."></textarea>
                                </div>

                                <div class="form-group mt-3">
                                    <button class="btn btn-primary" type="submit">Ajouter</button>
                                </div>

                            </form>

                        </div>

                    </div>

                </div>

            </div>

        </div>

        <div class="col-12">

            <div class="card">

                <h4 class="card-title">Containers de {{ $student->getFormattedName() }}</h4>

                @if($containers->count() < 1)

                    <h6 class="text-center">Aucuns containers ne sont lancés.</h6>

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

    </div>

@endsection
