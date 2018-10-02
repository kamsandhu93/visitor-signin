<template>
    <el-main>
        <el-button @click="changeRoute('/signin')">Sign In</el-button>
        <el-button @click="changeRoute('/signout')">Sign Out</el-button>
    </el-main>
</template>

<script>

export default {
    methods: {
        changeRoute (route) {
            this.$router.push({path: route})
        }
    }
}
</script>
