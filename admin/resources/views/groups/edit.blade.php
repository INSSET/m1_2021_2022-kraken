@extends('_inc._wrapper')

@section('title', 'Edition du groupe ', $group->getName())

@section('wrapper')

    <div class="row">

        <div class="col-12">

            <div class="card">

                <div class="row">

                    <div class="col-12">

                        <form class="mb-4" method="post" action="{{ route(\App\Helpers\RoutesDefinition::GROUPS_UPDATE_NAME, ['groupId' => $group->getId()]) }}">

                            @csrf

                            <div class="row">

                                <div class="col-12 col-md-3">

                                    <div class="form-group">

                                        <label for="name">Nom</label>
                                        <div class="btn-grouped">
                                            <input class="form-control" type="text" id="name" name="name" value="{{ $group->getName() }}">
                                            <button type="submit" class="btn btn-primary"><i class="fa-duotone fa-check"></i></button>
                                        </div>

                                    </div>

                                </div>

                            </div>

                        </form>

                    </div>

                </div>

                <div class="row">

                    <div class="col-12">

                        @if(!isset($group->getStudents()[0]))

                            <h4 class="text-center">Aucun étudiant n'a été trouvé.</h4>

                        @else

                            <table class="table table-centered mb-0">
                                <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Nom</th>
                                    <th>Action</th>
                                </tr>
                                </thead>
                                <tbody>

                                @foreach($group->getStudents() as $student)

                                    <tr>
                                        <td>{{ $student->getId() }}</td>
                                        <td>{{ $student->getName() }}</td>
                                        <td class="table-action">
                                            <a href="{{ route(\App\Helpers\RoutesDefinition::STUDENT_SHOW_NAME, ['student' => $student->getName()]) }}"><i
                                                    class="fa-duotone fa-pen"></i></a>
                                        </td>
                                    </tr>

                                @endforeach

                                </tbody>
                            </table>

                        @endif

                    </div>

                </div>

            </div>

        </div>

    </div>

@endsection
