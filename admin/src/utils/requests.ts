import store from "@/plugins/vuex";
import fetchAPI from "./callAPI";
import axios from "axios";

const BASE_URL = "http://backend.insset.localhost/api/v1/";

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
    axios.get(`${BASE_URL}/${APIRoutes.getGroups}`)
        .then(res => {
            console.log(`retour axios :`)
            console.log(res)
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
