<template>

  <DashboardAppView>

    <BreadcrumbComponent>
      <BreadcrumbItemComponent label="Dashboard" :route="{name: 'root'}" />
      <BreadcrumbItemComponent label="Ma VM" :route="{name: 'root'}" />
    </BreadcrumbComponent>

    <CardComponent title="Ma machine virtuelle">

      <div class="row">

        <div class="col-12 col-md-3">
          <VMComponent name="Symfony" status="stop" image="symfony-5.2.1" link="https://hub.docker.com/" />
        </div>

        <div class="col-12 col-md-3">
          <VMComponent name="BigData" status="up" image="pgsql-10.0.4" link="https://hub.docker.com/" />
        </div>

        <div class="col-12 col-md-3">
          <VMComponent name="Nginx" status="unknown" image="nginx-stable-alpha" link="https://hub.docker.com/" />
        </div>

      </div>

    </CardComponent>

  </DashboardAppView>

</template>

<script>
import CardComponent from "../../components/utils/card/CardComponent.vue";
import DashboardAppView from "../includes/DashboardAppView.vue";
import BreadcrumbComponent from "../../components/utils/breadcrumb/BreadcrumbComponent.vue";
import BreadcrumbItemComponent from "../../components/utils/breadcrumb/BreadcrumbItemComponent.vue";
import VMComponent from "@/components/vm/VMComponent.vue";

export default {
  name: "VirtualSpaceView",
  components: {VMComponent, CardComponent, DashboardAppView, BreadcrumbComponent, BreadcrumbItemComponent},
}
</script>

<style scoped>

</style>
