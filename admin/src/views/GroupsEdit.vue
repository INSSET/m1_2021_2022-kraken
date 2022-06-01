<template>
  <v-container>
    <h1 class="d-flex">
      <span>Groupe :</span>
      <v-form class="pl-3" @submit="renameGroup(group.group_id)">
        <v-text-field v-model="group.group_name" :disabled="disabled == 1"></v-text-field>
      </v-form>
      <v-btn class="ml-4" icon="mdi-pencil" @click="disabled = (disabled + 1) % 2"></v-btn>
    </h1>
    <v-table>
      <thead>
      <tr>
        <th>
          Name
        </th>
      </tr>
      </thead>
      <tbody>
      <tr
          v-for="(user,i) in group.users_names"
          :key="i"
      >
        <td>{{ user }}</td>
        <td>
          <v-btn size="small" class="float-right" flat icon=mdi-minus @click="deleteUser(user.users_names)"></v-btn>
        </td>
      </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script>
export default {
  computed: {
    group() {
      return this.$store.state.groups.find(group => group.group_id == this.$route.params.group_id)
    },
  },
  data() {
    return {
      disabled: 1
    }
  },
  methods: {
    deleteUser: function (user_name) {
      fetch("0.0.0.0:5000/", {
        "method": "DELETE"
      })
    },
    renameGroup: function (group_id) {
      fetch("0.0.0.0:5000/api/v1/students/" + group_id, {
        "method": "PATCH"
      })
      this.disabled = 1
    }
  }
}
</script>

<style>
.inputNameGroup {
  width: 400px;
}

.v-field__input input[disabled]::placeholder {
  color: black;
}

.v-form {
  width: 50%;
}

h1 {
  width: 100%;
}

.v-input__details {
  display: none !important;
}

.v-field__field {
  padding-top: 0 !important;
}
</style>
