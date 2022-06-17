@extends('_inc._wrapper')

@section('title', 'Clés SSH de ' . $student->getName())

@section('wrapper')


<div class="row">

<div class="col-12">

    <div class="card">

        <h4 class="card-title">Clés SSH de de {{ $student->getFormattedName() }}</h4>

        <div class="row">

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
                          action="{{ route(\App\Helpers\RoutesDefinition::SSH_ADD_KEY_NAME, ['student' => $student->getId()]) }}">

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