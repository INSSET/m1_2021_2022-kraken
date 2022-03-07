<template>
  <v-container fluid>

    <v-row align="center" justify="center">
      <v-col cols="6">
        <v-card>
          <v-card-title>
            <v-row>
              <v-col cols="4">
                user_name
              </v-col>
              <v-col cols="4">
                user_id
              </v-col>
              <v-col cols="4">
                group_id
              </v-col>
            </v-row>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="4">
                {{ user.user_name }}
              </v-col>
              <v-col cols="4">
                {{ user.user_id }}
              </v-col>
              <v-col cols="4">
                {{ user.group_id }}
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import api from "@/config/api";

export default {
  name: 'UserDetails',
  data: () => ({
    user: []
  }),
  methods: {
    async getUserById() {
      await api()
        .get(process.env.VUE_APP_GET_USER + this.$route.params.id, {
        })
        .then(response => {
          this.user = response.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created() {
    this.getUserById()
  }
}
</script>
