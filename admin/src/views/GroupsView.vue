<template>
    <v-container>
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
                        <v-btn size="small" to="/about" icon="mdi-pencil" ></v-btn>
                    </td>
                </tr>
            </tbody>
        </v-table>
    </v-container>
</template>

<script>
import { mapState } from 'vuex';
export default {
    data () {
        return {
            
        }
    },
    computed: mapState({
        groups: 'groups',
    })
}
</script>