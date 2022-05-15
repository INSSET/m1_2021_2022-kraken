<template>

  <form @submit="checkForm" method="post">

    <div class="form-group">
      <label for="login">
        Identifiant
      </label>
      <input class="form-control" type="text" id="login" name="login" placeholder="Identifiant">
    </div>

    <div class="form-group">
      <label for="password">
        Mot de passe
      </label>
      <input class="form-control" type="password" id="password" name="password" placeholder="*******">
    </div>

    <div class="d-flex justify-content-between">

      <div class="form-check">
        <input class="form-check-input" type="checkbox" value="" id="stayLogged">
        <label class="form-check-label" for="stayLogged">
          Rester connecté
        </label>
      </div>

      <router-link class="forgot-password" :to="{ path: '#'}">
        Mot de passe oublié
      </router-link>

    </div>


    <button type="submit" class="mt-4 big-button">Valider</button>

  </form>

</template>

<script>
export default {
  name: "AuthFormComponent",
  methods: {
    checkForm: (event) => {
      console.log("e")
      event.preventDefault();
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/components/input.scss";
@import "@/assets/components/button.scss";
</style>
