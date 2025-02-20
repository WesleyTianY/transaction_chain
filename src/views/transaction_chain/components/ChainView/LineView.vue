<template>
  <div>
    <b-card-header class="large-header" style="height:25px; padding: 20px 20px 2px 20px">
    </b-card-header>
    <b-card-body style="overflow: scroll; height: 500px; padding:5px ; border: 0.5px solid rgba(204, 204, 204, 0.2)">
      <TransactionChain></TransactionChain>
    </b-card-body>
  </div>
</template>
<script>
/* eslint-disable */
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
const { format } = require('date-fns')
import { BCard, BIcon, BButton, BNavbar, BCardHeader, BCardBody, BDropdown, BDropdownItem, BIconGear, BDropdownGroup, BFormTags, BInputGroup, BInputGroupText, BFormInput, BButtonGroup, BButtonToolbar, BIconArrowUp, BIconArrowDown  } from 'bootstrap-vue'
import TransactionChain from './Transaction.vue'
// var Mock = require('mockjs')
import Mock from 'mockjs';
export default {
  name: 'MacroView',
  components: {
    BCard,
    BIcon,
    BIconArrowUp, 
    BIconArrowDown,
    BButton,
    BCardHeader,
    BCardBody,
    BNavbar,
    BDropdown,
    BDropdownGroup,
    BDropdownItem,
    BIconGear,
    BFormTags,
    VueSlider,
    BInputGroup,
    BInputGroupText,
    BFormInput,
    BButtonGroup,
    BButtonToolbar,
    TransactionChain
    // TransactionChain
    // MacroGlyph,
    // BFormRadioGroup
  },
  props: [],
  data() {
    return {

    }
  },
  methods: {


  },
  created() {

  },
  mounted() {

  },
  watch: {

  },
  computed: {
    // 计算属性用于筛选项目

  }
}
</script>
<style>
.large-header{
    padding: 5px 5px 5px 10px;
    /* height: 5px; */
    font-size: 12px
}

.small-header{
    padding: 5px 5px 0px 20px;
    height: 33px
}

</style>
