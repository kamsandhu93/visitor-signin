<template>
    <div class="home">
        <el-button @click="changeRoute('/signin')">Sign In</el-button>
        <el-button @click="changeRoute('/signout')">Sign Out</el-button>
    </div>
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
