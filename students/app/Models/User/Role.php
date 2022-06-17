<?php

namespace App\Models\User;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Role extends Model
{
    use HasFactory;

    /**
     * Return role's permissions and merge with is parented
     *
     * @return array
     */
    public function allPermissions(): array
    {
        $ownPermissions = $this->permissions;

        $parentPermissions = [];

        if($this->parent !== null) {
            $parentPermissions = collect($this->parent->permissions);
        }

        return collect($ownPermissions)->merge($parentPermissions)->all();
    }

    /**
     * @param Permission|string $permission
     * @return bool
     */
    public function hasPermission(Permission|string $permission): bool
    {
        if($permission instanceof Permission) {
            $permission = $permission->label;
        }

        $permissionLabel = $permission;

        return $this->permissions->contains(function ($permission) use ($permissionLabel) {
            return $permission->label === $permissionLabel;
        });

    }

    /**
     * Return all role's permissions
     *
     * @return BelongsToMany
     */
    public function permissions(): BelongsToMany
    {
        return $this->belongsToMany(Permission::class);
    }

    /**
     * Return parented role
     *
     * @return BelongsTo
     */
    public function parent(): BelongsTo
    {
        return $this->belongsTo(Role::class, 'parent_id');
    }

    /**
     * @return HasMany
     */
    public function users(): HasMany
    {

        return $this->hasMany(User::class);

    }

    public function getSubordinate() {

        return self::where('rank', '<', $this->rank)->first();

    }

}
