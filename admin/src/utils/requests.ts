import store from "@/plugins/vuex";
import axios from "axios";
import Group from "@/models/group";
import Student from "@/models/student";

const BASE_URL = "http://backend.insset.localhost/api/v1/";

enum APIRoutes {
    groups = "groups",
}

export function getGroups() {

    store.commit({
        type: "setMsgErrorGetGroups",
        msgErrorGetGroups: "",
    })
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
        .catch(() => {
            store.commit({
                type: "setMsgErrorGetGroups",
                msgErrorGetGroups: "Une erreur est survenue lors de la récupération des groupes",
            })
        })
}

export function createGroupsWithCSV(group_name : string, file : object) {

    store.commit({
        type: "setMsgErrorCreateGroup",
        msgErrorCreateGroup: "",
    })
    axios.post(`${BASE_URL}${APIRoutes.groups}/${group_name}/upload`, {
        file: file
    }, {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    }).catch(()=>{
        store.commit({
            type: "setMsgErrorCreateGroup",
            msgErrorCreateGroup: "Une erreur est survenue lors de la création du groupe",
        })
    })

}

export function updateGroupName(group_id: number, group_name: string) {

    store.commit({
        type: "setMsgErrorUpdateGroupName",
        msgErrorUpdateGroupName: "",
    })
    axios.post(`${BASE_URL}${APIRoutes.groups}/${group_id}`, {
        groupName: group_name
    }).then(res => {
        // Si update Ok, maj des groups
        if (res.status == 200) {
            getGroups()
        }
    }).catch(()=>{
        store.commit({
            type: "setMsgErrorUpdateGroupName",
            msgErrorUpdateGroupName: "Une erreur est survenue lors du changement du nom du groupe",
        })
    })

}
