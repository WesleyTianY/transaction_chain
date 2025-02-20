<template>
  <div ref="lineupContainer"></div>
</template>

<script>
import LineUpJS from 'lineupjs';

export default {
  name: 'LineUp',
  props: {
    data: {
      type: Array,
      required: true
    }
  },
  mounted() {
    const lineupContainer = this.$refs.lineupContainer;
    LineUpJS.asLineUp(lineupContainer, this.data); // 在mounted钩子中使用LineUpJS
  }
}
</script>
