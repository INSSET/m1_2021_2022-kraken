<?php

namespace App\Entity;

class Student
{
    private int $id;
    private string $name;
    private ?Group $group;

    /**
     * @param int $id
     * @param string $name
     * @param Group|null $group
     */
    public function __construct(int $id, string $name, Group $group = null)
    {
        $this->id = $id;
        $this->name = $name;
        $this->group = $group;
    }

    /**
     * @return int
     */
    public function getId(): int
    {
        return $this->id;
    }

    /**
     * @param int $id
     */
    public function setId(int $id): void
    {
        $this->id = $id;
    }

    /**
     * @return string
     */
    public function getName(): string
    {
        return $this->name;
    }

    public function getFormattedName(): string
    {
        return str_replace('.', ' ', $this->name);
    }

    /**
     * @param string $name
     */
    public function setName(string $name): void
    {
        $this->name = $name;
    }

    /**
     * @return Group|null
     */
    public function getGroup(): ?Group
    {
        return $this->group;
    }

    /**
     * @param Group|null $group
     */
    public function setGroup(?Group $group): void
    {
        $this->group = $group;
    }

}
