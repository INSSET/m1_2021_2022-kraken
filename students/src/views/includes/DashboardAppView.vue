<template>

  <main>

    <LeftMenuComponent />

    <section class="wrapper">

      <HeaderComponent />

      <div class="wrapper-content">

        <slot />

      </div>

    </section>

  </main>


</template>

<script>

import LeftMenuComponent from "../../components/layouts/LeftMenuComponent.vue";
import HeaderComponent from "../../components/layouts/HeaderComponent.vue";

export default {
  name: "DashboardAppView",
  components: {LeftMenuComponent, HeaderComponent}
}
</script>

<style scoped lang="scss">
@import "@/assets/components/layouts/wrapper.scss";
</style>
