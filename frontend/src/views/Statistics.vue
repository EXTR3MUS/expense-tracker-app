<template>
  <div class="statistics">
    <div class="card">
      <h2>Estatísticas Gerais</h2>
      <div v-if="loading" class="loading">Carregando...</div>
      <div v-else class="stats-grid">
        <div class="stat-item">
          <span class="stat-label">Total Gasto:</span>
          <span class="stat-value">{{ formatCurrency(summary.total_expenses) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Número de Despesas:</span>
          <span class="stat-value">{{ summary.expense_count }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Média por Despesa:</span>
          <span class="stat-value">{{ formatCurrency(summary.average_expense) }}</span>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>Despesas por Categoria</h2>
      <div v-if="loading" class="loading">Carregando...</div>
      <table v-else-if="byCategory.length">
        <thead>
          <tr>
            <th>Categoria</th>
            <th>Quantidade</th>
            <th>Total</th>
            <th>Média</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in byCategory" :key="item.category">
            <td>{{ item.category }}</td>
            <td>{{ item.expense_count }}</td>
            <td>{{ formatCurrency(item.total_amount) }}</td>
            <td>{{ formatCurrency(item.average_amount) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>Nenhuma despesa cadastrada para análise.</p>
    </div>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'Statistics',
  data() {
    return {
      summary: {
        total_expenses: 0,
        expense_count: 0,
        average_expense: 0
      },
      byCategory: [],
      loading: false
    }
  },
  mounted() {
    this.loadStatistics()
  },
  methods: {
    async loadStatistics() {
      this.loading = true
      try {
        const [summaryRes, categoryRes] = await Promise.all([
          api.getSummaryStatistics(),
          api.getCategoryStatistics()
        ])
        this.summary = summaryRes.data
        this.byCategory = categoryRes.data
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error)
      } finally {
        this.loading = false
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
.stats-grid {
  display: grid;
  gap: 1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.stat-label {
  font-weight: 500;
  color: #7f8c8d;
}

.stat-value {
  font-weight: bold;
  color: #2c3e50;
  font-size: 1.2rem;
}
</style>
