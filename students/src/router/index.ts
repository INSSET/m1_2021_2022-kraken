import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import IndexView from "../views/dashboard/IndexView.vue";
import AddSSHKeyView from "../views/dashboard/AddSSHKeyView.vue";
import VirtualSpaceView from "../views/dashboard/VirtualSpaceView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      component: LoginView
    },
    {
      path: "/dashboard",
      name: "root",
      component: IndexView
    },
    {
      path: "/ssh",
      name: "ssh",
      component: AddSSHKeyView
    },
    {
      path: "/virtual-space",
      name: "vm",
      component: VirtualSpaceView
    }
  ],
});

export default router;
