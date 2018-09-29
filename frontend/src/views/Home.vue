<template>
    <div class="home">
        <button @click="changeRoute('/signin')">Sign In</button>
        <button @click="changeRoute('/signout')">Sign Out</button>
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
