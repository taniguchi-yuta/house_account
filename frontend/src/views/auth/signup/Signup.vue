<template>
  <form @submit.prevent="onsubmit()">
    <va-input
      v-model="email"
      class="mb-4"
      type="email"
      :label="t('auth.email')"
      :error="!!emailErrors.length"
      :error-messages="emailErrors"
    />

    <va-input
      v-model="password"
      class="mb-4"
      type="password"
      :label="t('auth.password')"
      :error="!!passwordErrors.length"
      :error-messages="passwordErrors"
    />

    <div class="auth-layout__options flex items-center justify-between">
      <va-checkbox
        v-model="agreedToTerms"
        class="mb-0"
        :error="!!agreedToTermsErrors.length"
        :error-messages="agreedToTermsErrors"
      >
        <template #label>
          <span class="ml-2">
            {{ t('auth.agree') }}
            <span class="va-link">{{ t('auth.termsOfUse') }}</span>
          </span>
        </template>
      </va-checkbox>
      <router-link class="ml-1 va-link" :to="{ name: 'recover-password' }">
        {{ t('auth.recover_password') }}
      </router-link>
    </div>

    <div class="flex justify-center mt-4">
      <va-button class="my-0" @click="onsubmit" :disabled="loading">{{ t('auth.sign_up') }}</va-button>
    </div>
  </form>
</template>

<script setup lang="ts">
  import { ref, computed, watch } from 'vue';
  import { useRouter } from 'vue-router';
  import { useI18n } from 'vue-i18n';
  import axios from 'axios';  // axios をインポート

  const { t } = useI18n();

  const email = ref('');
  const password = ref('');
  const agreedToTerms = ref(false);
  const emailErrors = ref<string[]>([]);
  const passwordErrors = ref<string[]>([]);
  const agreedToTermsErrors = ref<string[]>([]);
  const loading = ref(false); // ローディング状態の管理のための ref
  const router = useRouter();

  const formReady = computed(() => {
    return !(emailErrors.value.length || passwordErrors.value.length || agreedToTermsErrors.value.length);
  });

  async function onsubmit() {
    console.log("onsubmit was called");
    if (!formReady.value) return;

    emailErrors.value = email.value ? [] : ['Email is required'];
    passwordErrors.value = password.value ? [] : ['Password is required'];
    agreedToTermsErrors.value = agreedToTerms.value ? [] : ['You must agree to the terms of use to continue'];

    if (emailErrors.value.length || passwordErrors.value.length || agreedToTermsErrors.value.length) return;

    loading.value = true; // ローディング状態を開始

    try {
      const response = await axios.post('http://localhost:5000/api/v1/users/register', {
        emailAddress: email.value,
        password: password.value,
        // nameは今回のUIから取得できないので、指定していません。
      }, {
        withCredentials: true
      });

      if (response.data.status === 'success') {
        router.push({ name: 'dashboard' });
      } else {
        throw new Error(response.data.message);
      }
    } catch (error) {
      console.error('Error registering user:', error);
      // ここでエラーメッセージをユーザーに表示する方法を選択してください。
    } finally {
      loading.value = false; // ローディング状態を終了
    }
  }
</script>
