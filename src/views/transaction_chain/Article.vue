<template>
  <div class="page">

    <div id="top" class="top">
      <div class="top-fill" />
    </div>

    <div class="article appeal-article">
      <h2>ProxyChainVis</h2>
      <p>银行间市场代持链路可视分析是一种通过可视化工具或技术来探索银行间市场代持交易的相关数据，以便更好地理解和分析这些交易链路的方法。它包括债券选择、机构探索和链路追踪三个模块。</p>
      <p><span class="teal">ProxyChainVis</span> 是一个专为银行间市场代持交易链路可视分析而设计的工具。它提供了债券选择(bond selection)、机构探索(institution exploration)和链路追踪(chain tracking)三个模块，帮助用户更好地理解债券市场，发现潜在的问题和机会，为市场监管和风险管理提供重要参考。</p>

      <h2 id="tutorial">How to Use <span class="teal">ProxyChainVis</span> as an End-user?</h2>
      <p>作为最终用户，您可以通过以下步骤使用<span class="teal">ProxyChainVis</span>：</p>
      <ol>
        <li>在债券选择模块中，根据您的需求选择和筛选债券。</li>
        <li>在机构探索模块中，探索不同机构在债券市场中的参与情况和地理分布。</li>
        <li>在链路追踪模块中，追踪债券交易的路径和关联关系，深入理解债券市场的交易流程。</li>
      </ol>
      <p>通过这些步骤，您可以充分利用<span class="teal">ProxyChainVis</span>，更好地理解债券市场并做出相应的决策。</p>

      <h2 id="tutorial">Data Processing</h2>
      <p>在链路可视分析中，数据处理是一个关键步骤。它涉及收集、清洗、转换和整理原始数据，以便后续的分析和可视化。在数据处理阶段，我们会执行以下操作：</p>
      <ol>
        <li>数据收集：从不同的数据源获取相关数据，包括交易记录、债券信息、机构数据等。</li>
        <li>数据清洗：处理数据中的错误、缺失值和重复项，确保数据的准确性和完整性。</li>
        <li>数据转换：将数据转换为适合分析和可视化的格式，例如将日期格式转换为统一格式，或者将数据转换为可视化工具支持的格式。</li>
        <li>数据整理：将清洗和转换后的数据进行整理和归类，以便后续的分析和可视化操作。</li>
      </ol>

      <h2 id="tutorial">Visualization Design</h2>
      <p>可视化设计是链路可视分析的关键环节，它帮助用户直观地理解数据并发现潜在的模式和关系。在可视化设计中，我们考虑以下几个方面：</p><br>
      <ol>
        <li>图表选择：选择适合展示数据的图表类型，例如折线图、柱状图、饼图等。</li>
        <li>颜色使用：合理运用颜色来突出重点数据，并确保色彩搭配清晰易懂。</li>
        <li>布局设计：设计清晰的布局，使用户能够轻松地理解和比较数据。</li>
        <li>交互功能：添加交互功能，如鼠标悬停、筛选器等，增强用户体验并提供更深入的数据探索。</li>
        <li>可视化优化：不断优化可视化效果，以提高数据传达的效率和效果。</li>
      </ol>
    </div>

  </div>

</template>

<script>
import './define.scss'

export default {
  data() {
    return {
      // 假设datasets包含了表格中的数据
      datasets: [

      ]
    }
  }
}
</script>

<style lang="scss" scoped>
@import './Article.scss'; // 导入样式文件
</style>
