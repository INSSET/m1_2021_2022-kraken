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

          <form @submit="onSubmit">

            <div class="form-group">
              <label for="sshKey">Clé</label>
              <textarea id="sshKey" class="form-control" rows="6" placeholder="ssh-rsa AAAA..."
              v-model="sshKey"></textarea>
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
import axios from "axios"
axios.defaults.baseURL = "http://backend.insset.localhost/api/v1";

export default {
  name: "AddSSHKeyView",
  components: {CardComponent, DashboardAppView, BreadcrumbComponent, BreadcrumbItemComponent},
  data() {
    return{
      sshKey: null,
    } 
  },
  methods:{
    onSubmit : function(){
        axios.get("http://backend.insset.localhost/api/v1/students/john.doe")
        .then((res) => {
          var user_id = res.data.user_id;
          var sentKey = { key: this.sshKey };
          console.log(sentKey)
          axios.post("http://backend.insset.localhost/api/v1/students/"+user_id+"/ssh/upload/", sentKey)
            .catch(error => {
              console.error('There was an error!', error);
            })
          }
        )        
        event.preventDefault();
    }
  }
}
</script>

<style scoped>

</style>
