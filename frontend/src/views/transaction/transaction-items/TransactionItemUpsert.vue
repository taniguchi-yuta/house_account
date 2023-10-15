<template>
  <form @submit.prevent="onsubmit">
    <!-- ItemType Input -->
    <va-input
      v-model="itemType"
      class="mb-4"
      type="text"
      :label="t('transaction.itemType')"
      :error="!!itemTypeErrors.length"
      :error-messages="itemTypeErrors"
    />

    <!-- ItemName Input -->
    <va-input
      v-model="itemName"
      class="mb-4"
      type="text"
      :label="t('transaction.itemName')"
      :error="!!itemNameErrors.length"
      :error-messages="itemNameErrors"
    />

    <!-- Submit Button -->
    <div class="flex justify-center mt-4">
      <va-button class="my-0" @click="onsubmit">
        {{ isUpdateMode ? t('transaction.update') : t('transaction.register') }}
      </va-button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const router = useRouter()

const itemType = ref('')
const itemName = ref('')
const itemTypeErrors = ref<string[]>([])
const itemNameErrors = ref<string[]>([])
const isUpdateMode = ref(false)  // これは登録モードか更新モードかを判断します。適切に設定してください。

const formReady = computed(() => {
  return !(itemTypeErrors.value.length || itemNameErrors.value.length)
})

function onsubmit() {
  if (!formReady.value) return

  itemTypeErrors.value = itemType.value ? [] : [t('transaction.itemTypeRequired')]
  itemNameErrors.value = itemName.value ? [] : [t('transaction.itemNameRequired')]

  if (formReady.value) {
    if (isUpdateMode.value) {
      // 更新APIを呼び出すロジックをここに書く
    } else {
      // 登録APIを呼び出すロジックをここに書く
    }
    router.push({ name: 'dashboard' }) // 適切なルートにリダイレクトします。
  }
}
</script>
