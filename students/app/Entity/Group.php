<?php

namespace App\Entity;

class Group
{
    private int $id;
    private string $name;
    /** @var Student[] $students */
    private array $students;

    /**
     * @param int $id
     * @param string $name
     * @param array $students
     */
    public function __construct(int $id, string $name, array $students = [])
    {
        $this->id = $id;
        $this->name = $name;
        $this->students = $students;
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

    /**
     * @param string $name
     */
    public function setName(string $name): void
    {
        $this->name = $name;
    }

    /**
     * @return Student[]
     */
    public function getStudents(): array
    {
        return $this->students;
    }

    /**
     * @param Student[] $students
     */
    public function setStudents(array $students): void
    {
        $this->students = $students;
    }

}
