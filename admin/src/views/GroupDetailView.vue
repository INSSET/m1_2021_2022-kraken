<template>
    <v-container>
        <v-container>
            Nom : {{ group.group_name }}
            <v-btn class="mx-4" size="small" to="/about" icon="mdi-pencil" ></v-btn>
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
                    v-for="(user, i) in group.users_names"
                    :key="i"
                >
                    <td>{{ user }}</td>
                    <td>
                    </td>
                </tr>
            </tbody>
        </v-table>
    </v-container>
</template>

<script>
export default {
    computed: {
        group() { return this.$store.state.groups.find(group => group.group_id == this.$route.params.group_id)},
    },
    data () {
        return {

        }
    }
}
</script>