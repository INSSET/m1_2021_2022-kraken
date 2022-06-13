import axios from "axios";
import store from "@/plugins/vuex";
import Group from "@/models/group";
import Student from "@/models/student";

export default new class GroupService {

    BASE_URL = "http://backend.insset.localhost/api/v1/";

    /**
     * Fetch all groups
     */
    async findAll() {

        store.commit({
            type: "setMsgErrorGetGroups",
            msgErrorGetGroups: "",
        })
        axios.get(`${this.BASE_URL}groups`)
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

    /**
     * Creation of a group
     *
     * @param groupName
     * @param groupFile
     */
    async create(groupName: string, groupFile: object) {

        store.commit({
            type: "setMsgErrorCreateGroup",
            msgErrorCreateGroup: "",
        })
        axios.post(`${this.BASE_URL}groups/${groupName}/upload`, {
            file: groupFile
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

    /**
     * Update the group name
     * 
     * @param groupId 
     * @param groupName 
     */
    async updateName(groupId: number, groupName: string) {

        store.commit({
            type: "setMsgErrorUpdateGroupName",
            msgErrorUpdateGroupName: "",
        })
        axios.post(`${this.BASE_URL}groups/${groupId}`, {
            groupName: groupName
        }).then(res => {
            // Si update Ok, maj des groups
            if (res.status == 200) {
                this.findAll()
            }
        }).catch(()=>{
            store.commit({
                type: "setMsgErrorUpdateGroupName",
                msgErrorUpdateGroupName: "Une erreur est survenue lors du changement du nom du groupe",
            })
        })

    }

}
