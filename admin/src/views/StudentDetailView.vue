<template>
    <v-container>
        <v-span class="text-h2 text-center">Environnement de Paquet Tanguy</v-span>
        <v-row class="pa-3">
            <v-col
                v-for="n in 3"
                :key="n"
                cols="12"
                lg="4"
            >
                <v-card contained-text class="pa-2">
                    <v-table>
                        <thead>
                            <tr>
                                <th class="text-center" colspan="2">Name</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Status</td>
                                <td class="text-right">xxx</td>
                            </tr>
                            <tr>
                                <td>Version</td>
                                <td class="text-right">xxx</td>
                            </tr>
                            <tr>
                                <td>Lien</td>
                                <td class="text-right">xxx</td>
                            </tr>
                            <tr>
                                <td>Actions</td>
                                <td class="text-right">
                                    <v-btn size="small" @click="restartContainer()" icon="mdi-reload"></v-btn>
                                    <v-btn size="small" @click="stopContainer()" :visible="true" icon="mdi-stop"></v-btn>
                                    <v-btn size="small" @click="startContainer()" icon="mdi-play"></v-btn>
                                    <v-btn size="small" @click="getLogs()" icon="mdi-format-list-text"></v-btn>
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
    import GroupService from "@/services/group-service";

    export default {
        data() {
            return {}
        },
        provide: { GroupService },
        computed: mapState({
            groups: 'groups',
        }),
        mounted() {
            GroupService.findAll()
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