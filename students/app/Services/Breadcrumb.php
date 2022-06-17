<?php

namespace App\Services;

use App\Helpers\RoutesDefinition;
use App\Services\Breadcrumb\BreadcrumbItem;
use Illuminate\Support\Facades\Route;

class Breadcrumb
{
    /**
     * @return array|null
     */
    public static function getList(): ?array {

        $currentRouteName = Route::getCurrentRoute()->getName();

        $root = new BreadcrumbItem(RoutesDefinition::ROOT_NAME);

        if($currentRouteName === RoutesDefinition::ROOT_NAME) {
            return [$root];
        }

        $currentRouteName = str_replace(RoutesDefinition::ROOT_NAME . '.', '', $currentRouteName);
        $explodedRouteName = explode('.', $currentRouteName);

        $breadcrumbs = [];

        $breadcrumbs[] = $root;

        $parentIndex = 0;

        foreach ($explodedRouteName as $partialRoute) {

            $breadcrumbItem = new BreadcrumbItem($partialRoute);
            $breadcrumbItem->setParent($breadcrumbs[$parentIndex]);

            $initialRoute = Route::getRoutes()->getByName($breadcrumbItem->getRouteName());

            if($initialRoute !== null && $initialRoute->hasParameters()) {

                $breadcrumbItem->setParameters($initialRoute->originalParameters());

            }

            $breadcrumbs[] = $breadcrumbItem;

            $parentIndex++;

        }

        return $breadcrumbs;

    }
}
