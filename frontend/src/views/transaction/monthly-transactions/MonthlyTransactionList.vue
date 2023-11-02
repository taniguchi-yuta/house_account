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
          <th>{{ t('monthlyRecord.userId') }}</th>
          <th>{{ t('monthlyRecord.incomeExpenseItemId') }}</th>
          <th>{{ t('monthlyRecord.month') }}</th>
          <th>{{ t('monthlyRecord.amount') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="record in records" :key="record.id" @click="navigateToDetail(record.id)">
          <td>{{ record.user_id }}</td>
          <td>{{ record.income_expense_item_id }}</td>
          <td>{{ record.month }}</td>
          <td>{{ record.amount }}</td>
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
const records = ref([]);
const errorMessage = ref('');

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/v1/monthly-records');
    if (response.data.status === 'success') {
      records.value = response.data.records;
    } else {
      errorMessage.value = t('monthlyRecord.fetchError');
    }
  } catch (error) {
    errorMessage.value = t('monthlyRecord.fetchError');
  } finally {
    isLoading.value = false;
  }
});

function navigateToDetail(recordId: number) {
  router.push({ name: 'monthly-record-detail', params: { id: recordId } }); // Assuming the route name for the detail page is 'monthly-record-detail'
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
</style>
