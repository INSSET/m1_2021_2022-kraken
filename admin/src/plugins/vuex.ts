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
        }
    }
})

export default store;