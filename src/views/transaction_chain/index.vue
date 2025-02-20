<template>
  <div>
    <div class="dashboard-container">
      <div style="width: 1800px padding: 30 0 ">
        <div class="content" style="height:100%; padding: 0px 0px">
          <div class="row" style="display: flex; flex-wrap: nowrap;">
            <div class="custom-col-10" style="padding: 20;">
              <MacroView :end_date="end_date" :duration_days="duration_days"></MacroView>
            </div>
            <div class="custom-col-40" style="padding: 0;">
              <!-- <GraphView></GraphView> -->
            </div>
            <div class="custom-col-40" style="padding: 0;">
              <!-- <SankeyView></SankeyView>
              <LineView></LineView> -->
            </div>
          </div>
        </div>
      </div>
      <!-- <Article /> -->
    </div>
  </div>
</template>
<script>
import Mock from 'mockjs'
// import * as axios from 'axios'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import MacroView from './components/BondSelectionView/MacroView.vue'
// import LineView from './components/ChainView/LineView.vue'
// import SankeyView from './components/SankeyView'
// import GraphView from './components/GraphView/GraphView.vue'
// import Article from './Article.vue'
export default {
  name: '',
  components: {
    MacroView,
    GraphView,
    LineView,
    SankeyView
    // Article
  },
  data() {
    return {
      all_bond_list: false,
      selected_bond_id_list: [],
      selected_bond_list: [],
      end_date: '2023-07-05',
      duration_days: 1,
      transactionSummaryData: false,
      instnTypes: false
    }
  },
  computed: {
  },
  watch: {
    selected_bond_id_list(newSortByNum) {
      if (newSortByNum) {
        this.selected_bond_list = this.all_bond_list.filter(bond => this.selected_bond_id_list.includes(bond.Bond_cd))
      }
    }
  },
  created() {

  },

  mounted() {
    // this.all_bond_list = this.generateTransactionSummary()
    // axios.get('http://localhost:5003/api/bondSummaryData')
    //   .then(response => {
    //     const bondSummaryData = response.data.bondSummaryData
    //     this.all_bond_list = bondSummaryData
    //   })
    // axios.get('http://localhost:5003/api/institution_types')
    //   .then(response => {
    //     const data = JSON.parse(response.data.instn_dict)
    //     console.log('data:', data)
    //   })
    // this.$root.$on('ChangeBondSelection', (bond_cd) => {
    //   if (this.selected_bond_id_list.includes(bond_cd)) {
    //     this.selected_bond_id_list = this.selected_bond_id_list.filter(d => d !== bond_cd)
    //   } else {
    //     this.selected_bond_id_list.push(bond_cd)
    //   }
    // })
  },

  methods: {
    generateTransactionSummary() {
      const data = []
      for (let i = 1; i <= 50; i++) {
        const item = {
          'Bond_cd': i,
          'Bond_name': 'Name_' + Mock.Random.string('upper', 3, 4),
          'Transaction_num': Mock.Random.integer(0, 2000),
          'Transaction_volume': Mock.Random.float(0, 3000, 2, 2)
        }
        data.push(item)
        // console.log(item)
      }
      return data
    },

    randomDateInRange() {
      var startDate = new Date()
      var endDate = new Date()
      var randomTimestamp = Mock.Random.integer(startDate.getTime(), endDate.getTime())
      return new Date(randomTimestamp)
    }
  }
}
</script>

<style lang="scss" scoped>
.custom-col-10 {
    flex: 0 0 320px; /* 7.5vw is 10% of the viewport width when the scale is 75% */
    max-width: 320px;
}
.custom-col-40 {
    flex: 0 0 1050px; /* 30vw is 40% of the viewport width when the scale is 75% */
    max-width: 1050px;
}
.stand-alone-page {
  color: #333;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    Oxygen-Sans, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.5;
}
.dashboard {
  &-container {
    margin: 20px 0px 0px 35px;
  }
  &-text {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    font-size: 30px;
    line-height: 46px;
    color: #2c3e50;
  }
}
.toolbar-title {
  height: 28px;
  font-size: 15px;
  font-family: "Roboto", "Helvetica", "Arial", sans-serif;
  font-weight: 600;
  background: rgb(238, 238, 238);
  color: rgb(120, 120, 120);
  border-radius: 5px;
  padding-left: 10px;
  flex-shrink: 0;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}
.content {
  // background-color: $teal-600; /* 设置为与 .top-fill 相同的背景色 */
  padding: 30px; /* 将 padding 移到这里 */
  box-sizing: border-box; /* 确保 padding 不会增加元素的宽度和高度 */
  background-clip: content-box; /* 背景色仅填充内容框 */
  background-color: rgb(255, 255, 255)
}
.transparent-background {
  // background-color: $teal-600; /* 设置为与 .top-fill 相同的背景色 */
  padding: 30px; /* 将 padding 移到这里 */
  box-sizing: border-box; /* 确保 padding 不会增加元素的宽度和高度 */
  background-clip: content-box; /* 背景色仅填充内容框 */
  background-color: rgb(233, 223, 223);
  width: 100vw;
  box-sizing: border;
}
@import './Article.scss'
</style>
