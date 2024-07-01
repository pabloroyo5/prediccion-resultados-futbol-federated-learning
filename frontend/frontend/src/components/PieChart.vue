<template>
  <v-card class="mx-auto" max-width="400">
    <Pie :data="chartData" :options="options" />
  </v-card>
</template>

<script>
import { defineComponent, ref, watch } from 'vue';
import { Pie } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(Title, Tooltip, Legend, ArcElement, ChartDataLabels);

export default defineComponent({
  name: 'PieChart',
  components: {
    Pie
  },
  props: {
    probabilities: {
      type: Array,
      required: true,
    },
    labels: {
      type: Array,
      required: true,
    }
  },
  setup(props) {
    const colors = {
      min: '#B2DFDB', // Color más claro
      mid: '#26A69A', // Color intermedio
      max: '#00695C'  // Color más oscuro
    };

    // Función para asignar colores según las probabilidades
    function getBackgroundColor(probabilities) {
      const sortedIndices = [...probabilities.keys()].sort((a, b) => probabilities[a] - probabilities[b]);

      const backgroundColors = [];
      probabilities.forEach((_, index) => {
        if (index === sortedIndices[0]) {
          backgroundColors.push(colors.min); // Color más claro
        } else if (index === sortedIndices[1]) {
          backgroundColors.push(colors.mid); // Color intermedio
        } else if (index === sortedIndices[2]) {
          backgroundColors.push(colors.max); // Color más oscuro
        }
      });
      return backgroundColors;
    }

    const chartData = ref({
      labels: props.labels,
      datasets: [{
        backgroundColor: getBackgroundColor(props.probabilities),
        data: props.probabilities
      }]
    });

    const options = ref({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const value = context.raw;
              return `${(value * 100).toFixed(2)}%`;
            }
          }
        },
        datalabels: {
          color: 'white',
          formatter: function(value, context) {
            return `${(value * 100).toFixed(2)}%`;
          }
        }
      }
    });

    watch(() => [props.probabilities, props.labels], ([newProbabilities, newLabels]) => {
      chartData.value.datasets[0].data = newProbabilities;
      chartData.value.labels = newLabels;
      chartData.value.datasets[0].backgroundColor = getBackgroundColor(newProbabilities);
    });

    return {
      chartData,
      options
    };
  }
});
</script>

<style scoped>
.v-card {
  padding: 20px;
}
</style>