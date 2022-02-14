<template>
  <v-app>
    <v-app-bar
      app
      color="white"
      dark
      flat
    >
      <v-spacer></v-spacer>
      <v-btn color="white" text>
        <router-link to="/" class="text-decoration-none">Users List</router-link>
      </v-btn>
      <v-btn color="white" text>
        <router-link to="/groups" class="text-decoration-none">Group List</router-link>
      </v-btn>
      <v-btn color="white" class="red--text" @click="logout" rounded>Log out</v-btn>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),

  methods: {
    logout() {
    },
  },

};
</script>
