<template>
  <form @submit.prevent="onSubmit">
    <div class="flex items-center">
      <div class="pr-2">
        <select v-model="selectedYear" @change="updateMonthValue" class="border rounded p-1">
          <option v-for="year in yearOptions" :key="year" :value="year">{{ year }}</option>
        </select>
        <label class="pr-2">年</label>
      </div>
      <div class="pl-2">
        <select v-model="selectedMonth" @change="updateMonthValue" class="border rounded p-1">
          <option v-for="month in monthOptions" :key="month" :value="month">{{ month }}</option>
        </select>
        <label class="pr-2">月</label>
      </div>
    </div>

    <div class="flex justify-between -mx-2">
      <!-- Income Section -->
      <div class="w-1/2 px-2">
      <label>{{ t('transaction.income') }}</label>
        <div v-for="incomeTransaction in incomeTransactions" :key="incomeTransaction.id" class="mb-4 flex">
          <div class="w-1/2 pr-1">
            <select v-model="incomeTransaction.selectedIncomeName" class="border rounded p-1 w-full">
              <option v-for="itemName in incomeItemNames" :key="itemName" :value="itemName">
                {{ itemName }}
              </option>
            </select>
          </div>
          <div class="w-1/2 pl-1">
            <va-input
              v-model="incomeTransaction.incomeAmount"
              type="number"
              :label="t('transaction.amount')"
              :error="!!amountErrors.length"
              :error-messages="amountErrors"
            />
          </div>
        </div>
      </div>

      <!-- Expense Section -->
      <div class="w-1/2 px-2">
      <label>{{ t('transaction.expense') }}</label>
        <div v-for="expenseTransaction in expenseTransactions" :key="expenseTransaction.id" class="mb-4 flex">
          <div class="w-1/2 pr-1">
            <select v-model="expenseTransaction.selectedExpenseName" class="border rounded p-1 w-full">
              <option v-for="itemName in expenseItemNames" :key="itemName" :value="itemName">
                {{ itemName }}
              </option>
            </select>
          </div>
          <div class="w-1/2 pl-1">
            <va-input
              v-model="expenseTransaction.expenseAmount"
              type="number"
              :label="t('transaction.amount')"
              :error="!!amountErrors.length"
              :error-messages="amountErrors"
            />
          </div>
        </div>
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
import { VaDatePicker } from 'vuestic-ui';

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

const currentDate = new Date();
const currentYear = currentDate.getFullYear();
const selectedYear = ref(currentYear); // 現在の年をデフォルトとして設定

const selectedMonth = ref(new Date().getMonth() + 1); // 1から12の範囲で
const yearOptions = Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - i); // 今の年から10年前までのオプション
const monthOptions = Array.from({ length: 12 }, (_, i) => i + 1); // 1から12の月のオプション

const monthlyTransactions = ref([]);
// 入出金事項の一覧を保存するためのref
const transactionItems = ref([]);

const updateMonthValue = () => {
  month.value = `${selectedYear.value}${String(selectedMonth.value).padStart(2, '0')}`;
};

const totalBalance = computed(() => {
  return totalIncome.value - totalExpense.value;
});

watch(incomeAmount, (newValue) => {
  totalIncome.value = parseFloat(newValue) || 0;
});

watch(expenseAmount, (newValue) => {
  totalExpense.value = parseFloat(newValue) || 0;
});

watch([selectedYear, selectedMonth], () => {
    month.value = `${selectedYear.value}${String(selectedMonth.value).padStart(2, '0')}`;
    fetchMonthlyTransactions();
  });

const fetchMonthlyTransactions = async () => {
    try {
      // Convert month to 'YYYYMM' format
      const monthParam = `${selectedYear.value}${String(selectedMonth.value).padStart(2, '0')}`;
      const response = await axios.get('http://localhost:5000/api/v1/transactions/monthly', {
        params: {
          month: monthParam
        }
      });

      if (response.data && response.data.success) {
        // Map each transaction to include a selected income and expense name
        monthlyTransactions.value = response.data.transactions.map(t => {
          return {
            ...t,
            selectedIncomeName: t.item_type === 'income' ? t.item_name : incomeItemNames.value[0], // Use existing value or default
            selectedExpenseName: t.item_type === 'expense' ? t.item_name : expenseItemNames.value[0], // Use existing value or default
            incomeAmount: t.item_type === 'income' ? t.amount : 0, // Set amount for income
            expenseAmount: t.item_type === 'expense' ? t.amount : 0, // Set amount for expense
          };
        });
      } else {
        errors.value = response.data.errors || ["予期しないエラーが発生しました。"];
      }
    } catch (error) {
      if (error.response && error.response.data) {
        errors.value = error.response.data.errors || ["APIからのデータ取得中にエラーが発生しました。"];
      } else {
        errors.value = ["APIからのデータ取得中にエラーが発生しました。"];
      }
    }
};

const fetchTransactionItems = async () => {
    try {
        const response = await axios.get('http://localhost:5000/api/v1/transactions/items');
        if (response.data && response.data.status === "success") {
            transactionItems.value = response.data.items;
        } else {
            errors.value = response.data.errors || ["予期しないエラーが発生しました。"];
        }
    } catch (error) {
        errors.value = ["APIからのデータ取得中にエラーが発生しました。"];
    }
};

onMounted(() => {
    fetchTransactionItems();  // コンポーネントがマウントされたときに入出金事項の一覧を取得
});

// 収入と支出の入出金事項を分ける
const incomeItemNames = computed(() => {
    return transactionItems.value.filter(item => item.item_type === 'income').map(item => item.item_name);
});
const expenseItemNames = computed(() => {
    return transactionItems.value.filter(item => item.item_type === 'expense').map(item => item.item_name);
});
// 収入トランザクションのみを抽出
const incomeTransactions = computed(() => {
  return monthlyTransactions.value.filter(t => t.item_type === 'income');
});

// 支出トランザクションのみを抽出
const expenseTransactions = computed(() => {
  return monthlyTransactions.value.filter(t => t.item_type === 'expense');
});

// 2. 指定した年月に基づいて入出金情報をフィルタリング
const filteredTransactions = computed(() => {
  return monthlyTransactions.value.filter(t => t.month === month.value);
});

async function onSubmit() {
  try {
    // monthを 'YYYYMM' の形式に変換
    const monthParam = `${selectedYear.value}${String(selectedMonth.value).padStart(2, '0')}`;
    const requestData = {
      month: monthParam,
      incomeName: incomeName.value,
      expenseName: expenseName.value,
      incomeAmount: incomeAmount.value,
      expenseAmount: expenseAmount.value,
    };

    const response = await axios.post('/api/monthlyTransactionUpdate', requestData);

    if (response.data && response.data.success) {
      successMessage.value = ["データが正常に保存されました。"];
      errors.value = [];
    } else {
      errors.value = response.data.errors || ["予期しないエラーが発生しました。"];
      successMessage.value = null;
    }
  } catch (error) {
    if (error.response && error.response.data) {
      errors.value = error.response.data.errors || ["APIへのデータ送信中にエラーが発生しました。"];
    } else {
      errors.value = ["APIへのデータ送信中にエラーが発生しました。"];
    }
    successMessage.value = null;
  }
}
</script>
