import store from "@/plugins/vuex";
import fetchAPI from "./callAPI";
import axios from "axios";

enum Method {
    GET = "GET",
    POST = "POST",
}
enum APIRoutes {
    getGroups = "groups",
}

export function getGroups() {
    fetchAPI(APIRoutes.getGroups, Method.GET, {})
    .then(response => {
        store.commit({
            type: "setGroups",
            groups: response,
        })
    })
    .catch(err => {
        store.commit({
            type: "setGroups",
            groups: [],
        })
    })
}

export function createGroupsWithCSV(group_name : string, file : object) {

    axios.post(`http://backend.insset.localhost/api/v1/groups/${group_name}/upload`, {
        file: file
    }, {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
    }).then(res => {
        console.log(res)
    })

}
