<template>
  <div>
    <b-card no-body style="height:100%;">
      <b-card-header class="large-header" style="height:230px; padding: 5px 20px 0px 20px">
        <div style="display:flex; margin-top: 10px;">
          <span style="font-size: 15px;"><b>Bond List View</b></span>
          <b-dropdown dropright size="sm" variant="outline-secondary" style="margin-left: 20px; height: 15px; display: flex; align-items: center;" toggle-class="text-decoration-none">
            <template v-slot:button-content>
              <b-icon-gear style="font-size: 12px; height: 16px; width: 20px;" />
            </template>
            <div style="width:150px; margin-left: 10px; font-size: 12px;">
              Bond price Threshold1
              <vue-slider
                v-model="Threshold_local"
                :min="1"
                :max="4"
                :interval="0.5"
                :marks="true"
                style="margin-left:20px; margin-right:10px; margin-bottom:30px"
              ></vue-slider>
            </div>
          </b-dropdown>
        </div>
        <div style="display:flex; margin-top: 10px; float: left;">
          <el-date-picker
            v-model="date"
            type="date"
            placeholder="Pick a day"
          />
          <button class="btn btn-secondary button" style="margin-right: 10px;" @click="timeClick(date)">
            OK
          </button>
        </div>
        <div style="display:flex; margin-top: 10px; float: left;">
          <span style="font-size: 12px;">Trans num</span>
          <vue-slider
            v-model="transaction_num_range"
            :adsorb="true"
            :data="transaction_num_range_list"
            :included="true"
            style="width: 150px; margin-left: 20px;"
          ></vue-slider>
        </div>
        <div style="display:flex; margin-top: 10px; float: left;">
          <span style="margin-top: 5px">Sort by number</span>
          <b-button-group size="sm" style="margin-left: 10px; float: right;">
            <b-button variant="outline-secondary" style="font-size: 12px; height: 25px; margin-left: 24px; float: right;" @click="updateNumSort('num_descending')"><b-icon-arrow-down></b-icon-arrow-down></b-button>
            <b-button variant="outline-secondary" style="font-size: 12px; height: 25px;" @click="updateNumSort('num_ascending')"><b-icon-arrow-up></b-icon-arrow-up></b-button>
          </b-button-group>
        </div>
        <div style="display:flex; margin-top: 10px; float: left;">
          <span style="font-size: 12px; float: left;">Trans vol</span>
          <vue-slider
            v-model="transaction_volume_range"
            :adsorb="true"
            :data="transaction_volume_range_list"
            :included="true"
            style="width: 150px; margin-left: 27px;"
          ></vue-slider>
        </div>
        <div style="display:flex; margin-top: 10px; float: left;">
          <span style="margin-top: 5px">Sort by volume</span>
          <b-button-group size="sm" style="margin-left: 10px; float: right;">
            <b-button variant="outline-secondary" style="font-size: 12px; height: 25px; margin-left: 24px; float: right;" @click="updateVolSort('vol_descending')"><b-icon-arrow-down></b-icon-arrow-down></b-button>
            <b-button variant="outline-secondary" style="font-size: 12px; height: 25px;" @click="updateVolSort('vol_ascending')"><b-icon-arrow-up></b-icon-arrow-up></b-button>
          </b-button-group>
        </div>
      </b-card-header>
      <b-card-body style="overflow: scroll; height: 870px; padding:2px">
        <div style="display: flex; flex-direction: column;">
          <!-- Search Module -->
          <div style="flex: 1;">
            <div style="display:block; height:20px; margin-top: 0px; float: right;">
              <b-input-group size="sm" style="width:278px">
                <b-form-input v-model="searchQuery" placeholder="Search by Name or ID">
                </b-form-input>
                <template #append>
                  <b-input-group-text style="float: right;">
                    <svg width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                      <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                    </svg>
                  </b-input-group-text>
                </template>
              </b-input-group>
            </div>
          </div>

          <!-- List Module -->
          <div style="flex: 1; margin-top: 13px">
            <div v-if="marcoDataLoaded">
              <div style="font-size: 12px;">Transaction Num Range: {{ transaction_num_range[0] }} - {{ transaction_num_range[1] }}</div>
              <div style="font-size: 12px;">Transaction Volume Range: {{ transaction_volume_range[0] }} - {{ transaction_volume_range[1] }}</div>
              <div style="font-size: 12px;">Filtered Projects Count: {{ filteredAndSortedProjects.length }}</div>
              <!-- <MarcoCard v-for="bond in this.bond_list" :key="bond.Bond_cd" :bond_cd="bond.Bond_cd" :bond_name="bond.Bond_name" :transaction_num="bond.Transaction_num" :transaction_volume="bond.Transaction_volume" :duration_days="duration_days" :end_date="end_date" /> -->
              <MarcoCard v-for="bond in filteredAndSortedProjects" :key="bond.Bond_cd" :bond_cd="bond.Bond_cd" :bond_name="bond.Bond_name" :transaction_num="bond.Transaction_num" :transaction_volume="bond.Transaction_volume" :duration_days="duration_days" :end_date="end_date" />
            </div>
          </div>
        </div>
      </b-card-body>
    </b-card>
  </div>
