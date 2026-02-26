import GridLayout from './GridLayout.vue'
import GanttChart from './GanttChart.vue'

export {
  GridLayout,
  GanttChart
}

export default {
  install(app) {
    app.component('GridLayout', GridLayout)
    app.component('GanttChart', GanttChart)
  }
}
