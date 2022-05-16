import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import GroupsView from "../views/GroupsView.vue";
import GroupDetailView from "../views/GroupDetailView.vue";
import AddGroupView from "../views/AddGroupView.vue";
import GroupsEdit from "../views/GroupsEdit.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/groups",
      name: "groupsView",
      component: GroupsView,
    },
    {
      path: "/groups/add",
      name: "addGroup",
      component: AddGroupView,
    },
    {
      path: "/groupsEdit/:group_id",
      name: "groupsEdit",
      component: GroupsEdit,
    },
    {
      path: "/groups/:group_id",
      name: "groupDetail",
      component: GroupDetailView,
    },
  ],
});

export default router;
