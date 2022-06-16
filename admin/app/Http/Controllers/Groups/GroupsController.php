<?php

namespace App\Http\Controllers\Groups;

use App\Http\Controllers\Controller;
use App\Services\API\GroupsServices;
use GuzzleHttp\Exception\GuzzleException;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\View\Factory;
use Illuminate\Contracts\View\View;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use JsonException;
use Throwable;

class GroupsController extends Controller
{

    public function __construct(
        private GroupsServices $groupsServices
    ){}

    /**
     * @throws GuzzleException
     * @throws JsonException
     */
    public function index(): Factory|View|Application
    {

        $groups = $this->groupsServices->findAll();

        return view('groups.index', [
            'groups' => $groups
        ]);
    }

    /**
     * @throws GuzzleException
     * @throws JsonException
     */
    public function edit(int $groupId): Factory|View|Application
    {

        $group = $this->groupsServices->findOne($groupId);

        if(null === $group) {
            abort(404);
        }

        return view('groups.edit', [
            'group' => $group
        ]);

    }

    /**
     * @throws JsonException
     */
    public function update(Request $request, int $id): RedirectResponse
    {

        $name = $request->except('_token')['name'];

        $this->groupsServices->updateName($id, $name);

        return redirect()->back();

    }

    public function add(Request $request) {

        $name = $request->except('_token')['name'];

        $file = $request->file('file');

        try {
            $this->groupsServices->createByCsv($name, $file);
        } catch (Throwable $exception) {
            return redirect()->back();
        }

        return redirect()->back();

    }

}
