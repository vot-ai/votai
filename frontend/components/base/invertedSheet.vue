<template>
  <v-sheet v-bind="$attrs" v-on="$listeners">
    <slot v-for="(_, name) in $slots" :slot="name" :name="name" />
  </v-sheet>
</template>
<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import { useInvertedTheme } from '../../hooks/vuetify'
export default defineComponent({
  setup() {
    useInvertedTheme()
  }
})
</script>
