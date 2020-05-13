<template>
  <v-container fill-height>
    <fade-transition appear>
      <v-row key="login-page" align="center" justify="center">
        <v-col cols="12" sm="8" md="6" lg="4">
          <h2 class="display-1 font-weight-light mb-3">{{$t('login.header')}}</h2>
          <p class="body-1">{{$t('login.body-1')}}</p>
          <p class="body-1">
            {{$t('login.body-2.left')}}
            <b>{{$t('login.body-2.anonymous')}}</b>
            {{$t('login.body-2.right')}}
          </p>
        </v-col>
        <login-buttons />
      </v-row>
    </fade-transition>
  </v-container>
</template>
<script lang="ts">
import { defineComponent } from '@vue/composition-api'
import LoginButtons from '~/components/login/loginButtons.vue'

export default defineComponent({
  ...{ auth: 'guest' },
  components: { LoginButtons }
})
</script>
