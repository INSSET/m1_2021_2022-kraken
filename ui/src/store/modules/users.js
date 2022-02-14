import api from "../../config/api";
const users = {
    namespaced: true,

    state: {
        users: []
    },

    mutations: {
        SET_USERS: (state, user) => {
            state.users = user;
        },
    },

    actions: {
        GET_USERS: async ({ commit }) => {
            await api()
                .get(process.env.VUE_APP_GET_USERS)
                .then(response => {
                    const users = response.data;
                    commit("SET_USERS", users);
                })
                .catch(error => {
                    throw error;
                });
        },
    }
}

export default users;
