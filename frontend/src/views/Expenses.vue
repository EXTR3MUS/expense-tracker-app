<template>
  <div class="expenses">
    <div class="card">
      <h2>Gerenciar Despesas</h2>
      
      <form @submit.prevent="saveExpense" class="expense-form">
        <div class="form-group">
          <label>Descrição</label>
          <input v-model="form.description" type="text" required placeholder="Ex: Almoço no restaurante">
        </div>
        <div class="form-group">
          <label>Valor (R$)</label>
          <input v-model.number="form.amount" type="number" step="0.01" required placeholder="0.00">
        </div>
        <div class="form-group">
          <label>Categoria</label>
          <select v-model="form.category_id" required>
            <option value="">Selecione uma categoria</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label>Data</label>
          <input v-model="form.date" type="datetime-local">
        </div>
        <button type="submit" class="btn btn-primary">
          {{ editingId ? 'Atualizar' : 'Adicionar' }}
        </button>
        <button v-if="editingId" @click="cancelEdit" type="button" class="btn btn-danger">
          Cancelar
        </button>
      </form>

      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </div>

    <div class="card">
      <h3>Despesas Cadastradas</h3>
      <div v-if="loading" class="loading">Carregando...</div>
      <table v-else-if="expenses.length">
        <thead>
          <tr>
            <th>Descrição</th>
            <th>Valor</th>
            <th>Categoria</th>
            <th>Data</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="expense in expenses" :key="expense.id">
            <td>{{ expense.description }}</td>
            <td>{{ formatCurrency(expense.amount) }}</td>
            <td>{{ expense.category.name }}</td>
            <td>{{ formatDate(expense.date) }}</td>
            <td>
              <button @click="editExpense(expense)" class="btn btn-primary">Editar</button>
              <button @click="deleteExpense(expense.id)" class="btn btn-danger">Excluir</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>Nenhuma despesa cadastrada.</p>
    </div>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'Expenses',
  data() {
    return {
      expenses: [],
      categories: [],
      form: {
        description: '',
        amount: '',
        category_id: '',
        date: ''
      },
      editingId: null,
      loading: false,
      error: null,
      success: null
    }
  },
  mounted() {
    this.loadExpenses()
    this.loadCategories()
  },
  methods: {
    async loadExpenses() {
      this.loading = true
      try {
        const response = await api.getExpenses()
        this.expenses = response.data
      } catch (error) {
        this.error = 'Erro ao carregar despesas'
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async loadCategories() {
      try {
        const response = await api.getCategories()
        this.categories = response.data
      } catch (error) {
        console.error('Erro ao carregar categorias:', error)
      }
    },
    async saveExpense() {
      this.error = null
      this.success = null
      try {
        const data = { ...this.form }
        if (!data.date) {
          delete data.date
        }
        
        if (this.editingId) {
          await api.updateExpense(this.editingId, data)
          this.success = 'Despesa atualizada com sucesso!'
        } else {
          await api.createExpense(data)
          this.success = 'Despesa criada com sucesso!'
        }
        this.resetForm()
        this.loadExpenses()
      } catch (error) {
        this.error = error.response?.data?.detail || 'Erro ao salvar despesa'
        console.error(error)
      }
    },
    editExpense(expense) {
      this.editingId = expense.id
      this.form.description = expense.description
      this.form.amount = expense.amount
      this.form.category_id = expense.category_id
      this.form.date = expense.date ? new Date(expense.date).toISOString().slice(0, 16) : ''
    },
    async deleteExpense(id) {
      if (!confirm('Deseja realmente excluir esta despesa?')) return
      
      try {
        await api.deleteExpense(id)
        this.success = 'Despesa excluída com sucesso!'
        this.loadExpenses()
      } catch (error) {
        this.error = error.response?.data?.detail || 'Erro ao excluir despesa'
        console.error(error)
      }
    },
    cancelEdit() {
      this.resetForm()
    },
    resetForm() {
      this.form.description = ''
      this.form.amount = ''
      this.form.category_id = ''
      this.form.date = ''
      this.editingId = null
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

<style scoped>
.expense-form {
  margin-bottom: 1.5rem;
}

.expense-form .btn {
  margin-right: 0.5rem;
}

table button {
  margin-right: 0.5rem;
  padding: 0.25rem 0.75rem;
  font-size: 0.9rem;
}
</style>
