import { createRouter, createWebHistory } from "vue-router";
import GroupsView from "../views/GroupsView.vue";
import GroupDetailView from "../views/GroupDetailView.vue";
import AddGroupView from "../views/AddGroupView.vue";
import GroupsEdit from "../views/GroupsEdit.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/groups",
      name: "groups",
      component: GroupsView,
    },
    {
      path: "/groups/add",
      name: "addGroup",
      component: AddGroupView,
    },
    {
      path: "/groups/:group_id",
      name: "groupDetail",
      component: GroupDetailView,
    },
    {
      path: "/groupsEdit/:group_id",
      name: "groupsEdit",
      component: GroupsEdit,
    },
  ],
});

export default router;
