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
    <div class="flex justify-between -mx-2 transaction-sections">
      <!-- Income Section -->
      <div class="w-full px-2 mb-4 mt-4">
      <label>{{ t('transaction.income') }}</label>
        <div v-for="incomeTransaction in incomeTransactions" :key="incomeTransaction.id" class="mb-2 flex">
          <div class="w-1/2 pr-1">
            <select v-model="incomeTransaction.item_name" class="border rounded p-1 w-full">
              <option v-for="itemName in incomeItemNames" :key="itemName" :value="itemName">
                {{ itemName }}
              </option>
            </select>
          </div>
          <div class="w-1/2 pl-1">
            <va-input
              v-model="incomeTransaction.amount"
              type="number"
              :label="t('transaction.amount')"
              :error="!!amountErrors.length"
              :error-messages="amountErrors"
            />
          </div>
        </div>
        <button type="button" @click="addIncomeTransaction" class="p-2 bg-blue-500 text-white rounded">収入を追加</button>
      </div>
      <!-- Expense Section -->
      <div class="w-full px-2 mt-4">
      <label>{{ t('transaction.expense') }}</label>
        <div v-for="expenseTransaction in expenseTransactions" :key="expenseTransaction.id" class="mb-2 flex">
          <div class="w-1/2 pr-1">
            <select v-model="expenseTransaction.item_name" class="border rounded p-1 w-full">
              <option v-for="itemName in expenseItemNames" :key="itemName" :value="itemName">
                {{ itemName }}
              </option>
            </select>
          </div>
          <div class="w-1/2 pl-1">
            <va-input
              v-model="expenseTransaction.amount"
              type="number"
              :label="t('transaction.amount')"
              :error="!!amountErrors.length"
              :error-messages="amountErrors"
            />
          </div>
        </div>
        <button type="button" @click="addExpenseTransaction" class="p-2 bg-red-500 text-white rounded">支出を追加</button>
      </div>
    </div>
    <div class="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div class="bg-blue-100 p-4 rounded flex items-center justify-between">
        <div>
          <h3 class="text-blue-500 font-semibold">{{ t('transaction.totalIncome') }}</h3>
          <p class="text-lg font-bold text-blue-800">{{ totalIncome | currency }}</p>
        </div>
        <div class="text-blue-500">
          <!-- 任意のアイコンや画像を挿入 -->
          <span class="material-icons">arrow_upward</span>
        </div>
      </div>
      <div class="bg-red-100 p-4 rounded flex items-center justify-between">
        <div>
          <h3 class="text-red-500 font-semibold">{{ t('transaction.totalExpense') }}</h3>
          <p class="text-lg font-bold text-red-800">{{ totalExpense | currency }}</p>
        </div>
        <div class="text-red-500">
          <!-- 任意のアイコンや画像を挿入 -->
          <span class="material-icons">arrow_downward</span>
        </div>
      </div>
      <div :class="totalBalanceColor" class="p-4 rounded flex items-center justify-between">
        <div>
          <h3 :class="totalBalanceTextColor" class="font-semibold">{{ t('transaction.balance') }}</h3>
          <p class="text-lg font-bold" :class="totalBalanceTextColor">{{ totalBalance | currency }}</p>
        </div>
        <div :class="totalBalanceTextColor">
          <!-- 任意のアイコンや画像を挿入 -->
          <span class="material-icons" v-if="totalBalance >= 0">trending_up</span>
          <span class="material-icons" v-else>trending_down</span>
        </div>
      </div>
    </div>
    <div class="flex justify-center mt-4">
      <va-button class="px-6 py-3 bg-blue-500 text-white text-lg rounded-lg shadow-lg hover:bg-blue-600 transition-colors duration-300 ease-in-out" @click="onSubmit">
        {{ t('transaction.save') }}
      </va-button>
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
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useI18n } from 'vue-i18n';
import { VaDatePicker } from 'vuestic-ui';

const { t } = useI18n();
const route = useRoute();

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

const currentDate = new Date();
const currentYear = currentDate.getFullYear();
const selectedYear = ref(currentYear); // 現在の年をデフォルトとして設定

const selectedMonth = ref(new Date().getMonth() + 1); // 1から12の範囲で
const yearOptions = Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - i); // 今の年から10年前までのオプション
const monthOptions = Array.from({ length: 12 }, (_, i) => i + 1); // 1から12の月のオプション

const monthlyTransactions = ref([]);
// 入出金事項の一覧を保存するためのref
const transactionItems = ref([]);

const incomeTransactions = ref([]); // 収入トランザクションのリアクティブ配列
const expenseTransactions = ref([]); // 支出トランザクションのリアクティブ配列

const updateMonthValue = () => {
  month.value = `${selectedYear.value}${String(selectedMonth.value).padStart(2, '0')}`;
};

watch(incomeAmount, (newValue) => {
  totalIncome.value = parseFloat(newValue) || 0;
});

watch(expenseAmount, (newValue) => {
  totalExpense.value = parseFloat(newValue) || 0;
});


