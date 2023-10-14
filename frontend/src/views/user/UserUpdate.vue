<template>
  <div class="user-update">
    <va-card title="ユーザー情報の更新">
      <va-form @submit="updateUserInfo">
        <va-input v-model="userData.emailAddress" label="メールアドレス" placeholder="メールアドレスを入力してください" class="mb-4" />
        <va-input type="password" v-model="userData.password" label="パスワード" placeholder="パスワードを入力してください" class="mb-4" />
        <va-input v-model="userData.name" label="名前" placeholder="名前を入力してください" class="mb-4" />
        <div class="flex justify-center mt-4">
          <va-button type="submit" color="primary">更新</va-button>
        </div>
      </va-form>
    </va-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

const userData = ref({
  emailAddress: '',
  password: '',
  name: ''
});

async function updateUserInfo() {
  try {
    const response = await axios.put('/api/v1/users/update', userData.value);
    if (response.data.success) {
      // 更新が成功したときの処理
      this.$router.push('/path-after-success');  // 適切な遷移先に変更してください。
    } else {
      // エラーメッセージを表示するなどの処理
    }
  } catch (error) {
    console.error('ユーザー情報の更新に失敗しました：', error);
  }
}
</script>

<style lang="scss">
.user-update {
  .va-card {
    margin-bottom: 0 !important;
    &__title {
      display: flex;
      justify-content: space-between;
    }
  }
}
</style>
