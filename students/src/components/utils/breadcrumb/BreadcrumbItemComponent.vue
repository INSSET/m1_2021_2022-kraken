<template>

  <li class="breadcrumb-item">
    <router-link :to="{ path: '/' }">{{ label }}</router-link>
  </li>

</template>

<script>
export default {
  name: "BreadcrumbItemComponent",
  props: {
    route: {
      type: Object,
      required: true
    },
    label: {
      type: String,
      required: true
    }
  }
}
</script>
