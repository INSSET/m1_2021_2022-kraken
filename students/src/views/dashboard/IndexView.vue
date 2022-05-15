<template>

  <DashboardAppView>

    <BreadcrumbComponent>
      <BreadcrumbItemComponent label="Dashboard" route="{name: 'root'}" />
    </BreadcrumbComponent>

    <div class="row">

      <div class="col-12">

        <CardComponent title="Dashboard">
          <SubCardComponent>
            Card / SubCard template
          </SubCardComponent>
        </CardComponent>

      </div>

    </div>

  </DashboardAppView>

</template>

<script>
import DashboardAppView from "@/views/includes/DashboardAppView.vue";
import BreadcrumbComponent from "@/components/utils/breadcrumb/BreadcrumbComponent.vue";
import BreadcrumbItemComponent from "@/components/utils/breadcrumb/BreadcrumbItemComponent.vue";
import CardComponent from "@/components/utils/card/CardComponent.vue";
import SubCardComponent from "@/components/utils/card/SubCardComponent.vue";
export default {
  name: "IndexView",
  components: {SubCardComponent, CardComponent, DashboardAppView, BreadcrumbComponent, BreadcrumbItemComponent}
}
</script>

<style scoped>

</style>
