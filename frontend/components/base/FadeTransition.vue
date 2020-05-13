<template>
  <transition
    :appear="appear"
    :appear-active-class="appearClass"
    :enter-active-class="enterClass"
    :leave-active-class="leaveClass"
    mode="out-in"
    :duration="300"
  >
    <slot />
  </transition>
</template>

<script>
import { defineComponent, computed } from '@vue/composition-api'
export default defineComponent({
  inheritAttrs: false,
  props: {
    appear: Boolean,
    enter: Boolean,
    leave: Boolean
  },
  setup({ appear, enter, leave }) {
    const fadeIn = 'animated fadeIn'
    const fadeOut = 'animated fadeOut'
    const appearClass = computed(() => {
      return appear ? fadeIn : undefined
    })
    const enterClass = computed(() => {
      return enter ? fadeIn : undefined
    })
    const leaveClass = computed(() => {
      return leave ? fadeOut : undefined
    })
    return { appearClass, enterClass, leaveClass }
  }
})
</script>
