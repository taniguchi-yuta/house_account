<template>
  <form @submit.prevent="onsubmit">
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
      <va-checkbox v-model="keepLoggedIn" class="mb-0" :label="t('auth.keep_logged_in')" />
      <router-link class="ml-1 va-link" :to="{ name: 'recover-password' }">{{
        t('auth.recover_password')
      }}</router-link>
    </div>

    <div class="flex justify-center mt-4">
      <va-button class="my-0" @click="onsubmit">{{ t('auth.login') }}</va-button>
    </div>
  </form>
</template>

<script setup lang="ts">
  import { computed, ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useI18n } from 'vue-i18n';
  import axios from 'axios';  // axios をインポート

  const { t } = useI18n();
  const email = ref('');
  const password = ref('');
  const keepLoggedIn = ref(false);
  const emailErrors = ref<string[]>([]);
  const passwordErrors = ref<string[]>([]);
  const router = useRouter();

  const formReady = computed(() => !emailErrors.value.length && !passwordErrors.value.length);

  async function onsubmit() {
    if (!formReady.value) return;

    emailErrors.value = email.value ? [] : ['Email is required'];
    passwordErrors.value = password.value ? [] : ['Password is required'];

    if (emailErrors.value.length || passwordErrors.value.length) return;

    try {
      const response = await axios.post('http://localhost:5000/api/v1/users/login', {
        emailAddress: email.value,
        password: password.value,
      });

      if (response.data.status === 'success') {
        router.push({ name: 'dashboard' });
      } else {
        // ここでエラーメッセージをユーザーに表示する方法を選択してください。
        console.error('Login error:', response.data.message);
      }
    } catch (error) {
      console.error('Error during login:', error);
      // ここでエラーメッセージをユーザーに表示する方法を選択してください。
    }
  }
</script>
