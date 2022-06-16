<template>
  <v-app>
    <v-main>
      <v-card>
        <v-layout>
          <v-navigation-drawer
            theme="dark"
            class="bg-purple-darken-4"
            permanent
          >
            <v-list color="transparent">
              <v-list-item>
                <v-btn  to="/" variant="plain">
                  <v-icon>mdi-home</v-icon>
                  Home
                </v-btn>
              </v-list-item>
              <v-list-item>
                <v-btn  to="/groups" variant="plain">
                  <v-icon>mdi-account-multiple</v-icon>
                  Groups
                </v-btn>
              </v-list-item>
            </v-list>
          </v-navigation-drawer>
          <v-main style="height: 100vw">
            <router-view/>
          </v-main>
        </v-layout>
      </v-card>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App',

  data () {
    return {
      //
    }
  },
})
</script>
