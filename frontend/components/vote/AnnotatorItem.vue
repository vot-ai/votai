<template>
  <v-card min-width="100px" outlined tile :dark="darkLight.dark" :light="darkLight.light">
    <v-hover v-if="hasImage" v-slot:default="{ hover }">
      <a :href="imageOrLink" target="_blank">
        <v-img
          :src="item.metadata.image"
          lazy-src="/placeholder.png"
          class="image-hover"
          eager
          :class="hover ? 'image-hovered elevation-5' : ''"
          max-width="700"
          max-height="400"
        >
          <template v-slot:placeholder>
            <v-row class="fill-height ma-0" align="center" justify="center">
              <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
            </v-row>
          </template>
        </v-img>
      </a>
    </v-hover>
    <v-card-title>{{ item.name }}</v-card-title>
    <v-card-subtitle
      v-if="hasLocation"
    >{{$t('vote.item.location', { location: item.metadata.location })}}</v-card-subtitle>
    <v-card-text v-if="hasDescription" class="white-space">{{ item.metadata.description }}</v-card-text>
    <v-card-actions v-if="hasLink">
      <v-btn text :href="item.metadata.link">{{ linkText }}</v-btn>
    </v-card-actions>
    <v-divider></v-divider>
    <v-btn
      block
      tile
      depressed
      x-large
      :loading="loading"
      :disabled="last || waiting"
      @click="$emit('selected', item.id)"
    >{{ buttonText }}</v-btn>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, computed } from '@vue/composition-api'
import { IAnnotator } from '~/server/models/annotator'
import { ThenArg } from '~/types/utils'
import { useDarkTheme } from '~/hooks/vuetify'
import { useI18n } from '~/hooks/i18n'

type SerializedItem = ThenArg<ReturnType<IAnnotator['serializeItem']>>

export default defineComponent({
  props: {
    item: {
      type: Object as () => NonNullable<SerializedItem>,
      required: true
    },
    current: Boolean,
    first: Boolean,
    last: Boolean,
    waiting: Boolean,
    even: Boolean,
    loading: Boolean
  },
  setup(props) {
    const [isDark] = useDarkTheme()
    const i18n = useI18n()
    const darkLight = computed(() => {
      if (props.even !== props.current) {
        return { light: !isDark.value, dark: isDark.value }
      }
      return { light: isDark.value, dark: !isDark.value }
    })
    const buttonText = computed(() => {
      if (props.first) {
        return i18n.t('vote.item.load-next')
      }
      if (props.last) {
        return i18n.t('vote.item.done')
      }
      if (props.waiting) {
        return i18n.t('vote.item.waiting-next')
      }
      if (props.current) {
        return i18n.t('vote.item.choose-current')
      }
      return i18n.t('vote.item.choose-previous')
    })

    const hasImage = computed(() => !!props.item.metadata.image)
    const hasLink = computed(() => typeof props.item.metadata.link === 'string')
    const linkText = computed(() =>
      props.item.metadata.linkText
        ? props.item.metadata.linkText
        : i18n.t('vote.item.default-link-text')
    )
    const imageOrLink = computed(() =>
      hasLink.value ? props.item.metadata.link : props.item.metadata.image
    )
    const hasLocation = computed(() => !!props.item.metadata.location)
    const hasDescription = computed(() => !!props.item.metadata.description)

    return {
      buttonText,
      darkLight,
      hasImage,
      hasLink,
      imageOrLink,
      linkText,
      hasLocation,
      hasDescription
    }
  }
})
</script>

<style lang="scss" scoped>
.white-space {
  white-space: pre-line;
}
.image-hover {
  transform: scale3d(1.01, 1.01, 1);
  transition: all 0.5s;
  cursor: pointer;
}
.image-hovered {
  transform: scale3d(1.05, 1.05, 1);
}
</style>