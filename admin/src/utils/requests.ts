import store from "@/plugins/vuex";
import fetchAPI from "./callAPI";

enum Method {
    GET = "GET",
}
enum APIRoutes {
    getGroups = "students",
}

export function getGroups() {
    fetchAPI(APIRoutes.getGroups, Method.GET)
    .then(response => {
        console.log(response);
        store.commit({
            type: "setGroups",
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
                {
                    group_id: 3,
                    group_name: "Group 3",
                    users_names: [
                        "tita",
                        "titutu",
                    ],
                },
            ],
        })
    })
    .catch(err => {
        console.log(err);
        store.commit({
            type: "setGroups",
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
                {
                    group_id: 3,
                    group_name: "Group 3",
                    users_names: [
                        "tita",
                        "titutu",
                    ],
                },
            ],
        })
    })
}