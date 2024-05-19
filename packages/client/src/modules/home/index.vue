<template>

</template>
<script setup>
import { useRouter } from 'vue-router';
import HttpHelper from '../../common/utils/axios_helper';
import Urls from '../../common/urls/index';

const router = useRouter();
const toDetail = async () => {
  router.push('/detail');
};

// 测试发送请求
const sendMessage = async () => {
  const res = await HttpHelper.post(Urls.getDetail, { name: 'test' });
  console.log(res);
  alert(JSON.stringify(res));
};

</script>

<style lang="less"></style>