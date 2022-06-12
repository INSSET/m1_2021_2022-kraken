<template>
  <v-container>
    <div>
      <v-btn class="bg-deep-purple" :to="'/groups/add'">
        <v-icon large class="mr-1">
          mdi-plus
        </v-icon>
        Ajouter un groupe
      </v-btn>
    </div>
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
        <th class="text-left">
          Nom
        </th>
        <th class="text-right">
          Actions
        </th>
      </tr>
      </thead>
      <tbody>
      <tr
          v-for="group in groups"
          :key="group.id"
      >
        <td>{{ group.name }}</td>
        <td class="text-right">
          <v-btn class="mx-4" size="small" :to="'/groups/'+group.id" icon="mdi-magnify"></v-btn>
          <v-btn size="small" :to="'/groupsEdit/'+group.id" icon="mdi-pencil"></v-btn>
        </td>
      </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script>
import {mapState} from 'vuex';
import GroupService from "@/services/group-service";
import { getGroups } from '../utils/requests';

export default {
  data() {
    return {}
  },
  provide: { GroupService },
  computed: mapState({
    groups: 'groups',
    msgError: 'msgErrorGetGroups',
  }),
  mounted() {
    //GroupService.findAll()
    getGroups()
  }
}
</script>
