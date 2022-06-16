@extends('_inc._wrapper')

@section('title', 'Liste des groupes')

@section('wrapper')

    <div class="row">

        <div class="col-12">

            <div class="card">

                <h4 class="card-title">Liste des groupes</h4>

                <div class="row">

                    <div class="col-12">

                        @if(!isset($groups[0]))

                            <h4 class="text-center">Aucun groupe n'a été trouvé.</h4>

                        @else

                            <table class="table table-centered mb-0">
                                <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Nom</th>
                                    <th>Nombre d'étudiants</th>
                                    <th>Action</th>
                                </tr>
                                </thead>
                                <tbody>

                                @foreach($groups as $group)

                                    <tr>
                                        <td>{{ $group->getId() }}</td>
                                        <td>{{ $group->getName() }}</td>
                                        <td>{{ count($group->getStudents()) }}</td>
                                        <td class="table-action">
                                            <a href="{{ route(\App\Helpers\RoutesDefinition::GROUPS_EDIT_NAME, ['groupId' => $group->getId()]) }}"><i
                                                    class="fa-duotone fa-pen"></i></a>
                                        </td>
                                    </tr>

                                @endforeach

                                </tbody>
                            </table>

                        @endif

                    </div>

                    <div class="col-12 mt-4">

                        <form method="post" action="{{ route(\App\Helpers\RoutesDefinition::GROUPS_ADD_NAME) }}" enctype="multipart/form-data">

                            @csrf

                            <div class="row">

                                <div class="col-12 col-md-4">
                                    <div class="form-group">

                                        <label for="name">Nom du groupe</label>
                                        <input class="form-control" type="text" name="name" id="name" placeholder="L1">

                                    </div>
                                </div>

                                <div class="col-12 col-md-4">
                                    <div class="form-group">

                                        <label for="file">Fichier</label>
                                        <input class="form-control" type="file" name="file" id="file">

                                    </div>
                                </div>

                                <div class="col-12">
                                    <div class="form-group mt-3">
                                        <button type="submit" class="btn btn-primary">Enregistrer</button>
                                    </div>
                                </div>

                            </div>

                        </form>

                    </div>

                </div>

            </div>

        </div>

    </div>

@endsection
