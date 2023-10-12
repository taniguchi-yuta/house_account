<template>
  <div class="user-update-container">
    <va-card title="ユーザー情報の更新">
      <va-form @submit="updateUserInfo">
        <va-input v-model="userData.emailAddress" label="メールアドレス" placeholder="メールアドレスを入力してください" />
        <va-input type="password" v-model="userData.password" label="パスワード" placeholder="パスワードを入力してください" />
        <va-input v-model="userData.name" label="名前" placeholder="名前を入力してください" />
        <va-button type="submit" color="primary">更新</va-button>
      </va-form>
    </va-card>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import axios from 'axios';

export default {
  name: 'UserUpdate',
  data() {
    return {
      userData: {
        emailAddress: '',
        password: '',
        name: ''
      }
    };
  },
  methods: {
    async updateUserInfo() {
      try {
        const response = await axios.put('/api/v1/users/update', this.userData);
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
  }
};
</script>

<style scoped>
.user-update-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
}
</style>
