<template>
  <div class="categories">
    <div class="card">
      <h2>Gerenciar Categorias</h2>
      
      <form @submit.prevent="saveCategory" class="category-form">
        <div class="form-group">
          <label>Nome da Categoria</label>
          <input v-model="form.name" type="text" required placeholder="Ex: Alimentação">
        </div>
        <div class="form-group">
          <label>Descrição</label>
          <textarea v-model="form.description" placeholder="Descrição opcional"></textarea>
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
      <h3>Categorias Cadastradas</h3>
      <div v-if="loading" class="loading">Carregando...</div>
      <table v-else-if="categories.length">
        <thead>
          <tr>
            <th>Nome</th>
            <th>Descrição</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="category in categories" :key="category.id">
            <td>{{ category.name }}</td>
            <td>{{ category.description || '-' }}</td>
            <td>
              <button @click="editCategory(category)" class="btn btn-primary">Editar</button>
              <button @click="deleteCategory(category.id)" class="btn btn-danger">Excluir</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>Nenhuma categoria cadastrada.</p>
    </div>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'Categories',
  data() {
    return {
      categories: [],
      form: {
        name: '',
        description: ''
      },
      editingId: null,
      loading: false,
      error: null,
      success: null
    }
  },
  mounted() {
    this.loadCategories()
  },
  methods: {
    async loadCategories() {
      this.loading = true
      try {
        const response = await api.getCategories()
        this.categories = response.data
      } catch (error) {
        this.error = 'Erro ao carregar categorias'
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async saveCategory() {
      this.error = null
      this.success = null
      try {
        if (this.editingId) {
          await api.updateCategory(this.editingId, this.form)
          this.success = 'Categoria atualizada com sucesso!'
        } else {
          await api.createCategory(this.form)
          this.success = 'Categoria criada com sucesso!'
        }
        this.resetForm()
        this.loadCategories()
      } catch (error) {
        this.error = error.response?.data?.detail || 'Erro ao salvar categoria'
        console.error(error)
      }
    },
    editCategory(category) {
      this.editingId = category.id
      this.form.name = category.name
      this.form.description = category.description || ''
    },
    async deleteCategory(id) {
      if (!confirm('Deseja realmente excluir esta categoria?')) return
      
      try {
        await api.deleteCategory(id)
        this.success = 'Categoria excluída com sucesso!'
        this.loadCategories()
      } catch (error) {
        this.error = error.response?.data?.detail || 'Erro ao excluir categoria'
        console.error(error)
      }
    },
    cancelEdit() {
      this.resetForm()
    },
    resetForm() {
      this.form.name = ''
      this.form.description = ''
      this.editingId = null
    }
  }
}
</script>

<style scoped>
.category-form {
  margin-bottom: 1.5rem;
}

.category-form .btn {
  margin-right: 0.5rem;
}

table button {
  margin-right: 0.5rem;
  padding: 0.25rem 0.75rem;
  font-size: 0.9rem;
}
</style>
