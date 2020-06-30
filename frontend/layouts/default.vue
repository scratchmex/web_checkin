<template>
  <div>
    <MainNavbar />
    <Nuxt />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import MainNavbar from "~/components/MainNavbar.vue";

export default Vue.extend({
  components: {
    MainNavbar
  }
});
</script>

<style>
</style>
