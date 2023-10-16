<!-- MonthlyTransactionUpsert.vue -->
<template>
  <form @submit.prevent="onSubmit">
    <va-input
      v-model="month"
      class="mb-4"
      :label="t('transaction.month')"
      :error="!!monthErrors.length"
      :error-messages="monthErrors"
    />

    <va-input
      v-model="amount"
      class="mb-4"
      type="number"
      :label="t('transaction.amount')"
      :error="!!amountErrors.length"
      :error-messages="amountErrors"
    />

    <va-input
      v-model="itemName"
      class="mb-4"
      :label="t('transaction.itemName')"
      :error="!!itemNameErrors.length"
      :error-messages="itemNameErrors"
    />

    <div class="flex justify-center mt-4">
      <va-button class="my-0" @click="onSubmit">{{ t('transaction.save') }}</va-button>
    </div>
  </form>
</template>

<script setup lang="ts">
  import { ref, computed, onMounted } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { useRouter, useRoute } from 'vue-router';

  const { t } = useI18n();
  const route = useRoute();
  const router = useRouter();

  const month = ref('');
  const amount = ref('');
  const itemName = ref('');
  const monthErrors = ref<string[]>([]);
  const amountErrors = ref<string[]>([]);
  const itemNameErrors = ref<string[]>([]);

  const formReady = computed(() => {
    return !(monthErrors.value.length || amountErrors.value.length || itemNameErrors.value.length);
  });

  function onSubmit() {
    if (!formReady.value) return;

    monthErrors.value = month.value ? [] : [t('errors.required', { field: '月' })];
    amountErrors.value = amount.value ? [] : [t('errors.required', { field: '金額' })];
    itemNameErrors.value = itemName.value ? [] : [t('errors.required', { field: '項目名' })];

    if (!formReady.value) return;

    if (route.params.transaction_id) {
      // PUTを使用して更新APIを呼び出す
      // 例: updateTransaction(route.params.transaction_id, { month: month.value, amount: amount.value, itemName: itemName.value });
    } else {
      // POSTを使用して新規作成APIを呼び出す
      // 例: createMonthlyTransaction({ month: month.value, amount: amount.value, itemName: itemName.value });
    }

    router.push({ name: 'transaction-list' }); // 'transaction-list'という名前のルートに遷移することを想定
  }
</script>
