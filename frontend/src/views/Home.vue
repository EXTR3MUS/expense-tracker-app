<template>
  <div class="home">
    <div class="card">
      <h2>Bem-vindo ao Expense Tracker</h2>
      <p>Sistema de controle de despesas com categorização e estatísticas.</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <h3>Total de Despesas</h3>
        <p class="stat-value">{{ formatCurrency(summary.total_expenses) }}</p>
      </div>
      <div class="stat-card">
        <h3>Número de Despesas</h3>
        <p class="stat-value">{{ summary.expense_count }}</p>
      </div>
      <div class="stat-card">
        <h3>Média por Despesa</h3>
        <p class="stat-value">{{ formatCurrency(summary.average_expense) }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'Home',
  data() {
    return {
      summary: {
        total_expenses: 0,
        expense_count: 0,
        average_expense: 0
      }
    }
  },
  mounted() {
    this.loadSummary()
  },
  methods: {
    async loadSummary() {
      try {
        const response = await api.getSummaryStatistics()
        this.summary = response.data
      } catch (error) {
        console.error('Erro ao carregar resumo:', error)
      }
    },
    formatCurrency(value) {
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      }).format(value)
    }
  }
}
</script>

<style scoped>
.home h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-card h3 {
  color: #7f8c8d;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.stat-value {
  color: #2c3e50;
  font-size: 2rem;
  font-weight: bold;
}
</style>
