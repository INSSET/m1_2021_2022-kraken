import { createStore } from 'vuex';

// Create a new store instance.
const store = createStore({
    state () {
        return {
            groups: [
                {
                    group_id: 1,
                    group_name: "Group 1",
                    users_names: [
                        "toto",
                        "tata",
                    ],
                },
                {
                    group_id: 2,
                    group_name: "Group 2",
                    users_names: [
                        "tutu",
                        "titi",
                    ],
                },
            ],
        }
    },
    mutations: {
    }
})

export default store;