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
    },
    mutations: {
        setGroups (state, payload) {
            state.groups = payload.groups;
        }
    }
})

export default store;