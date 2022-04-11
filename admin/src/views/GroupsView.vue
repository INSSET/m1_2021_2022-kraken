<template>
    <v-container>
        <v-table>
            <thead>
                <tr>
                    <th class="text-left">
                        Nom
                    </th>
                    <th class="text-left">
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
                    <td>
                        <v-btn  :to="'/groups/'+group.group_id" icon="mdi-magnify" ></v-btn>
                        <v-btn  to="/about" icon="mdi-pencil" ></v-btn>
                    </td>
                </tr>
            </tbody>
        </v-table>
    </v-container>
</template>

<script>
import { mapState } from 'vuex';
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