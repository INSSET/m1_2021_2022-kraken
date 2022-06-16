<?php

namespace App\Services\Breadcrumb;

use App\Helpers\RoutesDefinition;
use Illuminate\Support\Facades\Route;
use RuntimeException;

final class BreadcrumbItem
{

    /**
     * @var string
     */
    private string $routeName;

    /**
     * @var array
     */
    private array $parameters;

    /**
     * @var BreadcrumbItem
     */
    private BreadcrumbItem $parent;

    /**
     * @param string $routeName
     * @param array $parameters
     */
    public function __construct(string $routeName, array $parameters = [])
    {
        $this->routeName = $routeName;
        $this->parameters = $parameters;
    }

    /**
     * @return string
     */
    public function getRouteName(): string
    {
        return $this->routeName;
    }

    /**
     * @param string $routeName
     */
    public function setRouteName(string $routeName): void
    {
        $this->routeName = $routeName;
    }

    /**
     * @return array
     */
    public function getParameters(): array
    {
        return $this->parameters;
    }

    /**
     * @param array $parameters
     */
    public function setParameters(array $parameters): void
    {
        $this->parameters = $parameters;
    }

    /**
     * @return bool
     */
    public function hasParameters(): bool
    {
        return !empty($this->parameters);
    }

    /**
     * @return BreadcrumbItem|null
     */
    public function getParent(): ?BreadcrumbItem
    {
        return $this->parent;
    }

    /**
     * @param BreadcrumbItem $parent
     */
    public function setParent(BreadcrumbItem $parent): void
    {
        $this->parent = $parent;

        $this->setRouteName($this->parent->getRouteName() . '.' . $this->getRouteName());

    }

    /**
     * @return bool
     */
    public function hasParent(): bool
    {
        return $this->parent !== null;
    }

    /**
     * @return mixed
     * @throws RuntimeException
     */
    public function getLastParameterValue(): mixed {

        if(!$this->hasParameters()) {
            throw new RuntimeException('Can\'t retrieve last parameter when list is null.');
        }

        return end($this->parameters);

    }

}
