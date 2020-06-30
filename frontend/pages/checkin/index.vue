<template>
  <div>
    <b-button v-b-modal.complete-checkin>Launch modal</b-button>
    <b-modal
      id="complete-checkin"
      title="Completar Checkin"
      ok-only
      ok-title="Terminar"
      no-close-on-backdrop
      hide-header-close
      no-close-on-esc
    >
      Para completar el Checkin, muestra el siguiente código QR al encargado
      <div id="qr" v-html="qr_content"></div>
    </b-modal>

    <div class="container">
      <h1>Hacer un Checkin</h1>

      <b-form @submit.prevent>
        <b-form-group
          label="NUA"
          label-cols-lg="2"
          valid-feedback="si!"
          invalid-feedback="no!"
          :state="false"
        >
          <b-input-group>
            <b-input-group-prepend is-text>
              <span>#</span>
            </b-input-group-prepend>
            <b-form-input placeholder="Escribe tu NUA" type="number" pattern="[0-9]*" required />
          </b-input-group>
        </b-form-group>

        <b-form-group label="Nombre completo" label-cols-lg="2">
          <b-input-group>
            <b-input-group-prepend is-text>
              <b-icon icon="person" />
            </b-input-group-prepend>
            <b-form-input placeholder="Escribe tu nombre" disabled />
          </b-input-group>
        </b-form-group>

        <b-form-group
          label="ID del evento"
          label-cols-lg="2"
          valid-feedback="si!"
          invalid-feedback="no!"
          :state="true"
        >
          <b-input-group>
            <b-input-group-prepend is-text>
              <b-icon icon="calendar2" />
            </b-input-group-prepend>
            <b-form-input placeholder="Pregunta el ID" required />
          </b-input-group>
        </b-form-group>

        <b-button type="submit" variant="primary">Enviar</b-button>
      </b-form>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  data() {
    return {
      qr_content: ""
    };
  },
  created() {
    this.qr_content = `<p>HTML here</p>`;
  }
});
</script>

<style>
</style>