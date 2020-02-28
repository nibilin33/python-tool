<template>
<div>
<p>&nbsp;</p>
<el-form label-width="80px" >
  <el-form-item label="企业名称">
    <el-input v-model="registerName"></el-input>
  </el-form-item>
  <el-form-item label="">
      <el-button @click="register">注册</el-button>
  </el-form-item>
</el-form>
<el-form label-width="80px" >
  <el-form-item label="企业ID">
    <el-input v-model="enterpriseName"></el-input>
  </el-form-item>
  <el-form-item label="">
      <el-button @click="submit">提交</el-button>
      <el-button @click="view">查看</el-button>
  </el-form-item>
</el-form>
</template>