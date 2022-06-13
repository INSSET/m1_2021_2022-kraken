import Group from '@/models/group';
import Student from '@/models/student';
import { createStore } from 'vuex';

// Create a new store instance.
const store = createStore({
    state: {
        groups: [
            new Group(
                1,
                "Group 1",
                [
                    new Student("toto"),
                    new Student("tata"),
                ]
            ),
            new Group(
                2,
                "Group 2",
                [
                    new Student("tutu"),
                    new Student("titi"),
                ]
            ),
        ],
        msgErrorGetGroups: "",
        msgErrorCreateGroup: "",
        msgErrorUpdateGroupName: "",
        students: [
            {
                user_id: "1",
                user_name: "tanguy.paquet",
                group_id: "1",
            },
            {
                user_id: "2",
                user_name: "harold.trannois",
                group_id: "1",
            }
        ],
        containerInfo: {
            1: {
                id: "1",
                image: "synfony-5.2.1",
                ports: "20001",
                status: "up",
                containerName: "Mon Symfony"
            },
            2: {
                id: "2",
                image: "pgsql-10.0.4",
                ports: "30000",
                status: "down",
                containerName: "Ma base de donnée"
            }
        },
        listSshKey: {

        },
    },
    mutations: {
        setGroups (state, payload) {
            state.groups = payload.groups;
        },
        setMsgErrorGetGroups (state, payload) {
            state.msgErrorGetGroups = payload.msgErrorGetGroups
        },
        setMsgErrorCreateGroup (state, payload) {
            state.msgErrorCreateGroup = payload.msgErrorCreateGroup
        },
        setMsgErrorUpdateGroupName (state, payload) {
            state.msgErrorUpdateGroupName = payload.msgErrorUpdateGroupName
        },
        resetAllMsgError (state, payload) {
            state.msgErrorGetGroups = ""
            state.msgErrorCreateGroup = ""
            state.msgErrorUpdateGroupName = ""
        },
        reloadStudents (state, payload) {
            state.students = payload.students
        },
        reloadContainer (state, payload) {
            state.containerInfo = payload.containerInfo;
        },
        reloadSshKey (state, payload) {
            state.listSshKey = payload.listSshKey
         }
    }
})


export default store;