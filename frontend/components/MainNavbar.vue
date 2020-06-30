<template>
  <b-navbar toggleable="md" variant="dark" type="dark">
    <b-navbar-brand to="/">
      <b-icon icon="bootstrap" />
      <span>Web-checkin</span>
    </b-navbar-brand>
    <b-navbar-toggle target="main-navbar" />
    <b-collapse is-nav id="main-navbar">
      <b-navbar-nav class="mr-auto">
        <b-nav-item to="/checkin" active-class="active">Registro</b-nav-item>
        <b-nav-item to="/info" active-class="active">Más información</b-nav-item>
        <b-nav-item to="/contact" active-class="active">Contáctanos</b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav>
        <b-nav-item to="/login" active-class="active">Admin</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({});
</script>