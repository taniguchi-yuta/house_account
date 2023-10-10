<template>
  <div class="login-container">
    <va-card flat>
      <va-form>
        <va-input label="メールアドレス" v-model="email" flat/>
        <va-input type="password" label="パスワード" v-model="password" flat/>
        <va-button @click="login" flat>ログイン</va-button>
      </va-form>
    </va-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    login() {
      // ログインロジックをここに追加
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
