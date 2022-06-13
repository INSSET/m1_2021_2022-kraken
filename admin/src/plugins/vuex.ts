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
                    new Student(1,"toto","Group 1"),
                    new Student(2,"tata", "Group 1"),
                ]
            ),
            new Group(
                2,
                "Group 2",
                [
                    new Student(3,"tutu","Group 2"),
                    new Student(4,"titi","Group 2"),
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
        listSshKey: [
            "ssh-dss AAAAB3NzaC1kc3MAAACBAJhbQcZK8lFMvpw7trbFj51Sqjd9nKBu2xkw/kvUAQlPQPaIRLOiq92fxp+jzp97xDqpwFnvU++ptUiB1nQQ8oq8l5t5QuHwfMMnSDMXhWf2235i4Lw2DtRTbxs0UQJ1l+QxO/AjlV/POcFpq6Z0PKMosi8TslqqPaqAbQtiEX2DAAAAFQDaK1EZY12itrt0lomTAOT0QATilwAAAIAK9C0YTR0T82r7TFheo/+vU6dS9KCypEjR7rEVf7MxCJLd9MQNkVTJe7XCFnYeT9oz7h8NbYHGyDQr7EZGIchtiju6EPFWuQWEAJAHq7z9s9ygoVqyWSQo0y/6riihJk5bo+Etj//OdwndlfKg0c6UGBFg8T2i6nKsbmMMEAI+XAAAAIA+bPjEeoZhwLuCp3Bv0+B4mWgGqnb2IhRSVDQNYeHIofhiSY7prVB+O1iQhrN/EJlygkaFWNaVlPmxrXa+8i+ZGWeVlAaKJdSAsDawNjOaHTi6/Cfqm7NTrLIIeOcjjxwrPLPZ3v0tP8MFjhYFdgjooYjTDzqQmpCGVSA4hXtqhg== tdd@CodeMagic.local",
            "ssh-dss AAAAB3NzaC1kc3MAAACBAJhbQcZK8lFMvpw7trbFj51Sqjd9nKBu2xkw/kvUAQlPQPaIRLOiq92fxp+jzp97xDqpwFnvU++ptUiB1nQQ8oq8l5t5QuHwfMMnSDMXhWf2235i4Lw2DtRTbxs0UQJ1l+QxO/AjlV/POcFpq6Z0PKMosi8TslqqPaqAbQtiEX2DAAAAFQDaK1EZY12itrt0lomTAOT0QATilwAAAIAK9C0YTR0T82r7TFheo/+vU6dS9KCypEjR7rEVf7MxCJLd9MQNkVTJe7XCFnYeT9oz7h8NbYHGyDQr7EZGIchtiju6EPFWuQWEAJAHq7z9s9ygoVqyWSQo0y/6riihJk5bo+Etj//OdwndlfKg0c6UGBFg8T2i6nKsbmMMEAI+XAAAAIA+bPjEeoZhwLuCp3Bv0+B4mWgGqnb2IhRSVDQNYeHIofhiSY7prVB+O1iQhrN/EJlygkaFWNaVlPmxrXa+8i+ZGWeVlAaKJdSAsDawNjOaHTi6/Cfqm7NTrLIIeOcjjxwrPLPZ3v0tP8MFjhYFdgjooYjTDzqQmpCGVSA4hXtqhg== tdd@CodeMagic.local",
        ],
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