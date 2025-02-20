<template>
  <div>
    <!-- 在这里使用你的组件，并传递数据 URL -->
    <chain />
  </div>
</template>

<script>
// import chain from '../TransactionChainView/chain.vue';

export default {
  components: {
    // TransactionChain
  },
  data() {
    return {
      dataUrl: 'data_chain.json', // 数据文件的 URL
      width: 1400, // SVG 宽度
      height: 800 // SVG 高度
    };
  }
};
</script>
