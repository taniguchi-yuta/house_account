<template>
  <div class="charts">
    <div class="grid grid-cols-12 gap-6">
      <va-card class="chart-widget md:col-span-6 col-span-12">
        <va-card-title>{{ t('charts.monthlyTransactions') }}</va-card-title>
        <va-card-content>
          <va-chart :data="monthlyTransactionsData" type="bar" />
        </va-card-content>
      </va-card>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { useI18n } from 'vue-i18n';
  import { ref, onMounted } from 'vue';
  import VaChart from '@/components/va-charts/VaChart.vue'; // この行を再度追加

  const { t } = useI18n();
  
  const monthlyTransactionsData = ref({});

  onMounted(setDummyData);

  function setDummyData() {
    // ダミーデータをセット
    monthlyTransactionsData.value = {
      labels: ['January', 'February', 'March', 'April', 'May'], // サンプル月データ
      datasets: [
        {
          label: '入金',
          data: [1200, 1500, 1400, 1300, 1450], // サンプル入金データ
          borderColor: '#42A5F5',
          backgroundColor: '#42A5F5',
          fill: false
        },
        {
          label: '出金',
          data: [800, 900, 850, 870, 880], // サンプル出金データ
          borderColor: '#FF7043',
          backgroundColor: '#FF7043',
          fill: false
        }
      ]
    };
  }
</script>

<style lang="scss">
  .chart-widget {
    .va-card__content {
      height: 450px;
    }
  }
</style>
