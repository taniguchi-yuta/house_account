import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

import AuthLayout from '../layouts/AuthLayout.vue'
import AppLayout from '../layouts/AppLayout.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/:catchAll(.*)',
    redirect: { name: 'monthly-transaction-list' },
  },
  // {
  //   name: 'admin',
  //   path: '/admin',
  //   component: AppLayout,
  //   children: [
  //     {
  //       name: 'dashboard',
  //       path: 'dashboard',
  //       component: () => import('@/views/dashboard/Dashboard.vue'),
  //     },
  //   ],
  // },
  {
    path: '/auth',
    component: AuthLayout,
    children: [
      {
        name: 'login',
        path: 'login',
        component: () => import('@/views/auth/login/Login.vue'),
      },
      {
        name: 'signup',
        path: 'signup',
        component: () => import('@/views/auth/signup/Signup.vue'),
      },
      {
        name: 'recover-password',
        path: 'recover-password',
        component: () => import('@/views/auth/recover-password/RecoverPassword.vue'),
      },
      {
        path: '',
        redirect: { name: 'login' },
      },
    ],
  },
  {
    name: 'user',
    path: '/user',
    component: AppLayout,
    children: [
      {
        name: 'user-update',
        path: 'update',
        component: () => import('@/views/user/user-update/UserUpdate.vue'),
      },
    ],
  },
  {
    name: 'transaction',
    path: '/transaction',
    component: AppLayout,
    children: [
      {
        name: 'transaction-item-list',
        path: 'item/list',
        component: () => import('@/views/transaction/transaction-items/TransactionItemList.vue'),
      },
      {
        name: 'transaction-item-upsert',
        path: 'item/upsert/:id?',
        component: () => import('@/views/transaction/transaction-items/TransactionItemUpsert.vue'),
      },
      {
        name: 'monthly-transaction-list',
        path: 'monthly/list',
        component: () => import('@/views/transaction/monthly-transactions/MonthlyTransactionList.vue'),
      },
      {
        name: 'monthly-transaction-upsert',
        path: 'monthly/upsert/:id?',
        component: () => import('@/views/transaction/monthly-transactions/MonthlyTransactionUpsert.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    // For some reason using documentation example doesn't scroll on page navigation.
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    } else {
      document.querySelector('.app-layout__page')?.scrollTo(0, 0)
    }
  },
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('Authorization');
  if (token) {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const expiry = payload.exp;
    const now = Date.now() / 1000;

    if (expiry < now) {
      // トークンの有効期限が切れている場合
      localStorage.removeItem('Authorization');
      if (to.name !== 'login') {
        next({ name: 'login' }); // ログインページにリダイレクト
      } else {
        next(); // 既にログインページにいる場合はそのまま
      }
    } else {
      // トークンが有効な場合
      next(); // ナビゲーションを続行
    }
  } else {
    // トークンが存在しない場合
    if (to.name !== 'login') {
      next({ name: 'login' }); // ログインページにリダイレクト
    } else {
      next(); // 既にログインページにいる場合はそのまま
    }
  }
});

export default router
