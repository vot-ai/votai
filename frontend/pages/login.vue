<template>
  <div>
    <button @click="$auth.loginWith('github')">Login github</button>
    <button @click="$auth.loginWith('anonymous')">Login Anonymous</button>
    <button @click="$auth.logout()">logout</button>
  </div>
</template>
<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  ...{ auth: 'guest' }
})
</script>
