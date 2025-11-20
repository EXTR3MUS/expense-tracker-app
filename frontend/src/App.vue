<template>
  <div id="app">
    <nav class="navbar">
      <div class="container">
        <h1>💰 Expense Tracker</h1>
        <a href="/audit" class="btn btn-sm btn-audit">🔍 Audit Logs</a>
      </div>
    </nav>
    <div class="container">
      <div class="main-content">
        <!-- Seção de Categorias -->
        <div class="card">
          <h2>Categorias</h2>
          <form @submit.prevent="saveCategory" class="form">
            <div class="form-row">
              <input v-model="categoryForm.name" type="text" placeholder="Nome da categoria" required>
              <button type="submit" class="btn btn-success">
                {{ editingCategoryId ? 'Atualizar' : 'Adicionar' }}
              </button>
              <button v-if="editingCategoryId" @click="cancelEditCategory" type="button" class="btn btn-danger">
                Cancelar
              </button>
            </div>
          </form>
          
          <div class="list">
            <div v-for="category in categories" :key="category.category_id" class="list-item">
              <span>{{ category.name }}</span>
              <div>
                <button @click="editCategory(category)" class="btn btn-sm btn-primary">Editar</button>
                <button @click="deleteCategory(category.category_id)" class="btn btn-sm btn-danger">Excluir</button>
              </div>
            </div>
            <p v-if="!categories.length" class="empty">Nenhuma categoria cadastrada</p>
          </div>
        </div>

        <!-- Seção de Transações -->
        <div class="card">
          <h2>Transações</h2>
          <form @submit.prevent="saveTransaction" class="form">
            <div class="form-group">
              <input v-model="transactionForm.description" type="text" placeholder="Descrição" required>
            </div>
            <div class="form-row">
              <input v-model.number="transactionForm.amount" type="number" step="0.01" placeholder="Valor" required>
              <select v-model="transactionForm.category_id" required>
                <option value="">Selecione categoria</option>
                <option v-for="cat in categories" :key="cat.category_id" :value="cat.category_id">
                  {{ cat.name }}
                </option>
              </select>
              <button type="submit" class="btn btn-success">
                {{ editingTransactionId ? 'Atualizar' : 'Adicionar' }}
              </button>
              <button v-if="editingTransactionId" @click="cancelEditTransaction" type="button" class="btn btn-danger">
                Cancelar
              </button>
            </div>
          </form>

          <div class="list">
            <div v-for="tx in transactions" :key="tx.transaction_id" class="list-item">
              <div>
                <strong>{{ tx.description }}</strong>
                <span class="category-badge">{{ tx.category.name }}</span>
                <small>{{ formatDate(tx.date) }}</small>
              </div>
              <div class="amount-actions">
                <span class="amount">{{ formatCurrency(tx.amount) }}</span>
                <button @click="editTransaction(tx)" class="btn btn-sm btn-primary">Editar</button>
                <button @click="deleteTransaction(tx.transaction_id)" class="btn btn-sm btn-danger">Excluir</button>
              </div>
            </div>
            <p v-if="!transactions.length" class="empty">Nenhuma transação cadastrada</p>
          </div>
        </div>

        <!-- Estatísticas -->
        <div class="card">
          <h2>Estatísticas</h2>
          <div class="stats-grid">
            <div class="stat-box">
              <h4>Total Gasto (Histórico)</h4>
              <p class="stat-value">{{ formatCurrency(budget.total_spent_ever) }}</p>
            </div>
          </div>

          <h3>Resumo Mensal</h3>
          <div class="monthly-list">
            <div v-for="item in monthlyStats" :key="item.month" class="monthly-item">
              <span>{{ item.month }}</span>
              <strong>{{ formatCurrency(item.total_expenses) }}</strong>
            </div>
            <p v-if="!monthlyStats.length" class="empty">Sem dados mensais</p>
          </div>

          <h3>Por Categoria</h3>
          <div class="category-stats">
            <div v-for="item in categoryStats" :key="item.category" class="category-stat-item">
              <div>
                <strong>{{ item.category }}</strong>
                <small>{{ item.transaction_count }} transações</small>
              </div>
              <div class="stat-amounts">
                <span>Total: {{ formatCurrency(item.total_amount) }}</span>
                <small>Média: {{ formatCurrency(item.average_amount) }}</small>
              </div>
            </div>
            <p v-if="!categoryStats.length" class="empty">Sem dados por categoria</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from './api'

