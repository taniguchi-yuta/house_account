<template>
  <div>
    <!-- Display a loading message while fetching data -->
    <div v-if="isLoading">
      {{ t('transaction.loading') }}
    </div>

    <!-- Display the list of transactions in a table format -->
    <table v-else class="table">
      <thead>
        <tr>
          <th>{{ t('transaction.itemType') }}</th>
          <th>{{ t('transaction.itemName') }}</th>
          <th>{{ t('transaction.transactionDay') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id" @click="navigateToDetail(item.id)"
        :class="[
            item.item_type === 'income' ? 'income-row' : 'expense-row',
            !item.is_active ? 'inactive-row' : '', // is_active データに基づいてクラスを設定
          ]">
          <td>{{ item.item_type }}</td>
          <td>{{ item.item_name }}</td>
          <td>{{ item.transaction_day }}日</td>
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
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import axios from 'axios';

const { t } = useI18n();
const router = useRouter();

const isLoading = ref(true);
const items = ref([]);
const errorMessage = ref('');

onMounted(async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/v1/transactions/items`);
    if (response.data.status === 'success') {
      items.value = response.data.items;
    } else {
      errorMessage.value = t('transaction.fetchError');
    }
  } catch (error) {
    errorMessage.value = t('transaction.fetchError');
  } finally {
    isLoading.value = false;
  }
});

function navigateToDetail(itemId: number) {
  router.push({ name: 'transaction-item-upsert', params: { id: itemId } }); // Assuming the route name for detail page is 'itemDetail'
}
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
.income-row {
  background-color: #eaffea; /* totalBalanceColorのbg-green-100に相当する色 */
  color: #34a853; /* totalBalanceTextColorのtext-green-800に相当する色 */
}

.expense-row {
  background-color: #ffebee; /* totalBalanceColorのbg-red-100に相当する色 */
  color: #d32f2f; /* totalBalanceTextColorのtext-red-800に相当する色 */
}

.inactive-row {
  background-color: #f2f2f2; /* グレーアウトの背景色を変更 */
  color: #888888; /* グレーアウトのテキストカラーを変更 */
  opacity: 0.7; /* グレーアウトの透明度を調整 */
  cursor: not-allowed; /* グレーアウト時のカーソルを変更 */
}
</style>