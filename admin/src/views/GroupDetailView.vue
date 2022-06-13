<template>
    <v-container>
        <v-container>
            Nom : {{ group.name }}
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
                    v-for="(user, i) in group.users"
                    :key="i"
                >
                    <td>{{ user.name }}</td>
                    <td>
                        <v-btn size="small" class="float-right" :to="'/student/'+getIdStudent(user.name)" icon=mdi-laptop></v-btn>
                    </td>
                </tr>
            </tbody>
        </v-table>
    </v-container>
</template>

<script lang="ts">

    import {mapState} from 'vuex';
    import StudentService from "@/services/student-service";

    export default {
        provide: { StudentService },
        computed: mapState({
            group() { return this.$store.state.groups.find(group => group.id == this.$route.params.group_id)},        }),
        data () {
            return {

            }
        },
        method: {
            getIdStudent: function(nameStudent: string) {
                StudentService.getStudentInformationByName(nameStudent);
            }
        }
    }
</script>