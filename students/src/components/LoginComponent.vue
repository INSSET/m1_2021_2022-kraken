<template>

  <section class="auth-container">

    <div class="auth-content">

      <div class="auth-form">

        <div class="auth-title">
          <hr>
          <h6>Students</h6>
          <hr>
        </div>

        <AuthFormComponent />

      </div>

    </div>

  </section>


</template>

<script>
import AuthFormComponent from "@/components/form/AuthFormComponent.vue";
export default {
  name: "LoginComponent",
  components: {AuthFormComponent}
}
</script>

<style lang="scss">
  @import "@/assets/components/auth.scss";
</style>
