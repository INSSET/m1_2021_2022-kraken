<template>
  
</template>

<script>
export default {
  name: "Input",
  props: {
      name: {
        type: String,
        required: true
      },
      label: {
        type: String,
        required: true
      },
      type: {
        type: String,
        required: true
      },
      value: {
        type: String,
        required: false
      },
      placeholder: {
        type: String,
        required: false
      }
  },
  computed: {
    model: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit('value', value);
      },
    },
  },
  methods: {
    onInput(event) {
      // Can add validation here
      this.$emit('input', event.target.value);
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/components/form/input.scss";
</style>
