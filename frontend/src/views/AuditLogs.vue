<template>
  <div id="app">
    <nav class="navbar">
      <div class="container">
        <h1>🔍 Audit Logs</h1>
        <a href="/" class="btn btn-primary">← Back to Home</a>
      </div>
    </nav>
    <div class="container">
      <div class="card">
        <h2>Transaction Audit Trail</h2>
        <p class="info-text">Complete history of all transaction operations (INSERT, UPDATE, DELETE)</p>
        
        <div v-if="loading" class="loading">Loading audit logs...</div>
        
        <div v-else-if="logs.length" class="logs-container">
          <div v-for="log in logs" :key="log.log_id" class="log-item" :class="`operation-${log.operation.toLowerCase()}`">
            <div class="log-header">
              <span class="operation-badge" :class="log.operation.toLowerCase()">{{ log.operation }}</span>
              <span class="log-id">#{{ log.transaction_id }}</span>
              <span class="log-timestamp">{{ formatDate(log.log_timestamp) }}</span>
            </div>
            
            <div class="log-details">
              <!-- INSERT Operation -->
              <div v-if="log.operation === 'INSERT'" class="change-grid">
                <div class="change-item">
                  <strong>Amount:</strong> {{ formatCurrency(log.new_amount) }}
                </div>
                <div class="change-item">
                  <strong>Description:</strong> {{ log.new_description || '-' }}
                </div>
                <div class="change-item">
                  <strong>Category ID:</strong> {{ log.new_category_id }}
                </div>
                <div class="change-item">
                  <strong>Date:</strong> {{ formatDate(log.new_date) }}
                </div>
              </div>
              
              <!-- UPDATE Operation -->
              <div v-else-if="log.operation === 'UPDATE'" class="change-grid">
                <div v-if="log.old_amount !== log.new_amount" class="change-item">
                  <strong>Amount:</strong>
                  <span class="old-value">{{ formatCurrency(log.old_amount) }}</span>
                  <span class="arrow">→</span>
                  <span class="new-value">{{ formatCurrency(log.new_amount) }}</span>
                </div>
                <div v-if="log.old_description !== log.new_description" class="change-item">
                  <strong>Description:</strong>
                  <span class="old-value">{{ log.old_description || '-' }}</span>
                  <span class="arrow">→</span>
                  <span class="new-value">{{ log.new_description || '-' }}</span>
                </div>
                <div v-if="log.old_category_id !== log.new_category_id" class="change-item">
                  <strong>Category ID:</strong>
                  <span class="old-value">{{ log.old_category_id }}</span>
                  <span class="arrow">→</span>
                  <span class="new-value">{{ log.new_category_id }}</span>
                </div>
                <div v-if="log.old_date !== log.new_date" class="change-item">
                  <strong>Date:</strong>
                  <span class="old-value">{{ formatDate(log.old_date) }}</span>
                  <span class="arrow">→</span>
                  <span class="new-value">{{ formatDate(log.new_date) }}</span>
                </div>
              </div>
              
              <!-- DELETE Operation -->
              <div v-else-if="log.operation === 'DELETE'" class="change-grid">
                <div class="change-item">
                  <strong>Amount:</strong> {{ formatCurrency(log.old_amount) }}
                </div>
                <div class="change-item">
                  <strong>Description:</strong> {{ log.old_description || '-' }}
                </div>
                <div class="change-item">
                  <strong>Category ID:</strong> {{ log.old_category_id }}
                </div>
                <div class="change-item">
                  <strong>Date:</strong> {{ formatDate(log.old_date) }}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <p v-else class="empty">No audit logs found.</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api'
import { useRouter } from 'vue-router'

export default {
  name: 'AuditLogs',
  data() {
    return {
      logs: [],
      loading: false
    }
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  mounted() {
    this.checkPasswordAndLoad()
  },
  methods: {
    checkPasswordAndLoad() {
      const password = prompt('Enter password to view audit logs:')
      
      if (password === '123') {
        this.loadAuditLogs()
      } else {
        this.router.push('/unauthorized')
      }
    },
    async loadAuditLogs() {
      this.loading = true
      try {
        const response = await api.getAuditLogs()
        this.logs = response.data
      } catch (error) {
        console.error('Error loading audit logs:', error)
        alert('Error loading audit logs')
      } finally {
        this.loading = false
      }
    },
    formatCurrency(value) {
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      }).format(value)
    },
    formatDate(dateString) {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('pt-BR')
    }
  }
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
  background: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar .container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar h1 {
  font-size: 1.5rem;
}

.navbar .btn {
  background: #3498db;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card h2 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.info-text {
  color: #7f8c8d;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #95a5a6;
  font-style: italic;
}

.logs-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.log-item {
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 1rem;
  background: #f8f9fa;
}

.log-item.operation-insert {
  border-left: 4px solid #2ecc71;
}

.log-item.operation-update {
  border-left: 4px solid #f39c12;
}

.log-item.operation-delete {
  border-left: 4px solid #e74c3c;
}

.log-header {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #ddd;
}

.operation-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-weight: bold;
  font-size: 0.85rem;
  color: white;
}

.operation-badge.insert {
  background: #2ecc71;
}

.operation-badge.update {
  background: #f39c12;
}

.operation-badge.delete {
  background: #e74c3c;
}

.log-id {
  font-weight: bold;
  color: #2c3e50;
}

.log-timestamp {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-left: auto;
}

.log-details {
  margin-top: 0.5rem;
}

.change-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.75rem;
}

.change-item {
  padding: 0.5rem;
  background: white;
  border-radius: 4px;
}

.change-item strong {
  display: block;
  color: #7f8c8d;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}

.old-value {
  color: #e74c3c;
  text-decoration: line-through;
}

.new-value {
  color: #2ecc71;
  font-weight: 500;
}

.arrow {
  color: #7f8c8d;
  margin: 0 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
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
