<template>

  <div class="vm-container">

    <h4 class="vm-name">{{ name }}</h4>

    <div class="vm-body">

      <div class="vm-item">
        <span>Status</span>
        <span class="vm-status" :class="classObjectStatus">{{ status.charAt(0).toUpperCase() + status.slice(1) }} <small></small></span>
      </div>

      <div class="vm-item">
        <span>Version</span>
        <strong class="vm-version">{{ image }}</strong>
      </div>

      <div class="vm-item">
        <span>Lien</span>
        <a :href="link" target="_blank">{{ getLinkTitle() }}</a>
      </div>

      <div class="vm-item">
        <span>Actions</span>
        <div class="vm-actions">
          <button class="vm-apply up" @click="start" v-if="status === 'stop'" title="Démarrer"><i class="fa-duotone fa-play"></i></button>
          <button class="vm-apply stop" @click="stop" v-else-if="status === 'up'" title="Stopper"><i class="fa-duotone fa-stop"></i></button>
          <button class="vm-apply unknown" @click="restart" title="Redémarrer"><i class="fa-duotone fa-repeat"></i></button>
          <button class="vm-apply" @click="logs" title="Logs"><i class="fa-duotone fa-list"></i></button>
        </div>
      </div>

    </div>

  </div>

</template>

<script>
export default {
  name: "VMComponent",
  props: {
    name: {
      type: String,
      required: true
    },
    status: {
      type: String,
      required: true
    },
    image: {
      type: String,
      required: true
    },
    link: {
      type: String,
      required: true
    }
  },
  computed: {
    classObjectStatus() {
      return {
        up: this.status === 'up',
        stop: this.status === 'stop',
        unknown: this.status === 'unknown'
      }
    }
  },
  methods: {
    getLinkTitle: function () {
      return this.link.replace(/^https?:\/\//, '').replace(/\//g, '');
    },
    start() {
      alert("START");
    },
    stop() {
      alert("STOP");
    },
    restart() {
      alert("RESTART");
    },
    logs() {
      alert("LOGS");
    }
  }
}
</script>

<style scoped lang="scss">

  @import "@/assets/components/vm.scss";

</style>
