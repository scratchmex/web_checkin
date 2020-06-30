<template>
  <div>
    <h1>Iniciar sesión</h1>
    <b-form @submit.prevent>
      <b-form-group
        label-cols-lg="2"
        label="Usuario"
        valid-feedback="si!"
        invalid-feedback="no!"
        :state="true"
      >
        <b-input-group>
          <b-input-group-prepend is-text>
            <b-icon icon="person" />
          </b-input-group-prepend>
          <b-form-input placeholder="Escribe tu usuario" required/>
        </b-input-group>
      </b-form-group>
      <b-form-group
        label-cols-lg="2"
        label="Contraseña"
        valid-feedback="si!"
        invalid-feedback="no!"
        :state="false"
      >
        <b-input-group>
          <b-input-group-prepend is-text>
            <b-icon icon="lock" />
          </b-input-group-prepend>
          <b-form-input type="password" placeholder="Escribe tu contraseña" required/>
        </b-input-group>
      </b-form-group>

      <b-button type="submit" variant="primary">Enviar</b-button>
    </b-form>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({});
</script>

<style>
</style>