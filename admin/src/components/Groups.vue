<template>
  <v-container fluid>

    <v-data-iterator
        :items="groups"
        :search="search"
        hide-default-footer
    >
      <template>
        <v-row>
          <v-col
              v-for="group in groups"
              :key="group.group_id"
              cols="12"
              sm="6"
              md="4"
              lg="4"
          >
            <v-card>
              <v-card-title class="subheading font-weight-bold">
                {{ group.group_name }}
                <v-spacer></v-spacer>
                {{ group.group_id }}
              </v-card-title>

              <v-divider></v-divider>

              <v-list dense v-for="user in group.users_name" :key="user.group_id">
                <v-list-item>
                  <v-list-item-content class="align-end">
                    {{ user }}
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>
    <v-snackbar v-model="snackbar" :timeout="3000" :color="snackbarColor">
      {{ snackbarText }}
      <template v-slot:action="{ attrs }">
        <v-btn
            text
            v-bind="attrs"
            @click="snackbar = false"
        >
          <v-icon>
            mdi-close
          </v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import api from "@/config/api";

export default {
  name: 'Groups',

  data: () => ({
    groups: [],
    search: '',
    snackbar: false,
    snackbarText: '',
    snackbarColor: '',
  }),
  methods: {
    async getGroups() {
      await api()
          .get(process.env.VUE_APP_GET_GROUPS, {
            headers: {
              'Authorization': `Bearer ${this.$store.state.token.token}`
            }
          })
          .then(response => {
            this.groups = response.data
          })
          .catch(error => {
            if (error.response && error.response.status === 401) {
              this.snackbar = true
              this.snackbarColor = 'error'
              this.snackbarText = error.response.data.description
            }
          })
    },
  },
  created() {
    this.getGroups()
  }
}
</script>