export default {
  name: 'App',
  data() {
    return {
      categories: [],
      transactions: [],
      budget: { budget_id: 1, total_spent_ever: 0 },
      monthlyStats: [],
      categoryStats: [],
      categoryForm: { name: '' },
      transactionForm: { description: '', amount: '', category_id: '' },
      editingCategoryId: null,
      editingTransactionId: null
    }
  },
  mounted() {
    this.loadAll()
  },
  methods: {
    async loadAll() {
      await Promise.all([
        this.loadCategories(),
        this.loadTransactions(),
        this.loadStatistics()
      ])
    },
    async loadCategories() {
      try {
        const response = await api.getCategories()
        this.categories = response.data
      } catch (error) {
        console.error('Erro ao carregar categorias:', error)
      }
    },
    async loadTransactions() {
      try {
        const response = await api.getTransactions()
        this.transactions = response.data
      } catch (error) {
        console.error('Erro ao carregar transações:', error)
      }
    },
    async loadStatistics() {
      try {
        const [budgetRes, monthlyRes, categoryRes] = await Promise.all([
          api.getBudget(),
          api.getMonthlyStatistics(),
          api.getCategoryStatistics()
        ])
        this.budget = budgetRes.data
        this.monthlyStats = monthlyRes.data
        this.categoryStats = categoryRes.data
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error)
      }
    },
    async saveCategory() {
      try {
        if (this.editingCategoryId) {
          await api.updateCategory(this.editingCategoryId, this.categoryForm)
        } else {
          await api.createCategory(this.categoryForm)
        }
        this.categoryForm.name = ''
        this.editingCategoryId = null
        await this.loadCategories()
      } catch (error) {
        alert(error.response?.data?.detail || 'Erro ao salvar categoria')
      }
    },
    editCategory(category) {
      this.editingCategoryId = category.category_id
      this.categoryForm.name = category.name
    },
    async deleteCategory(id) {
      if (!confirm('Deseja realmente excluir?')) return
      try {
        await api.deleteCategory(id)
        await this.loadCategories()
      } catch (error) {
        alert(error.response?.data?.detail || 'Erro ao excluir categoria')
      }
    },
    cancelEditCategory() {
      this.categoryForm.name = ''
      this.editingCategoryId = null
    },
    async saveTransaction() {
      try {
        if (this.editingTransactionId) {
          await api.updateTransaction(this.editingTransactionId, this.transactionForm)
        } else {
          await api.createTransaction(this.transactionForm)
        }
        this.transactionForm = { description: '', amount: '', category_id: '' }
        this.editingTransactionId = null
        await this.loadAll()
      } catch (error) {
        alert(error.response?.data?.detail || 'Erro ao salvar transação')
      }
    },
    editTransaction(tx) {
      this.editingTransactionId = tx.transaction_id
      this.transactionForm.description = tx.description
      this.transactionForm.amount = tx.amount
      this.transactionForm.category_id = tx.category_id
    },
    async deleteTransaction(id) {
      if (!confirm('Deseja realmente excluir?')) return
      try {
        await api.deleteTransaction(id)
        await this.loadAll()
      } catch (error) {
        alert(error.response?.data?.detail || 'Erro ao excluir transação')
      }
    },
    cancelEditTransaction() {
      this.transactionForm = { description: '', amount: '', category_id: '' }
      this.editingTransactionId = null
    },
    formatCurrency(value) {
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      }).format(value)
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('pt-BR')
    }
  }
}
</script>

<style>
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

.btn-audit {
  background: #9b59b6;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.9rem;
  transition: background 0.3s;
}

.btn-audit:hover {
  background: #8e44ad;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.main-content {
  display: grid;
  gap: 1.5rem;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.card h3 {
  color: #34495e;
  margin: 1.5rem 0 1rem;
  font-size: 1.1rem;
}

.card h4 {
  color: #7f8c8d;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 0.5rem;
}

.form-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.form-row input,
.form-row select,
.form-group input {
  flex: 1;
  min-width: 150px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
  white-space: nowrap;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-success {
  background: #2ecc71;
  color: white;
}

.btn-success:hover {
  background: #27ae60;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background: #c0392b;
}

.btn-sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.9rem;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 4px;
  gap: 1rem;
}

.list-item > div {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.category-badge {
  background: #3498db;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.amount-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.amount {
  font-weight: bold;
  color: #e74c3c;
  min-width: 100px;
  text-align: right;
}

.empty {
  color: #95a5a6;
  text-align: center;
  padding: 1rem;
  font-style: italic;
}

.stats-grid {
  display: grid;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-box {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-top: 0.5rem;
}

.monthly-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.monthly-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.category-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.category-stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.stat-amounts {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.stat-amounts small {
  color: #7f8c8d;
}

small {
  font-size: 0.85rem;
  color: #7f8c8d;
}
</style>
