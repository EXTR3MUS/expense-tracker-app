<template>
  <router-view />
</template>

<script>
export default {
  name: 'RouterApp',
  mounted() {
    console.log('RouterApp mounted, current route:', this.$route.path)
  }
}
</script>
