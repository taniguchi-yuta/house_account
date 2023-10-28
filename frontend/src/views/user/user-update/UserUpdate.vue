<template>
  <div class="user-update">
    <va-card title="ユーザー情報の更新">
      <va-form>
        <va-input v-model="userData.emailAddress" label="メールアドレス" placeholder="メールアドレスを入力してください" class="mb-4" />
        <va-input type="password" v-model="userData.password" label="パスワード" placeholder="パスワードを入力してください" class="mb-4" />
        <va-input v-model="userData.name" label="名前" placeholder="名前を入力してください" class="mb-4" />
        
        <!-- 成功メッセージを表示する部分 -->
        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>

        <!-- エラーメッセージを表示する部分 -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div class="flex justify-center mt-4">
          <va-button @click.prevent="updateUserInfo" color="primary">更新</va-button>
        </div>
      </va-form>
    </va-card>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted, defineExpose } from 'vue';
import axios from 'axios';

const userData = ref({
  emailAddress: '',
  password: '',
  name: ''
});
const successMessage = ref('');
const errorMessage = ref('');

// ページロード時にユーザー情報を取得
onMounted(async () => {
  try {
    const token = localStorage.getItem('Authorization');
    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
    }

    const response = await axios.get('http://localhost:5000/api/v1/users/current');

    if (response.data.status === "success") {
      userData.value = {
        emailAddress: response.data.user.emailAddress,
        password: '',
        name: response.data.user.name
      };
    } else {
      errorMessage.value = response.data.message || 'ユーザー情報の取得に失敗しました。';
    }
  } catch (error) {
    errorMessage.value = 'ユーザー情報の取得に失敗しました。';
  }
});

async function updateUserInfo() {
  try {
    const token = localStorage.getItem('Authorization');
    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
    }

    const response = await axios.put('http://localhost:5000/api/v1/users/update', userData.value);

    if (response.data.status === "success") {
      successMessage.value = "ユーザー情報が正常に更新されました！";
      errorMessage.value = '';
    } else {
      errorMessage.value = response.data.message || '更新に失敗しました。';
      successMessage.value = '';
    }
  } catch (error) {
    errorMessage.value = 'ユーザー情報の更新に失敗しました。';
    successMessage.value = '';
  }
}

defineExpose({
  updateUserInfo
});
</script>


<style scoped>
.success-message {
  margin-top: 20px;
  padding: 10px 15px;
  border: 1px solid #4caf50;
  background-color: #e8f5e9;
  color: #2e7d32;
  border-radius: 4px;
  text-align: center;
}

.error-message {
  margin-top: 20px;
  padding: 10px 15px;
  border: 1px solid #f44336;
  background-color: #ffebee;
  color: #d32f2f;
  border-radius: 4px;
  text-align: center;
}
</style>

