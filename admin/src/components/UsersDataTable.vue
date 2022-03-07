<template>
  <v-container>

    <v-row>
      <v-col cols="4">
        <v-select
            v-model="search"
            :items="users"
            item-text="group_id"
            item-value="group_id"
            label="Filter by group"
            clearable
        ></v-select>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="4">
        <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
            clearable
        ></v-text-field>
      </v-col>
    </v-row>

    <v-data-table
        :headers="headers"
        :items="users"
        :search="search"
        class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar
            flat
        >
          <v-toolbar-title>Users List</v-toolbar-title>
          <v-divider
              class="mx-4"
              inset
              vertical
          ></v-divider>
          <v-spacer></v-spacer>
        </v-toolbar>
      </template>
      <template v-slot:top>
        <v-dialog v-model="dialog" max-width="800px">
          <v-card>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                        v-model="editedUser.user_id"
                        label="User ID"
                    />
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                        v-model="editedUser.user_name"
                        label="User Name"
                    />
                  </v-col>
                  <v-col cols="12" sm="6" md="3">
                    <v-text-field
                        v-model="editedUser.group_id"
                        label="User Group ID"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="getUserDetails(editedUser)">Afficher plus de détails</v-btn>
              <v-btn color="red darken-1" text @click="dialog = false">Annuler</v-btn>
              <v-btn
                  color="blue darken-1"
                  text
                  @click="save(editedUser)"
              >Modifier</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="headline">Are you sure you want to delete user : <span>{{ editedUser.user_name }} ?</span></v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDeleteDialog">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="deleteUser(editedUser.user_id)">Delete</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
            small
            class="mr-2"
            @click="editUser(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
            small
            @click="showDeleteDialog(item)"
        >
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
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
import router from "@/router";

export default {
  name: 'Users',

  data: () => ({
    headers: [
      {
        text: 'User Name', value: 'user_name'
      },
      {
        text: 'User ID', value: 'user_id'
      },
      {
        text: 'Group ID', value: 'group_id'
      },
      {
        text: '', value: 'actions', sortable: false
      }
    ],
    users: [],
    search: '',
    filterByGroup: '',
    dialog: false,
    dialogDelete: false,
    editedIndex: -1,
    editedUser: {
      user_id: '',
      user_name: '',
      group_id: ''
    },
    defaultUser: {
      uid: '',
      name: '',
      gid: ''
    },
    tokenType: '',
    snackbar: false,
    snackbarText: '',
    snackbarColor: '',
  }),

  methods: {
    async getUsers() {
      await api()
          .get(process.env.VUE_APP_GET_USERS, {
          })
          .then(response => {
            this.users = response.data
          })
          .catch(error => {
            if (error.response && error.response.status === 401) {
              this.snackbar = true
              this.snackbarColor = 'error'
              this.snackbarText = error.response.data.description
            }
          })
    },
    getUserDetails(editedUser) {
      router.push({ name: 'UserDetails', params: { id: editedUser.user_id } })
    },
    editUser (item) {
      this.editedIndex = this.users.indexOf(item)
      this.editedUser = Object.assign({}, item)
      this.dialog = true
    },
    save (item) {
      if (this.editedIndex > -1) {
        this.snackbar = true
        this.snackbarColor = 'success'
        this.snackbarText = item.user_name.replace('.', ' ') + " data has been updated"
        Object.assign(this.users[this.editedIndex], this.editedUser.user_id)
      } else {
        this.snackbar = true
        this.snackbarColor = 'error'
        this.snackbarText = 'Something went wrong'
        this.users.push(this.editedUser)
      }
      this.close()
    },
    deleteUser (item) {
      api()
        .get(process.env.VUE_APP_GET_USER + item)
        .then(response => {
          this.snackbar = true
          this.snackbarColor = 'success'
          this.snackbarText = response.data
        })
        .catch(error => {
          this.snackbar = true
          this.snackbarColor = 'error'
          this.snackbarText = error
        })
        this.editedIndex = this.users.indexOf(item)
        this.editedUser = Object.assign({}, item)
        this.dialogDelete = false
    },
    showDeleteDialog(item) {
      this.editedIndex = this.users.indexOf(item)
      this.editedUser = Object.assign({}, item)
      this.dialogDelete = true
    },
    closeDeleteDialog () {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedUser = Object.assign({}, this.defaultUser)
        this.editedIndex = -1
      })
    },
    close () {
      this.dialog = false
      this.$nextTick(() => {
        this.editedUser = Object.assign({}, this.defaultUser)
        this.editedIndex = -1
      })
    },
  },

  mounted() {
    this.getUsers();
  }
}
</script>
