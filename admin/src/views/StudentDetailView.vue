<template>
    <v-container>
        <v-span class="text-h2 text-center">Environnement de {{student.user_name.replace('.', ' ')}}</v-span>
        <v-row class="pa-3" v-if="containerInfo">
            <v-col
                v-for="container in containerInfo"
                :key="container"
                cols="12"
                lg="4"
            >
                <v-card contained-text class="pa-2">
                    <v-table>
                        <thead>
                            <tr>
                                <th class="text-center" colspan="2">{{ container.containerName }} - ( {{ container.id }} )</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Image</td>
                                <td class="text-right">{{ container.image }}</td>
                            </tr>
                            <tr>
                                <td>Port SSH</td>
                                <td class="text-right">{{ container.ports }}</td>
                            </tr>
                            <tr>
                                <td>Lien</td>
                                <td class="text-right"><a :href="'http://'+student.user_name+'.insset.localhost'">{{ student.user_name }}.insset.localhost</a></td>
                            </tr>
                            <tr>
                                <td>Status</td>
                                <td class="text-right">{{ container.status }}</td>
                            </tr>
                            <tr>
                                <td>Actions</td>
                                <td class="text-right">
                                <span :class="{'d-none': container.status == 'down'}"><v-btn size="small" @click="actionContainer(student.user_id, 'down')" icon="mdi-stop"></v-btn></span>
                                    <span :class="{'d-none': container.status == 'up'}"><v-btn size="small" @click="actionContainer(student.user_id, 'up')" icon="mdi-play"></v-btn></span>
                                    <span><v-btn size="small" @click="actionContainer(student.user_id, 'restart')" icon="mdi-reload"></v-btn></span>
                                    <span><v-btn size="small" @click="getLogs()" icon="mdi-format-list-text"></v-btn></span>
                                </td>
                            </tr>
                        </tbody>
                    </v-table>
                </v-card>
            </v-col>
            
        </v-row>
    </v-container>
</template>

<script lang="ts">
    import {mapState} from 'vuex';
    import StudentService from "@/services/student-service";


    // Récupérer le port SSH du container
    // Refresh des logs tous les x temps
    // SSH
    // Dockerfiles
    // Status de container basé sur les status docker

    // [APP].[LOGIN_ETUDIANT].insset.localhost
    // => symfony.paquet.tanguy.insset.localhost
    export default {
        provide: { StudentService },
        computed: mapState({
            containerInfo: 'containerInfo',
            studentInformation: 'students',
            student() { return this.$store.state.students.find(student => student.user_id == this.$route.params.student_id)},
        }),
        mounted() {
            StudentService.getContainerInfo(this.$route.params.group_id);
            StudentService.getStudentInformation(this.$route.params.group_id);
        },
        methods: {
            actionContainer: function (idStudent: string, action: string) {
                fetch("http://0.0.0.0:5000/api/v1/students/" + idStudent + "/container/command/" + action, {
                    "method": "POST"
                })
            },
            getKeys: function (user_id: string) {
                fetch("http://0.0.0.0:5000/api/v1/students/" + user_id + "/keys", {
                    "method": "GET"
                }).then(function (response) {
                    return response;
                })
            }
        }
    } 
</script>

<style lang="scss">
    .mdi {
        &-play {
            color: greenyellow!important;
        }
        &-stop {
            color: red;
        }
        &-reload {
            color: orange;
        }
    }
</style>