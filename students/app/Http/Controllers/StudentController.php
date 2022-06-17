<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Services\API\StudentService;
use Illuminate\Http\Request;
use JsonException;
use Throwable;

class StudentController extends Controller
{
    public function __construct(
        private StudentService $studentService
    )
    {
    }

    /**
     * @throws JsonException
     */
    public function show(string $student)
    {

        $student = $this->studentService->findOneByName($student);

        if (null === $student) {
            abort(404);
        }

        $sshKeys = $this->studentService->getSshStudentKey($student->getId());

        return view('ssh.show', [
            'student' => $student,
            'sshKeys' => $sshKeys
        ]);

    }

    public function uploadSshKey(Request $request, int $id)
    {

        $key = $request->input('ssh');

        if ('' === $key || ' ' === $key) {
            return redirect()->back();
        }

        try {
            $this->studentService->uploadSshKey($key, $id);
        } catch (Throwable $exception) {
            return redirect()->back();
        }

        return redirect()->back();

    }

    public function show_containers(string $student)
    {
        $student = $this->studentService->findOneByName($student);

        if (null === $student) {
            abort(404);
        }

        $containers = $this->studentService->getContainers($student->getId());

        return view('containers.index', [
            'student' => $student,
            'containers' => $containers
        ]);
    }

    public function sendContainerCommand(int $id, string $action) {

        $this->studentService->sendContainerAction($id, $action);
        return redirect()->back();

    }
}
