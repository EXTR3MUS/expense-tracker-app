<template>
  <div id="app">
    <nav class="navbar">
      <div class="container">
        <h1>🚫 Unauthorized Access</h1>
      </div>
    </nav>
    <div class="container">
      <div class="card unauthorized-card">
        <div class="icon">🔒</div>
        <h2>Access Denied</h2>
        <p>You do not have permission to access the audit logs.</p>
        <p class="hint">Incorrect password provided.</p>
        <a href="/" class="btn btn-primary">Go to Home</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Unauthorized'
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f5f5f5;
}

#app {
  min-height: 100vh;
}

.navbar {
  background: #e74c3c;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar .container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.navbar h1 {
  font-size: 1.5rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 3rem 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.unauthorized-card {
  text-align: center;
  max-width: 500px;
  margin: 2rem auto;
}

.icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.unauthorized-card h2 {
  color: #e74c3c;
  margin-bottom: 1rem;
  font-size: 1.8rem;
}

.unauthorized-card p {
  color: #7f8c8d;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.hint {
  font-size: 0.9rem;
  font-style: italic;
  margin-bottom: 2rem !important;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  text-decoration: none;
  transition: background 0.3s;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}
</style>
