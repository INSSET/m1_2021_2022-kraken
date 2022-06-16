<?php

namespace App\Models\User;

use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Collection;

trait HasPermission
{

    /**
     * @return BelongsTo
     */
    public function role()
    {

        return $this->belongsTo(Role::class);

    }

    /**
     * @param string|Role $role
     * @return bool
     */
    public function hasRole(string | Role $role): bool
    {

        if(is_string($role)) {

            $role = Role::where(['label' => $role])->first();

        }

        return $this->role === $role;

    }

    /**
     * @return Collection
     */
    public function getPermissions(): Collection
    {

        return collect($this->role->allPermissions());

    }

    /**
     * @param string $permission
     * @return bool
     */
    public function hasPermission(string $permission): bool
    {

        if ($this->role->can_bypass == true) {
            return true;
        }

        $permissionsArray = $this->getPermissions()->map(function ($value, $key) use ($permission) {

            return $value->label === $permission;

        });

        return $permissionsArray->contains(true);

    }

    /**
     * @param string|Role $role
     * @return void
     */
    public function setRole(string | Role $role) {
        if(is_string($role)) {

            $role = Role::where(['label' => $role])->first();

        }
        $this->role_id = $role->id;
        $this->save();

    }



}
