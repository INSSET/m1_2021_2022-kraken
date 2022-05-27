<template>
    <v-container>
        <v-btn class="bg-deep-purple" :to="'/groups/add'" >
            <v-icon large class="mr-1">
                mdi-plus
            </v-icon>
            Ajouter un groupe
        </v-btn>
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
                    :key="group.group_id"
                >
                    <td>{{ group.group_name }}</td>
                    <td class="text-right" >
                        <v-btn class="mx-4" size="small" :to="'/groups/'+group.group_id" icon="mdi-magnify" ></v-btn>
                        <v-btn size="small" :to="'/groupsEdit/'+group.group_id" icon="mdi-pencil" ></v-btn>
                    </td>
                </tr>
            </tbody>
        </v-table>
    </v-container>
</template>

<script>
import { mapState } from 'vuex';
import { getGroups } from '../utils/requests'
export default {
    data () {
        return {
            
        }
    },
    computed: mapState({
        groups: 'groups',
    }),
    mounted() {
        getGroups()
    }
}
</script>