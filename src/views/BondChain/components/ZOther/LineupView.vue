<template>
  <div>
    <b-card-header class="large-header" style="height:25px; padding: 20px 20px 2px 20px">
    </b-card-header>
    <b-card-body style=" height: 375px; padding:5px ; border: 0.5px solid rgba(204, 204, 204, 0.2)">
      <!-- <LineUp :data="fakeData" /> -->
    </b-card-body>
  </div>
</template>

<script>
/* eslint-disable */
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { BCard, BCardHeader, BCardBody } from 'bootstrap-vue'
// import LineUp from './thelineup.vue';


export default {
  name: 'MacroView',
  components: {
    BCard,
    BCardHeader,
    BCardBody,
    // LineUp
  },
  data() {
    return {
      fakeData: this.generateFakeData()
    }
  },
  mounted() {
    console.log('mounted', this.fakeData)
  },
  computed: {
    filteredSlices() {
      return this.slices.filter(slice => {
        return slice.pr_cat.includes(this.filterText) || slice.gt_cat.includes(this.filterText);
      }).sort((a, b) => {
        const aValue = a[this.sortAttr];
        const bValue = b[this.sortAttr];
        if (this.sortType === 'asc') {
          return aValue > bValue ? 1 : -1;
        } else {
          return aValue < bValue ? 1 : -1;
        }
      });
    }
  },
  methods: {
    toggleSortType() {
      this.sortType = this.sortType === 'asc' ? 'desc' : 'asc';
    },
    applyFilter() {
      // 这里可以根据输入的筛选条件来更新数据展示
    },
    generateFakeData() {
      const arr = [];
      const cats = ['c1', 'c2', 'c3'];
      for (let i = 0; i < 100; ++i) {
        arr.push({
          a: Math.random() * 10,
          d: 'Row ' + i,
          cat: cats[Math.floor(Math.random() * 3)],
          cat2: cats[Math.floor(Math.random() * 3)],
        });
      }
      return arr;
    }

  }
}
</script>

<style scoped>
.large-header {
    padding: 5px 5px 5px 10px;
    font-size: 12px
}

.small-header {
    padding: 5px 5px 0px 20px;
    height: 33px
}
.slices-content {
    height: calc(100% - 2px);
    background: rgb(255, 255, 255);
    border: 1px solid #c1c1c1;
    border-radius: 5px;
}

.slices-data-content {
    height: calc(100% - 60px);
    display: block;
    overflow-x: hidden;
    overflow-y: auto;
}

.slices-data-content::-webkit-scrollbar {
    display: none;
}
</style>
