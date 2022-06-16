<?php

namespace App\Entity;

class Container
{
    private string $id;
    private string $image;
    private string $name;
    private string $status;
    private string $containerName;

    /**
     * @param int $id
     * @param string $image
     * @param string $name
     * @param string $status
     * @param string $containerName
     */
    public function __construct(string $id, string $image, string $name, string $status, string $containerName)
    {
        $this->id = $id;
        $this->image = $image;
        $this->name = $name;
        $this->status = $status;
        $this->containerName = $containerName;
    }

    /**
     * @return int
     */
    public function getId(): string
    {
        return $this->id;
    }

    /**
     * @param int $id
     */
    public function setId(string $id): void
    {
        $this->id = $id;
    }

    /**
     * @return string
     */
    public function getImage(): string
    {
        return $this->image;
    }

    /**
     * @param string $image
     */
    public function setImage(string $image): void
    {
        $this->image = $image;
    }

    /**
     * @return string
     */
    public function getName(): string
    {
        return $this->name;
    }

    /**
     * @param string $name
     */
    public function setName(string $name): void
    {
        $this->name = $name;
    }

    /**
     * @return string
     */
    public function getStatus(): string
    {
        return $this->status;
    }

    /**
     * @param string $status
     */
    public function setStatus(string $status): void
    {
        $this->status = $status;
    }

    /**
     * @return string
     */
    public function getContainerName(): string
    {
        return $this->containerName;
    }

    /**
     * @param string $containerName
     */
    public function setContainerName(string $containerName): void
    {
        $this->containerName = $containerName;
    }


}