</template>
<script>
/* eslint-disable */
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
import * as axios from 'axios'
const { format } = require('date-fns')
import { BCard, BIcon, BButton, BNavbar, BCardHeader, BCardBody, BDropdown, BDropdownItem, BIconGear, BDropdownGroup, BFormTags, BInputGroup, BInputGroupText, BFormInput, BButtonGroup, BButtonToolbar, BIconArrowUp, BIconArrowDown  } from 'bootstrap-vue'
import MarcoCard from './MarcoCard.vue'
import { fetchBondSummaryData } from '../../../../api/bond.js';
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
    MarcoCard,
    BButtonGroup,
    BButtonToolbar
    // MacroGlyph,
    // BFormRadioGroup
  },
  props: ['all_bond_list', 'end_date', 'duration_days'],
  data() {
    return {
      // isLoading: true,
      bond_list : null,
      transaction_num_range : ["0", "2000"],
      transaction_volume_range: ["1000", "50000"],
      transaction_num_range_list: ["0", "3", "5", "10", "100", "1000", "2000"],
      transaction_volume_range_list: ["1000", "3000", "5000", "8000", "10000", "20000", "50000"],
      Threshold_local: 1,
      sortByNum : "",
      sortByVol : "",
      isSortByNumSelected: false,
      isSortByVolSelected: false,
      filteredBonds : null,
      searchQuery: "",
      date: null,
      marcoDataLoaded: false
    }
  },
  methods: {
    // fetchData() {
    //   const queryDate = this.date ? this.date.toISOString().slice(0, 10) : this.end_date
    //   const url = `http://localhost:5003/api/getAllData/${queryDate}`
    //   console.log('fetchData', url)
    //   fetch(url)
    //     .then(response => {
    //       if (!response.ok) {
    //         // Log the response status and text for further diagnosis
    //         return response.text().then(text => {
    //           throw new Error(`Fetch error: ${response.status} ${response.statusText} - ${text}`);
    //         });
    //       }
    //       return response.json();
    //     })
    //     .then(data => {
    //       console.log('Success:', data);
    //       this.bond_list = data.bondSummaryData;
    //     })
    //     .catch(error => {
    //       console.error('There was a problem with the fetch operation:', error);
    //     });
    // },
    async fetchData(queryDate) {
      try {
        console.log('queryDate', queryDate)
        const data = await fetchBondSummaryData(queryDate);
        console.log('data', data)
        this.bond_list = data;
        this.$emit('data-loaded', this.bond_list);
        this.marcoDataLoaded = true;
        console.log('Data loaded:', data);
      } catch (error) {
        console.error('Error fetching bond summary data:', error);
      } finally {
        this.isLoading = false;
      }
    },
    timeClick(date) {
        const queryDate = date.toISOString().slice(0, 10)
        // setQueryDate(queryDate)
        this.fetchData(queryDate)
        // fetch(url)
        //   .then(response => {
        //     if (!response.ok) {
        //       // Log the response status and text for further diagnosis
        //       return response.text().then(text => {
        //         throw new Error(`Fetch error: ${response.status} ${response.statusText} - ${text}`);
        //       });
        //     }
        //     return response.json();
        //   })
        //   .then(data => {
        //     console.log('Success:', data);
        //     this.bond_list = data.bondSummaryData;
        //   })
        //   .catch(error => {
        //     console.error('There was a problem with the fetch operation:', error);
        //   });
        // alert(`Selected Time Range: ${startTime} to ${endTime}`);
    },
    updateNumSort(sortValue){
      this.sortByNum = sortValue
      this.isSortByNumSelected = true
      console.log(this.sortByNum)
    },

    updateVolSort(sortValue){
      this.sortByVol = sortValue
      this.isSortByVolSelected = true
      console.log(this.sortByVol)
    },

  },
  created() {
    this.bond_list = this.all_bond_list
  },
  mounted() {
    
  },
  watch: {
    sortByNum(newSortByNum) {
      if (newSortByNum) {
        this.isSortByNumSelected = true;
        this.isSortByVolSelected = false;
      }
    },
    sortByVol(newSortByVol) {
      if (newSortByVol) {
        this.isSortByVolSelected = true;
        this.isSortByNumSelected = false;
      }
    },
    marcoDataLoaded(newValue) {
      if (newValue) {
        console.log('marcoDataLoaded 已更新为 true，开始渲染 MarcoCard 组件');
        // 这里可以执行额外的逻辑
      }
    }
  },
  computed: {
    // 计算属性用于筛选项目
    filteredAndSortedProjects() {
      // 将字符串数组转换为整数数组
      const transaction_num_range_intArray = this.transaction_num_range.map(str => parseInt(str));
      const transaction_volume_range_intArray = this.transaction_volume_range.map(str => parseInt(str));

      const minTransactionNum = Math.min(...transaction_num_range_intArray);
      const maxTransactionNum = Math.max(...transaction_num_range_intArray);
      const minTransactionVolume = Math.min(...transaction_volume_range_intArray);
      const maxTransactionVolume = Math.max(...transaction_volume_range_intArray);

      this.filteredBonds = this.bond_list.filter((bond) => {
        const passTransactionNum = bond.Transaction_num >= minTransactionNum && bond.Transaction_num < maxTransactionNum;
        const passTransactionVol = bond.Transaction_volume >= minTransactionVolume && bond.Transaction_volume < maxTransactionVolume;

        return passTransactionNum && passTransactionVol;
      })

      if (!this.sortByNum && !this.sortByVol) {
        return this.filteredBonds; // No sorting logic applied
      }

      let sortedBonds = [...this.filteredBonds];// Create a shallow copy to avoid modifying original array
      sortedBonds = sortedBonds.filter((bond) => {
        const bondCdString = bond.Bond_cd.toString(); // Convert Bond_cd to string
        return bond.Bond_name.toLowerCase().includes(this.searchQuery.toLowerCase()) || bondCdString.toLowerCase().includes(this.searchQuery.toLowerCase())
      })

      if (this.isSortByNumSelected) {
        if (this.sortByNum === "num_descending") {
          sortedBonds.sort((a, b) => a.Transaction_num - b.Transaction_num)
        } else if (this.sortByNum === "num_ascending") {
          sortedBonds.sort((a, b) => b.Transaction_num - a.Transaction_num)
        }
      }


      if (this.isSortByVolSelected) {
        if (this.sortByVol === "vol_descending") {
          sortedBonds.sort((a, b) => a.Transaction_volume - b.Transaction_volume)
        } else if (this.sortByVol === "vol_ascending") {
          sortedBonds.sort((a, b) => b.Transaction_volume - a.Transaction_volume)
        }
      }

      return sortedBonds
    }
  }
}
</script>
<style scoped>
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
