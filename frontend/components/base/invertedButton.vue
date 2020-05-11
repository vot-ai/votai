<template>
  <v-btn
    v-bind="$attrs"
    :dark="!$vuetify.theme.dark"
    :light="$vuetify.theme.dark"
    v-on="$listeners"
  >
    <slot v-for="(_, name) in $slots" :slot="name" :name="name" />
  </v-btn>
</template>
<script lang="ts">
import Vue from 'vue'
export default Vue.extend({})
</script>
