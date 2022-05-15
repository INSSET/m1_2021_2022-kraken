<template>

  <div class="sub-card">

    <slot />

  </div>

</template>

<script>
export default {
  name: "SubCardComponent"
}
</script>

<style scoped lang="scss">
  .sub-card {

    padding: 25px;
    border: 1px solid rgba(map-get($colors, "third"), .1);

  }
</style>
