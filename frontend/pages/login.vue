<template>
  <v-container key="login-page" fill-height>
    <v-row align="center" justify="center">
      <fade-transition appear>
        <v-col cols="12" sm="8" md="6" lg="4">
          <h2 class="display-1 font-weight-light mb-3">{{$t('login.header')}}</h2>
          <p class="body-1">{{$t('login.body-1')}}</p>
          <p class="body-1">
            {{$t('login.body-2.left')}}
            <b>{{$t('login.body-2.anonymous')}}</b>
            {{$t('login.body-2.right')}}
          </p>
        </v-col>
      </fade-transition>
      <fade-transition appear>
        <login-buttons />
      </fade-transition>
    </v-row>
  </v-container>
</template>
<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import LoginButtons from '~/components/login/LoginButtons.vue'

export default defineComponent({
  ...{ auth: 'guest' },
  components: { LoginButtons }
})
</script>
