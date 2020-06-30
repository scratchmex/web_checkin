<template>
  <!-- <div class="d-flex flex-column align-items-center justify-content-center"> -->
  <b-container fluid="sm" class="py-5 d-flex flex-column align-items-center justify-content-center">
    <div class="w-25">
      <b-img fluid rounded="circle" src="~/static/seminario_junior.png" />
    </div>
    <h1>Seminario Jr.</h1>
    <div class="row d-inline">
      <div class="m-3">
        <div class="px-3">
          <b-icon icon="calendar" />
          <span>Todos los miércoles 15:00hrs.</span>
        </div>
        <div class="px-3">
          <b-icon icon="geo" />
          <span>Salón de seminarios DEMAT</span>
        </div>
      </div>
    </div>
    <b-button to="/checkin" size="lg" variant="secondary">Hacer Checkin</b-button>
  </b-container>
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
