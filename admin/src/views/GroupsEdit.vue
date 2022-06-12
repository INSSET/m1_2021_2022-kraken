<template>
  <v-container>
    <h1 class="d-flex">
      <span>Groupe :</span>
      <v-form class="pl-3" @submit="renameGroup(group.id, group.name)">
        <v-text-field v-model="group.name" :disabled="disabled == 1"></v-text-field>
      </v-form>
      <v-btn class="ml-4" icon="mdi-pencil" @click="disabled = (disabled + 1) % 2"></v-btn>
    </h1>
    <div class="ma-2" v-if="msgError != ''" >
      <v-icon
        color="red"
      >
        mdi-alert-circle-outline
      </v-icon>
      {{ msgError }}
    </div>
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
          v-for="(user,i) in group.users"
          :key="i"
      >
        <td>{{ user.name }}</td>
        <td>
          <v-btn size="small" class="float-right" flat icon=mdi-minus @click="deleteUser(user.name)"></v-btn>
        </td>
      </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script>
import { updateGroupName } from '../utils/requests'
export default {
  computed: {
    group() {
      return this.$store.state.groups.find(group => group.id == this.$route.params.group_id)
    },
    msgError() {
      return this.$store.state.msgErrorUpdateGroupName
    }
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
    renameGroup: function (group_id, group_name) {
      updateGroupName(group_id, group_name)
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
