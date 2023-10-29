<template>
  <form @submit.prevent="onsubmit">
    <!-- ItemType Input -->
    <va-select
      v-model="itemType"
      :label="t('transaction.itemType')"
      :error="!!itemTypeErrors.length"
      :error-messages="itemTypeErrors"
      :options="itemTypes"
      placeholder="Select Item Type"
    ></va-select>

    <!-- ItemName Input -->
    <va-input
      v-model="itemName"
      class="mb-4"
      type="text"
      :label="t('transaction.itemName')"
      :error="!!itemNameErrors.length"
      :error-messages="itemNameErrors"
    />

    <!-- Success Message -->
    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- Submit Button -->
    <div class="flex justify-center mt-4">
      <va-button class="my-0" @click="onsubmit">
        {{ isUpdateMode ? t('transaction.update') : t('transaction.register') }}
      </va-button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import axios from 'axios'

const { t } = useI18n()
const router = useRouter()
const route = useRoute();

const itemType = ref('')
const itemName = ref('')
const itemTypeErrors = ref<string[]>([])
const itemNameErrors = ref<string[]>([])
const isUpdateMode = ref(!!route.params.id)  // Check if itemID exists to set update mode
const successMessage = ref('')
const errorMessage = ref('')
const itemID = ref(route.params.id)
const itemTypes = ref([
  { text: t('transaction.income'), value: 'income' },
  { text: t('transaction.expense'), value: 'expense' }
]);

// Fetch initial data for the form
async function fetchData() {
  if (!isUpdateMode.value) return

  try {
    const response = await axios.get(`http://localhost:5000/api/v1/transactions/item/${itemID.value}`)
    if (response.data && response.data.status === 'success') {
      itemType.value = response.data.item.item_type
      itemName.value = response.data.item.item_name
    }
  } catch (error) {
    console.error('Failed to fetch the item data', error)
  }
}

onMounted(fetchData) // Call fetchData when the component is mounted

const formReady = computed(() => {
  return !(itemTypeErrors.value.length || itemNameErrors.value.length)
})

function validateForm(): boolean {
  itemTypeErrors.value = itemType.value ? [] : [t('transaction.itemTypeRequired')]
  itemNameErrors.value = itemName.value ? [] : [t('transaction.itemNameRequired')]
  return !(itemTypeErrors.value.length || itemNameErrors.value.length)
}

async function onsubmit() {
  if (!validateForm()) return

  try {
    let response
    const payload = {
      ItemType: itemType.value.value,
      ItemName: itemName.value
    }
    console.log(itemType.value)
    if (isUpdateMode.value) {
      response = await axios.put(`http://localhost:5000/api/v1/transactions/item/${itemID.value}`, payload)
    } else {
      response = await axios.post('http://localhost:5000/api/v1/transactions/item', payload)
    }

    if (response.data.status === 'success') {
      successMessage.value = t('transaction.successfulOperation')
      setTimeout(() => successMessage.value = '', 3000) // Clear the message after 3 seconds
    } else {
      errorMessage.value = response.data.message || t('transaction.failedOperation')
      setTimeout(() => errorMessage.value = '', 3000) // Clear the message after 3 seconds
    }
  } catch (error) {
    errorMessage.value = t('transaction.failedOperation')
    console.error(error)
    setTimeout(() => errorMessage.value = '', 3000) // Clear the message after 3 seconds
  }
}
</script>

<style scoped>
.success-message {
  padding: 1em;
  background-color: #eaffea;
  border: 1px solid #b8e6b8;
  color: #34a853;
  margin-bottom: 1em;
}

.error-message {
  padding: 1em;
  background-color: #ffebee;
  border: 1px solid #ff8a80;
  color: #d32f2f;
  margin-bottom: 1em;
}
</style>
