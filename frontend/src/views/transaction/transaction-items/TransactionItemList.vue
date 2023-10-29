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
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id" @click="navigateToDetail(item.id)">
          <td>{{ item.item_type }}</td>
          <td>{{ item.item_name }}</td>
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
    const response = await axios.get('http://localhost:5000/api/v1/transactions/items');
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
</style>