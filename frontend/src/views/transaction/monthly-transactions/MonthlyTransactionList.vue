<template>
  <div>
    <!-- Display a loading message while fetching data -->
    <div v-if="isLoading">
      {{ t('monthlyRecord.loading') }}
    </div>

    <!-- Display the list of monthly records in a table format -->
    <table v-else class="table">
      <thead>
        <tr>
          <th>{{ t('monthlyRecord.month') }}</th>
          <th class="desktop-only">{{ t('monthlyRecord.totalIncome') }}</th>
          <th class="desktop-only">{{ t('monthlyRecord.totalExpense') }}</th>
          <th>{{ t('monthlyRecord.balance') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(summary, month) in monthlySummaries" :key="month" @click="navigateToDetail(month)"
            :class="summary.balance >= 0 ? 'balance-positive' : 'balance-negative'">
          <td>{{ formatMonth(month) }}</td>
          <td class="desktop-only" :class="'income'">{{ formatCurrency(summary.totalIncome) }}</td>
          <td class="desktop-only" :class="'expense'">{{ formatCurrency(summary.totalExpense) }}</td>
          <td>{{ formatCurrency(summary.balance) }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Error message -->
    <div v-if="errorMessage">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import axios from 'axios';

const { t } = useI18n();
const router = useRouter();

const isLoading = ref(true);
const records = ref([]);
const errorMessage = ref('');

// 月別の収入と支出のサマリーを計算する
const monthlySummaries = computed(() => {
  const summaries = {};

  // `income_expense_item` リレーションを介して `item_type` を得る
  records.value.forEach(record => {
    const month = record.month; // "YYYYMM" 形式
    const item_type = record.item_type;
    const amount = parseFloat(record.amount);

    if (!summaries[month]) {
      summaries[month] = { totalIncome: 0, totalExpense: 0, balance: 0 };
    }

    if (item_type === 'income') {
      summaries[month].totalIncome += amount;
    } else {
      summaries[month].totalExpense += amount;
    }

    summaries[month].balance = summaries[month].totalIncome - summaries[month].totalExpense;
  });

  return summaries;
});

onMounted(async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/v1/transactions/monthly`);
    if (response.data.success) {
      records.value = response.data.transactions.map(t => ({
        ...t,
        month: t.month,
        amount: t.amount,
        income_expense_item: t.income_expense_item
      }));
    } else {
      errorMessage.value = t('monthlyRecord.fetchError');
    }
  } catch (error) {
    errorMessage.value = t('monthlyRecord.fetchError');
  } finally {
    isLoading.value = false;
  }
});

function navigateToDetail(month) {
  router.push({ name: 'monthly-transaction-upsert', params: { month } });
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ja-JP', { style: 'currency', currency: 'JPY' }).format(value);
};

const formatMonth = (monthString) => {
  const year = monthString.substring(0, 4);
  const month = monthString.substring(4, 6);
  return `${year}年${month}月`;
};

</script>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
}
.table th, .table td {
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
}
.table th {
  background-color: #f7f7f7;
}
.table tr:hover {
  background-color: #f5f5f5;
  cursor: pointer;
}
.table .income {
  color: #34a853; /* 緑色 */
}

.table .expense {
  color: #d32f2f; /* 赤色 */
}

.table .balance-positive {
  color: #34a853; /* 緑色 */
}
.table tr.balance-positive {
  background-color: #eaffea; /* プラスの収支の行の背景色（薄い緑色） */
}
.table .balance-negative {
  color: #d32f2f; /* 赤色 */
}
.table tr.balance-negative {
  background-color: #ffebee; /* マイナスの収支の行の背景色（薄い赤色） */
}
/* スマートフォン画面のスタイル */
@media (max-width: 768px) {
  .desktop-only {
    display: none;
  }
}
</style>
