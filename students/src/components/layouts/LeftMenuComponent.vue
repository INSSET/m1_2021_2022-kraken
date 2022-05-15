<template>

  <section class="menu">

    <div class="menu-brand">

      <router-link :to="{ name: 'root' }" class="menu-title">eSpace</router-link>

    </div>

    <div class="menu-container">

      <div class="menu-section">

        <h6 class="menu-section-title">Mon espace virtuel</h6>

        <ul class="menu-section-list">

          <li class="menu-section-item">
            <router-link :to="{ name: 'ssh' }"><i class="fa-duotone fa-key"></i>   Mes clé SSH</router-link>
          </li>

          <li class="menu-section-item">
            <a href="#"><i class="fa-duotone fa-lock"></i>   Mes identifiants</a>
          </li>

          <li class="menu-section-item">
            <router-link :to="{ name: 'vm' }"><i class="fa-duotone fa-computer-classic"></i>   Ma VM</router-link>
          </li>

        </ul>

      </div>

    </div>

  </section>


</template>

<script>
export default {
  name: "LeftMenuComponent"
}
</script>

<style scoped lang="scss">
  @import "@/assets/components/layouts/menu.scss";
</style>
