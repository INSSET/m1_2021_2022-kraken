<template>

  <ul class="breadcrumb-content">

    <slot />

  </ul>

</template>

<script>
export default {
  name: "BreadcrumbComponent"
}
</script>

<style lang="scss">
  @import "@/assets/components/breadcrumb.scss";
</style>
