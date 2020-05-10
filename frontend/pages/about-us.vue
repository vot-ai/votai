<template>
  <v-layout>
    <v-flex class="text-center">
      <img src="/v.png" alt="Vuetify.js" class="mb-5" />
      <blockquote class="blockquote">
        &#8220;First, solve the problem. Then, write the code.&#8221;
        <button
          @click="$i18n.setLocale('en')"
        >en</button>
        <button @click="$i18n.setLocale('pt')">pt</button>
        <footer>
          <small>
            <em>&mdash;John Johnson</em>
          </small>
        </footer>
      </blockquote>
    </v-flex>
  </v-layout>
</template>
<script lang="ts">
import Vue from 'vue'
export default Vue.extend({})
</script>