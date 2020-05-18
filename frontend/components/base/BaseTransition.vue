<template>
  <transition-group
    v-if="group"
    v-bind="$attrs"
    :appear="appear"
    @leave="leave"
    @before-enter="beforeEnter"
    @before-leave="beforeLeave"
    @after-enter="afterEnter"
    @after-leave="afterLeave"
  >
    <slot />
  </transition-group>
  <transition
    v-else
    v-bind="$attrs"
    :appear="appear"
    @leave="leave"
    @before-enter="beforeEnter"
    @before-leave="beforeLeave"
    @after-enter="afterEnter"
    @after-leave="afterLeave"
  >
    <slot />
  </transition>
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'
export default defineComponent({
  inheritAttrs: false,
  props: {
    appear: Boolean,
    group: Boolean,
    duration: {
      type: Number,
      default: 500
    }
  },
  setup(props, ctx) {
    // Lifecycle hooks
    const cleanUpStyles = (el: HTMLElement) => {
      el.style.animationFillMode = ''
      el.style.animationDuration = ''
    }
    const setAbsolutePosition = (el: HTMLElement) => {
      el.style.left = el.offsetLeft + 'px'
      el.style.top = el.offsetTop + 'px'
      el.style.width = el.offsetWidth + 'px'
      el.style.height = el.offsetHeight + 'px'
      el.style.position = 'absolute'
    }
    const beforeEnter = (el: HTMLElement) => {
      el.style.animationDuration = `${props.duration}ms`
      el.style.animationFillMode = 'both'
      ctx.emit('before-enter', el)
    }
    const afterEnter = (el: HTMLElement) => {
      cleanUpStyles(el)
      ctx.emit('after-enter', el)
    }
    const afterLeave = (el: HTMLElement) => {
      cleanUpStyles(el)
      ctx.emit('after-leave', el)
    }
    const beforeLeave = (el: HTMLElement) => {
      el.style.animationDuration = `${props.duration}ms`
      el.style.animationFillMode = 'both'
      ctx.emit('before-leave', el)
    }
    const leave = (...args: any[]) => {
      setAbsolutePosition(args[0])
      ctx.emit('leave', ...args)
    }
    return {
      beforeEnter,
      afterEnter,
      afterLeave,
      beforeLeave,
      leave
    }
  }
})
</script>
