<template>
  <div>
    <!-- 月のフィルタリング -->
    <div class="mb-4 d-flex align-items-center">
      <label class="mr-2">{{ t('transaction.month') }}</label>
      <input v-model="filterMonth" @input="fetchTransactions" />
    </div>

    <!-- 一覧表示 -->
    <table class="table-bordered w-100">
      <thead>
        <tr>
          <th class="p-2">{{ t('transaction.month') }}</th>
          <th class="p-2">{{ t('transaction.amount') }}</th>
          <th class="p-2">{{ t('transaction.itemName') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="transaction in transactions" :key="transaction.id">
          <td class="p-2">{{ transaction.month }}</td>
          <td class="p-2">{{ transaction.amount }}</td>
          <td class="p-2">{{ transaction.itemName }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const filterMonth = ref(''); // ユーザーが入力した月を保持する
const transactions = ref([]); // APIから取得した取引のリスト

onMounted(fetchTransactions);

function fetchTransactions() {
  // ここでAPIを呼び出してデータを取得
  // 例: transactions.value = await getMonthlyTransactions(filterMonth.value);

  // 仮のデータを設定
  transactions.value = [
    { id: 1, month: '2023-01', amount: 1000, itemName: '食費' },
    // ... その他のデータ
  ];
}
</script>
