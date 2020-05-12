<template>
  <div class="banner">
    <v-container fluid class="pa-0 abc">
      <v-row align-content="center" align="center" justify="center" no-gutters>
        <v-col md="6" cols="12" class="pa-0">
          <v-sheet class="full-height" tile elevation="0">
            <v-row justify="center" align="center" align-content="center" no-gutters>
              <i-btn>test</i-btn>
            </v-row>
          </v-sheet>
        </v-col>
        <v-col md="6" cols="12" class="pa-0">
          <i-sheet class="full-height" tile elevation="0">
            <v-row justify="center" align="center" align-content="center" no-gutters>
              <i-btn>test</i-btn>
            </v-row>
          </i-sheet>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'
export default defineComponent({})
</script>

<style lang="scss" scoped>
.banner {
  .theme--dark {
    background-color: map-get($map: $material-dark, $key: background);
  }
  .full-height {
    height: 100vh;
    .row {
      height: 100%;
    }
  }
}
</style>
