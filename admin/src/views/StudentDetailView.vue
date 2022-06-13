<template>
    <v-container>
        <p class="text-h2 text-center">Environnement de {{student.user_name.replace('.', ' ')}}</p>
        <p class="text-h3">Containers</p>
        <v-row class="pa-3" v-if="containerInfo.length > 0">
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
        <p v-else class="text-error pa-2">Pas de containers</p>

        <v-row>           
            <v-col
                class="pa-2"
                cols="12"
            >

                <p class="text-h3">Clés SSH</p>

                <v-btn class="my-3" size="small" @click="displayTextarea = !displayTextarea">Ajouter une clé</v-btn>
                <v-form @submit="addSshKey(student.user_id)" :class="{'d-none': !displayTextarea}">
                    <v-textarea></v-textarea>
                    <v-btn class="mt-3" @click="addSshKey(student.user_id), displayTextarea = !displayTextarea">Valider</v-btn>
                    <v-btn class="mt-3 mx-3" @click="displayTextarea = !displayTextarea">Annuler</v-btn>
                </v-form>
                <div v-if="listSshKey.length > 0">
                    <v-col
                        v-for="sshKey in listSshKey"
                        :key="sshKey"
                        cols="12"
                    >
                        <v-card class="pa-2 break-word">
                            {{sshKey}}
                        </v-card>
                    </v-col>
                </div>
                <p v-else class="text-error pa-2">Pas de clés SSH</p>
                
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
        data() {
            return {
            displayTextarea: false
            }
        },
        computed: mapState({
            containerInfo: 'containerInfo',
            studentInformation: 'students',
            listSshKey: 'listSshKey',
            student() { return this.$store.state.students.find(student => student.user_id == this.$route.params.student_id)},
        }),
        mounted() {
            StudentService.getContainerInfo(this.$route.params.student_id);
            StudentService.getStudentInformation(this.$route.params.student_id);
        },
        methods: {
            actionContainer: function (idStudent: string, action: string) {
                StudentService.setActionContainer(idStudent, action);
            },
            getKeys: function (idStudent: string) {
                StudentService.getSshKeys(idStudent);
            },
            addSshKey: function (idStudent: string) {
                StudentService.addSshKey(idStudent);
            },
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

    textarea {
        width: 100%;
    }

    .break-word {
        word-break: break-all;
    }
</style>