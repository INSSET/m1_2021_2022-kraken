<template>

  <DashboardAppView>

    <BreadcrumbComponent>
      <BreadcrumbItemComponent label="Dashboard" :route="{name: 'root'}" />
      <BreadcrumbItemComponent label="Clefs ssh" :route="{name: 'root'}" />
      <BreadcrumbItemComponent label="Nouvelle clef" :route="{name: 'ssh'}" />
    </BreadcrumbComponent>

    <div class="row">

      <div class="col-12">

        <CardComponent title="Nouvelle clé ssh">

          <form>

            <div class="form-group">
              <label for="sshKey">Clé</label>
              <textarea id="sshKey" class="form-control" rows="6" placeholder="ssh-rsa AAAA..."></textarea>
            </div>

            <div class="form-group">
              <button type="submit" class="btn btn-primary">Valider</button>
            </div>

          </form>

        </CardComponent>

      </div>

    </div>

  </DashboardAppView>

</template>

<script>
import CardComponent from "@/components/utils/card/CardComponent.vue";
import DashboardAppView from "@/views/includes/DashboardAppView.vue";
import BreadcrumbComponent from "@/components/utils/breadcrumb/BreadcrumbComponent.vue";
import BreadcrumbItemComponent from "@/components/utils/breadcrumb/BreadcrumbItemComponent.vue";

export default {
  name: "AddSSHKeyView",
  components: {CardComponent, DashboardAppView, BreadcrumbComponent, BreadcrumbItemComponent},
  props: [
      "sskKey"
  ]
}
</script>

<style scoped>

</style>
