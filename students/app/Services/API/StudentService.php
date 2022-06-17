<?php

namespace App\Services\API;

use App\Entity\Container;
use App\Entity\Group;
use App\Entity\Student;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\GuzzleException;
use Illuminate\Support\Collection;
use JsonException;

class StudentService
{
    private string $apiEndpoint;

    public function __construct(
        private Client $client
    ){
        $this->apiEndpoint = env('API_BACKEND_HOST');
    }

    /**
     * @throws JsonException
     */
    public function findOneByName(string $name): ?Student
    {

        try {
            $response = $this->client->request('GET', sprintf('%s/students/%s', $this->apiEndpoint, $name));
        } catch (GuzzleException $e) {
            return null;
        }

        if($response->getStatusCode() !== 200) {
            return null;
        }

        $fetchedStudent = json_decode($response->getBody()->getContents(), true, 512, JSON_THROW_ON_ERROR);

        try {
            $groupResponse = $this->client->request('GET', sprintf('%s/groups/%d', $this->apiEndpoint, $fetchedStudent['group_id']));
            $group = json_decode($groupResponse->getBody()->getContents(), true, 512, JSON_THROW_ON_ERROR);
        } catch (GuzzleException $exception) {
            return null;
        }

        return new Student(
            $fetchedStudent['user_id'],
            $fetchedStudent['user_name'],
            new Group(
                $group['group_id'],
                $group['group_name']
            )
        );

    }

    /**
     * @throws JsonException
     */
    public function getSshStudentKey(int $id): Collection
    {

        try {
            $response = $this->client->request('GET', sprintf('%s/students/%d/keys', $this->apiEndpoint, $id));
        } catch (GuzzleException $e) {
            return collect();
        }

        if($response->getStatusCode() !== 200) {
            return collect();
        }

        return collect(json_decode($response->getBody()->getContents(), true, 512, JSON_THROW_ON_ERROR)['keys']);

    }

    public function uploadSshKey(string $key, int $id) {

        try {
            $this->client->request('POST', sprintf('%s/students/%d/ssh/upload', $this->apiEndpoint, $id), [
                'body' => json_encode(['key' => $key], JSON_THROW_ON_ERROR),
                'headers' => ['Content-Type' => 'application/json', 'Accept' => 'application/json'],
            ]);
        } catch (GuzzleException|JsonException $e) {}

    }

    /**
     * @throws JsonException
     */
    public function getContainers(int $id): Collection
    {
        try {
            $response = $this->client->request('GET', sprintf('%s/students/%d/container/info', $this->apiEndpoint, $id));
        } catch (GuzzleException $e) {
            return collect();
        }

        if($response->getStatusCode() !== 200) {
            return collect();
        }

        return collect([json_decode($response->getBody()->getContents(), true, 512, JSON_THROW_ON_ERROR)])->map(static function ($container) {
            return new Container($container['id'], $container['image'], $container['ports'], $container['status'], $container['containerName']);
        });
    }

    public function sendContainerAction(int $id, string $action): void
    {
        try {
            $this->client->request('POST', sprintf('%s/students/%d/container/command/%s', $this->apiEndpoint, $id, $action));
        } catch (GuzzleException|JsonException $e) {}
    }

}
