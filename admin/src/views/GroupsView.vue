<template>
    <v-container>
        <v-expansion-panels>
            <v-expansion-panel
                v-for="group in groups"
                :key="group.group_id"
            >
                <v-expansion-panel-title>
                    {{ group.group_name }}
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                    <v-list
                        v-for="(user,i) in group.users_names"
                        :key="i"
                    >
                        <v-list-item
                            density='compact'
                        >
                            <v-list-item-header>
                                {{ user.users_names }}
                            </v-list-item-header>
                        </v-list-item>
                    </v-list>
                </v-expansion-panel-text>
            </v-expansion-panel>
        </v-expansion-panels>
    </v-container>
</template>

<script>
const fetch_groups = fetch("https://0.0.0.0:5000/api/v1/students", {
    "method": "GET",
})
.then(response => {
    if (response.ok) {
        return response.json();
    } else {
        console.log(response.statusText);
    }
})
.then(json => {
    return json.body;
})
.catch(err=>{
    console.log(err);
});
console.log(fetch_groups);
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