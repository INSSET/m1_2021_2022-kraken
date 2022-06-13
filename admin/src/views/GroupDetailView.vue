<template>
    <v-container>
        <v-container>
            Nom : {{ group.name }}
            <v-btn class="mx-4" size="small" :to="'/groupsEdit/'+group.id" icon="mdi-pencil" ></v-btn>
        </v-container>
        <v-divider insset />
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
                    v-for="(user, i) in group.users"
                    :key="i"
                >
                    <td>{{ user.name }}</td>
                    <td>
                        <v-btn size="small" class="float-right" :to="'/student/1'" flat icon=mdi-minus></v-btn>
                    </td>
                </tr>
            </tbody>
        </v-table>
    </v-container>
</template>

<script>
export default {
    computed: {
        group() { return this.$store.state.groups.find(group => group.id == this.$route.params.group_id)},
    },
    data () {
        return {

        }
    }
}
</script>