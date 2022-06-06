<template>
    <v-container>
        <v-form>
            <v-text-field
                label="Nom du groupe"
                v-model="group_name"
                class="my-4"
            ></v-text-field>
            <v-file-input
                accept=".csv"
                label="Liste des étudiants"
                @change="onChangeFile"
                class="my-4"
            ></v-file-input>
            <v-btn
                class="bg-deep-purple mb-4"
                @click="onSubmit"
            >
                Créer le groupe
            </v-btn>
        </v-form>
        
        <v-expansion-panels>
            <v-expansion-panel>
                <v-expansion-panel-title>
                    Contenue du fichier
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                    <v-table
                        :class="{'d-none': (students_names.length === 0)}"
                        class="mx-4 mb-4"
                    >
                        <thead>
                            <tr>
                                <th class="text-left">
                                    Nom
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="student_name in students_names"
                                :key="student_name"
                            >
                                <td>{{ student_name }}</td>
                            </tr>
                        </tbody>
                    </v-table>
                </v-expansion-panel-text>
            </v-expansion-panel>
        </v-expansion-panels>
    </v-container>
</template>

<script>
import { createGroupsWithCSV } from '../utils/requests';
import axios from "axios";
export default {
    data() {
        return {
            group_name: "",
            students_names: [],
            csvFile: null,
        }
    },
    methods: {
        onChangeFile: function(e) {
            this.csvFile = e.target.files[0];
            let fileReader = new FileReader();
            fileReader.onload = () => {
                let content = fileReader.result;
                let lines = content.split("\n");
                for(let line in lines) {
                    if (line != 0) {
                        let columns = lines[line].trim().split(";");
                        this.students_names.push(columns[0]);
                    }
                }
            }
            fileReader.readAsText(e.target.files[0])
        },
        onSubmit: function(e) {
            createGroupsWithCSV(this.group_name, this.csvFile)
        }
    }
}
</script>
