<template>

  <section class="topbar">

    <a href="#">
      <i class="fa-duotone fa-gear"></i>
    </a>

    <a href="#">
      <i class="fa-duotone fa-arrow-right-from-bracket"></i>
    </a>

    <div class="user-profile">
      <div class="user-profile-informations">
        <img src="https://pfpmaker.com/_nuxt/img/profile-3-1.3e702c5.png" alt="Profile" title="Profile" width="40">
      </div>
    </div>

  </section>


</template>

<script>
export default {
  name: "HeaderComponent"
}
</script>

<style scoped lang="scss">
  @import "@/assets/components/layouts/header.scss";
</style>
