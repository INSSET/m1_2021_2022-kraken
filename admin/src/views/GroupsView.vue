<template>
    <v-expansion-panels>
        <v-expansion-panel
            v-for="group in groups"
            :key="group.group_id"
        >
            <v-expansion-panel-title>
                <v-btn @click="renameGroup($event, group.group_id)" icon=mdi-pencil class="mr-4"></v-btn>
                {{ group.group_name }}
                <v-text-field
                    label="Nouveau nom" class="d-none group-{{group.group_id}}"
                ></v-text-field>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
                <v-list
                    v-for="(user,i) in group.users_names"
                    :key="i"
                >
                    <v-list-item>
                        <v-list-item-header>
                            {{ user.users_names }}
                        </v-list-item-header>
                        <template v-slot:append><v-btn icon=mdi-account-multiple-minus></v-btn></template>
                    </v-list-item>
                    
                </v-list>
            </v-expansion-panel-text>
        </v-expansion-panel>
    </v-expansion-panels>
</template>

<script>
fetch("0.0.0.0:5000/api/v1/students", {
    "method": "GET"
})
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
    methods: {
        deleteUser: function () {
            fetch("0.0.0.0:5000/", {
                "method": ""
            })
        },
        renameGroup: function(event, group_id) {
            const input = document.getElementsByClassName('group-'+group_id);
            console.log(input);
            input[0].style.display = "block";
        }
    }
}
</script>