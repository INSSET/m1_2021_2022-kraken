<template>

  <div class="card">

    <h4 class="card-title">{{ title }}</h4>

    <slot />

  </div>

</template>

<script>
export default {
  name: "CardComponent",
  props: {
    title: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped lang="scss">
  @import "@/assets/components/card.scss";
</style>
