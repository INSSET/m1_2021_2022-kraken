import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios"
axios.defaults.headers.post['Content-Type'] ='application/json;charset=utf-8';
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
axios.defaults.baseURL = "http://backend.insset.localhost/api/v1";

const app = createApp(App);

app.use(router);

app.mount("#app");
