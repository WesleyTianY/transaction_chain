<template>
  <b-card no-body>
    <b-card-header class="small-header" style="font-size:12px; padding:2px 2px; height:26px">
      {{ bond_cd }}
      <b>Num:</b> {{ transaction_num }}
      <b>Name:</b> {{ bond_name }}
      <!-- <b>Vol:</b> {{ transaction_volume }} -->
      <b-button v-if="!selected" size="sm" variant="outline" style="float: right; padding: 0" @click="onClick">
        <b-icon-plus-square />
      </b-button>
      <b-button v-if="selected" size="sm" variant="outline" style="float: right; padding: 0" @click="onClick">
        <b-icon-dash-square />
      </b-button>
    </b-card-header>
    <!-- <svg v-if="item.value" :ref="'chart-' + index" width="100" height="20" /> -->
    <b-card-body :id="'mg_'+bond_cd" style="padding: 2px">
      <MarcoGlyph :bond_cd="bond_cd" :end_date="end_date" :duration_days="duration_days" />
    </b-card-body>
  </b-card>
</template>

<script>
// import { defineComponent } from '@vue/composition-api'
// import * as axios from 'axios'
// eslint-disable-next-line
import * as d3 from 'd3'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
// eslint-disable-next-line
import { BCard, BCardBody, BCardHeader, BIconPlusSquare, BIconDashSquare, BButton } from 'bootstrap-vue'
import MarcoGlyph from './MarcoGlyph.vue'
// eslint-disable-next-line
// import { RadarChart } from '../assets/RadarChart'

export default {
  name: 'MacroCard',
  components: {
    BCard,
    BButton,
    BCardBody,
    BIconPlusSquare,
    BIconDashSquare,
    BCardHeader,
    MarcoGlyph
  },
  // eslint-disable-next-line
  props: ['bond_cd', 'bond_name', 'transaction_num', 'transaction_volume', 'duration_days', 'end_date'],
  data() {
    return {
      selected: false
      // dataPackages: false
    }
  },
  mounted() {

  },
  methods: {
    onClick() {
      this.selected = !this.selected
      this.$root.$emit('ChangeBondSelection', this.bond_cd)
    }
  }
}
</script>