watch([selectedYear, selectedMonth], () => {
  updateFilteredTransactions();
}, { deep: true });

// 全ての入出金情報を取得する
const fetchAllTransactions = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/v1/transactions/monthly');
    if (response.data && response.data.success) {
      monthlyTransactions.value = response.data.transactions;
      updateFilteredTransactions();
    } else {
      errors.value = response.data.errors || ["予期しないエラーが発生しました。"];
    }
  } catch (error) {
    errors.value = ["APIからのデータ取得中にエラーが発生しました。"];
  }
};

// 選択された年月に基づいてフィルタリング
const updateFilteredTransactions = () => {
  const selectedMonthString = `${selectedYear.value}${String(selectedMonth.value).padStart(2, '0')}`;
  incomeTransactions.value = monthlyTransactions.value.filter(t => t.item_type === 'income' && t.month === selectedMonthString);
  expenseTransactions.value = monthlyTransactions.value.filter(t => t.item_type === 'expense' && t.month === selectedMonthString);
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
    fetchAllTransactions();

    // パラメータから年月を取得してセットする
    let monthParam = route.params.month;

    // 'YYYYMM' 形式であることを確認、そうでない場合は現在の年月を使用
    if (!monthParam || monthParam.length !== 6) {
      const now = new Date();
      const year = now.getFullYear().toString();
      const month = (now.getMonth() + 1).toString().padStart(2, '0');
      monthParam = year + month;
      // エラーがあればここで処理するか、ユーザーに通知する
    }

  selectedYear.value = monthParam.substring(0, 4);
  selectedMonth.value = parseInt(monthParam.substring(4, 6), 10);

    // 初期データフェッチまたはフィルタリングロジックを実行
    fetchTransactionItems();
});

// 収入と支出の入出金事項を分ける
const incomeItemNames = computed(() => {
    return transactionItems.value.filter(item => item.item_type === 'income').map(item => item.item_name);
});
const expenseItemNames = computed(() => {
    return transactionItems.value.filter(item => item.item_type === 'expense').map(item => item.item_name);
});

const addIncomeTransaction = () => {
  incomeTransactions.value.push({
    selectedIncomeName: '', // 選択された収入名
    incomeAmount: 0, // 収入額
    isNew: true,
  });
};
const addExpenseTransaction = () => {
  expenseTransactions.value.push({
    selectedExpenseName: '', // 選択された支出名
    expenseAmount: 0, // 支出額
    isNew: true,
  });
};

// 2. 指定した年月に基づいて入出金情報をフィルタリング
const filteredTransactions = computed(() => {
  return monthlyTransactions.value.filter(t => t.month === month.value);
});

// 収入の合計を計算する計算プロパティ
const totalIncome = computed(() => {
  return incomeTransactions.value.reduce((acc, transaction) => acc + Number(transaction.amount || 0), 0);
});

// 支出の合計を計算する計算プロパティ
const totalExpense = computed(() => {
  return expenseTransactions.value.reduce((acc, transaction) => acc + Number(transaction.amount || 0), 0);
});

// 収支バランスを計算する計算プロパティ
const totalBalance = computed(() => {
  return totalIncome.value - totalExpense.value;
});

async function onSubmit() {
  // 選択された年月を 'YYYYMM' 形式で取得
  const selectedMonthString = `${selectedYear.value}${String(selectedMonth.value).padStart(2, '0')}`;

  // 収入と支出の取引を結合する
  const transactions = [
    ...incomeTransactions.value.filter(t => t.isNew).map(t => ({
      Month: selectedMonthString,
      ItemName: t.item_name,
      Amount: t.amount,
    })),
    ...expenseTransactions.value.filter(t => t.isNew).map(t => ({
      Month: selectedMonthString,
      ItemName: t.item_name,
      Amount: t.amount,
    })),
  ];
  // APIに送信するデータ
  const requestData = {
    transactions,
  };
  console.log(requestData)

  try {
    const response = await axios.post('http://localhost:5000/api/v1/transactions/monthly', requestData);

    if (response.data && response.data.status === "success") {
      // 成功メッセージを表示
      successMessage.value = response.data.message || "データが正常に保存されました。";
      errors.value = [];
    } else {
      errors.value = response.data.message || ["予期しないエラーが発生しました。"];
      successMessage.value = null;
    }
  } catch (error) {
    // エラーハンドリング
    errors.value = ["APIへのデータ送信中にエラーが発生しました。"];
    successMessage.value = null;
  }
}
const totalBalanceColor = computed(() => ({
  'bg-green-100': totalBalance.value >= 0,
  'bg-red-100': totalBalance.value < 0,
}));

const totalBalanceTextColor = computed(() => ({
  'text-green-800': totalBalance.value >= 0,
  'text-red-800': totalBalance.value < 0,
}));
</script>
<style>
@media (max-width: 768px) {
  .transaction-sections {
    flex-direction: column;
  }
}
</style>