<template>
  <div>
    <b-card-header class="large-header" style="height:25px; padding: 20px 20px 2px 20px">
    </b-card-header>
    <b-card-body style=" height: 500px; padding:5px ; border: 0.5px solid rgba(204, 204, 204, 0.2)">
      <div id="canvas"></div>
    </b-card-body>
  </div>
</template>
<script>
/* eslint-disable */

// 导入外部 JavaScript 文件
// import './asset/d3.v3.min.js';
import './asset/showdown.min.js';
// import './asset/highlight.pack.js';
// 导入外部 CSS 样式表
import './css/highlightjs.css';
// import './css/global.css';
import * as axios from 'axios'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
const { format } = require('date-fns')
import { BCard, BIcon, BButton, BNavbar, BCardHeader, BCardBody, BDropdown, BDropdownItem, BIconGear, BDropdownGroup, BFormTags, BInputGroup, BInputGroupText, BFormInput, BButtonGroup, BButtonToolbar, BIconArrowUp, BIconArrowDown  } from 'bootstrap-vue'
import TransactionChain from '../ChainView/Transaction.vue'
// var Mock = require('mockjs')
// import Mock from 'mockjs';
// import SankeyDriver from './js/sankey.js'
import SankeyDriver from './js1/sankey-driver.js'
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
    TransactionChain,
    // sankey,
    // sankeydriver
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
    SankeyChart(){
      // var driver = new SankeyDriver();
      d3.json('asset/titanic-data.json', function(titanicData){
        console.log('titanicData:', titanicData);
        var margin = {
          top: 0, bottom: 10, left: 0, right: 10,
        };
        var size = {
          width: 960, height: 400,
        }
        // driver.prepare(d3.select("#canvas"), size, margin);
        // driver.draw(titanicData);
        // sendBeacon("sankey.draw");
      });
    },
    async getDataAndDraw() {
      try {
          const response = await axios.get('http://localhost:5003/api/transaction_sankey_data');
          const transaction_sankey_data = response.data;
          console.log('transaction_sankey_data:', transaction_sankey_data)
          var margin = {
            top: 0, bottom: 10, left: 0, right: 10,
          };
          var size = {
            width: 960, height: 400,
          }
          // const sankeyData = SankeyDriver
          const sankeyDriver = new SankeyDriver(); // 创建 sankeyDriver 实例
          console.log("sankeyDriver:", sankeyDriver)
          sankeyDriver.prepare(d3.select("#canvas"), size, margin)
          sankeyDriver.draw(transaction_sankey_data)
        } catch (error) {
          console.error('Error fetching data:', error);
        }
    },

  },
  created() {

  },
  mounted() {
    // this.getDataAndDraw()
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
