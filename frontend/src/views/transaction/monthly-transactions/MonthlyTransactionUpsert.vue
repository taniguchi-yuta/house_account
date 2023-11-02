<template>
  <form @submit.prevent="onSubmit">
    <div>
      <va-input
        v-model="month"
        class="mb-4"
        :label="t('transaction.month')"
        :error="!!monthErrors.length"
        :error-messages="monthErrors"
      />
    </div>

    <div class="flex">
      <div class="w-1/2 pr-2">
        <label>{{ t('transaction.income') }}</label>
        <va-input
          v-model="incomeName"
          class="mb-2"
          :label="t('transaction.itemName')"
          :error="!!itemNameErrors.length"
          :error-messages="itemNameErrors"
        />
        <va-input
          v-model="incomeAmount"
          class="mb-2"
          type="number"
          :label="t('transaction.amount')"
          :error="!!amountErrors.length"
          :error-messages="amountErrors"
        />
      </div>
      <div class="w-1/2 pl-2">
        <label>{{ t('transaction.expense') }}</label>
        <va-input
          v-model="expenseName"
          class="mb-2"
          :label="t('transaction.itemName')"
          :error="!!itemNameErrors.length"
          :error-messages="itemNameErrors"
        />
        <va-input
          v-model="expenseAmount"
          class="mb-2"
          type="number"
          :label="t('transaction.amount')"
          :error="!!amountErrors.length"
          :error-messages="amountErrors"
        />
      </div>
    </div>

    <div class="mt-4">
      <label>{{ t('transaction.summary') }}</label>
      <div class="bg-gray-100 p-4 rounded">
        <p>{{ t('transaction.totalIncome') }}: {{ totalIncome }}</p>
        <p>{{ t('transaction.totalExpense') }}: {{ totalExpense }}</p>
        <p>{{ t('transaction.balance') }}: {{ totalBalance }}</p>
      </div>
    </div>

    <div class="flex justify-center mt-4">
      <va-button class="my-0" @click="onSubmit">{{ t('transaction.save') }}</va-button>
    </div>

    <!-- Success Messages Display -->
    <div v-if="successMessage">
      <p>{{ successMessage }}</p>
    </div>

    <!-- Error Messages Display -->
    <div v-if="errors && errors.length">
      <ul>
          <li v-for="error in errors" :key="error">{{ error }}</li>
        </ul>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue';
import axios from 'axios';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const month = ref('');
const incomeName = ref('');
const expenseName = ref('');
const incomeAmount = ref(0);
const expenseAmount = ref(0);
const monthlyTransaction = ref(null);
const errors = ref([]);
const successMessage = ref(null);

const monthErrors = ref([]);
const itemNameErrors = ref([]);
const amountErrors = ref([]);

const totalIncome = ref(0);
const totalExpense = ref(0);

const totalBalance = computed(() => {
  return totalIncome.value - totalExpense.value;
});

watch(incomeAmount, (newValue) => {
  totalIncome.value = parseFloat(newValue) || 0;
});

watch(expenseAmount, (newValue) => {
  totalExpense.value = parseFloat(newValue) || 0;
});

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/v1/transactions/monthly');

    if (response.data && response.data.success) {
      if (response.data.transactions.length > 0) {
        const transaction = response.data.transactions[0];
        month.value = transaction.month;
        incomeName.value = transaction.item_name; 
        incomeAmount.value = parseFloat(transaction.amount);
      } else {
        // トランザクションがない場合の処理をここに記述します
        console.log('トランザクションのデータがありません。');
      }
    } else {
      errors.value = response.data.errors || ["予期しないエラーが発生しました。"];
    }
  } catch (error) {
    errors.value = ["APIからのデータ取得中にエラーが発生しました。"];
  }
});

async function onSubmit() {
  try {
    const requestData = {
      month: month.value,
      incomeName: incomeName.value,
      expenseName: expenseName.value,
      incomeAmount: incomeAmount.value,
      expenseAmount: expenseAmount.value,
    };

    const response = await axios.post('/api/monthlyTransactionUpdate', requestData);

    if (response.data && response.data.success) {
      successMessage.value = ["データが正常に保存されました。"];
    } else {
      errors.value = response.data.errors || ["予期しないエラーが発生しました。"];
      successMessage.value = null;
    }
  } catch (error) {
    errors.value = ["APIへのデータ送信中にエラーが発生しました。"];
    successMessage.value = null;
  }
}
</script>
