<template>
    <v-expansion-panels>
        <v-expansion-panel
            v-for="group in groups"
            :key="group.group_id"
        >
            <v-expansion-panel-title>
                {{ group.group_name }}
            </v-expansion-panel-title>
            <v-expansion-panel-text>
                <v-table>
                    <thead>
                        <tr>
                            <th class="text-left">
                                
                            </th>
                            <th class="text-left">
                                Nom
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="(user,i) in group.users_names"
                            :key="i"
                        >
                            <td>{{ i+1 }}</td>
                            <td>{{ user.users_names }}</td>
                        </tr>
                    </tbody>
                </v-table>
            </v-expansion-panel-text>
        </v-expansion-panel>
    </v-expansion-panels>
</template>

<script>
export default {
    data () {
        return {
            groups: [
                {
                    group_id: 1,
                    group_name: "Group 1",
                    users_names: [
                        {
                            users_names: "toto",
                        },
                        {
                            users_names: "tata",
                        },
                    ],
                },
                {
                    group_id: 2,
                    group_name: "Group 2",
                    users_names: [
                        {
                            users_names: "tutu",
                        },
                        {
                            users_names: "titi",
                        },
                    ],
                },
            ],
        }
    },
}
</script>