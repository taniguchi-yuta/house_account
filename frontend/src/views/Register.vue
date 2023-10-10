<template>
  <div class="registration-container">
    <va-card flat>
      <va-form>
        <va-input label="メールアドレス" v-model="email" flat/>
        <va-input type="password" label="パスワード" v-model="password" flat/>
        <va-input label="ユーザー名" v-model="username" flat/>
        <va-button @click="register" flat>登録</va-button>
      </va-form>
    </va-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      username: ''
    };
  },
  methods: {
    register() {
      // 登録ロジックをここに追加
    }
  }
};
</script>

<style scoped>
.registration-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
