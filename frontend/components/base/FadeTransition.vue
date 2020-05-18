<template>
  <base-transition name="my-fade" v-bind="$attrs" v-on="$listeners">
    <slot />
  </base-transition>
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import BaseTransition from './BaseTransition.vue'
export default defineComponent({
  components: { BaseTransition }
})
</script>

<style lang="scss">
$trans-cubic-bezier: cubic-bezier(0.215, 0.61, 0.355, 1);
@mixin timing-function {
  animation-timing-function: $trans-cubic-bezier;
}

/* ----------------------------------------------
 * Modified version from Animista
 * Animista is Licensed under FreeBSD License.
 * See http://animista.net/license for more info. 
 * w: http://animista.net, t: @cssanimista
 * ---------------------------------------------- */

@keyframes fadeOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

.my-fade-enter-active {
  animation-name: fadeIn;
}

.my-fade-leave-active {
  animation-name: fadeOut;
}

.my-fade-move {
  transition-timing-function: ease-in-out;
  transition-property: all;
  transition-duration: 400ms;
}
</style>