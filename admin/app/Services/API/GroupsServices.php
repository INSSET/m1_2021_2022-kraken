<?php

namespace App\Services\API;

use App\Entity\Group;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\GuzzleException;
use Illuminate\Http\File;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Collection;
use JsonException;
use RuntimeException;

class GroupsServices
{

    private string $apiEndpoint;

    public function __construct(
        private Client $client,
        private StudentService $studentService
    ){
        $this->apiEndpoint = env('API_BACKEND_HOST');
    }

    /**
     * @throws GuzzleException
     * @throws JsonException
     */
    public function findAll(): Collection
    {
        try {
            $response = $this->client->request('GET', sprintf('%s/groups', $this->apiEndpoint));
        } catch (GuzzleException $e) {
            return new Collection();
        }

        if($response->getStatusCode() !== 200) {
            return new Collection();
        }

        $fetchedGroups = json_decode($response->getBody()->getContents(), true, 512, JSON_THROW_ON_ERROR);

        foreach ($fetchedGroups as $group) {

            $groups[] = $this->mapGroupWithStudents($group);

        }

        return collect($groups);
    }

    /**
     * @throws GuzzleException
     * @throws JsonException
     */
    public function findOne(int $groupId): ?Group
    {
        try {
            $response = $this->client->request('GET', sprintf('%s/groups/%d', $this->apiEndpoint, $groupId));
        } catch (GuzzleException $e) {
            return null;
        }

        if ($response->getStatusCode() !== 200) {
            return null;
        }

        $fetchedGroup = json_decode($response->getBody()->getContents(), true, 512, JSON_THROW_ON_ERROR);

        return $this->mapGroupWithStudents($fetchedGroup);

    }

    /**
     * @throws JsonException
     */
    public function updateName(int $groupId, string $name): void
    {

        try {
            $this->client->request('PATCH', sprintf('%s/groups/%d', $this->apiEndpoint, $groupId), [
                'body' => json_encode(['groupName' => $name], JSON_THROW_ON_ERROR),
                'headers' => ['Content-Type' => 'application/json', 'Accept' => 'application/json'],
            ]);
        } catch (GuzzleException $e) {}

    }

    /**
     * @param mixed $group
     * @return Group
     * @throws JsonException
     */
    private function mapGroupWithStudents(mixed $group): Group
    {
        $groupStudents = [];

        foreach ($group['users_names'] as $studentName) {

            $fetchedStudent = $this->studentService->findOneByName($studentName);

            if (null !== $fetchedStudent) {
                $groupStudents[] = $fetchedStudent;
            }

        }

        return new Group(
            $group['group_id'],
            $group['group_name'],
            $groupStudents
        );
    }

    public function createByCsv(string $name, UploadedFile $file): void
    {
        try {
            $this->client->request('POST', sprintf('%s/groups/%s/upload', $this->apiEndpoint, $name), [
                'form_params' => ['file' => $file->getRealPath()],
            ]);
        } catch (GuzzleException $e) {}
    }

}
