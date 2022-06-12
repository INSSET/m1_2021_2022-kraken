import store from "@/plugins/vuex";
import axios from "axios";
import Group from "@/models/group";
import Student from "@/models/student";

const BASE_URL = "http://backend.insset.localhost/api/v1/";

enum APIRoutes {
    groups = "groups",
}

export function getGroups() {
    axios.get(`${BASE_URL}${APIRoutes.groups}`)
        .then(res => {

            // Transformaion des données
            let groups: Array<Group> = [];
            res.data.forEach((group: { group_id: number, group_name: string, users_names: string[]; }) => {
                let students: Array<Student> = [];
                group.users_names.forEach(studentName => {
                    students.push(new Student(studentName))
                });
                groups.push(new Group(group.group_id, group.group_name, students))
            });

            // Mise à jour du store 
            store.commit({
                type: "setGroups",
                groups: groups,
            })

        })
}

export function createGroupsWithCSV(group_name : string, file : object) {

    axios.post(`${BASE_URL}${APIRoutes.groups}/${group_name}/upload`, {
        file: file
    }, {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    })

}
