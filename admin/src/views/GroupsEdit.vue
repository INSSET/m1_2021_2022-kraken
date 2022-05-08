<template>
    <v-container>
        <h1 class="">
            Groupe :
            <v-form @submit="renameGroup(group_id)"><v-text-field v-model="group_name" :disabled="disabled == 1"></v-text-field></v-form>
            <v-btn class="ml-4" icon="mdi-pencil" @click="disabled = (disabled + 1) % 2"></v-btn>
        </h1>
        <v-table>
            <thead>
                <tr>
                    <th>
                        Name ({{$route.params.id_group}})
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="(user,i) in users_names"
                    :key="i"
                >
                    <td>{{ user.users_names }} <v-btn class="float-right" flat icon=mdi-minus @click="deleteUser(user.users_names)"></v-btn></td>
                </tr>
            </tbody>
        </v-table>
    </v-container>
</template>

<script>
const fetch_groups = fetch("https://0.0.0.0:5000/api/v1/students/", {
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
            group_id: 1,
            group_name: "Master 1 - Informatique",
            users_names: [
                {
                    users_names: "toto",
                },
                {
                    users_names: "tata",
                },
                {
                    users_names: "aaa",
                },
                {
                    users_names: "zzz",
                },
                {
                    users_names: "eee",
                },
                {
                    users_names: "rrr",
                },
            ],
            disabled: 1
        }
    },
    methods: {
        deleteUser: function (user_name) {
            fetch("0.0.0.0:5000/", {
                "method": "DELETE"
            })
        },
        renameGroup: function(group_id) {
            fetch("0.0.0.0:5000/api/v1/students/"+group_id, {
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
</style>
