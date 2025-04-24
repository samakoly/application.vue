<template>
  <div class="upload-container">
    <div class="upload-header">
      <button class="back-button">
        <span>←</span>
      </button>
      <h2 class="header-title">Upload de fichiers</h2>
      <button class="settings-button">
        <span>⚙</span>
      </button>
    </div>

    <div class="upload-content">
      <div class="dropzone" @click="triggerFileInput" @dragover.prevent="onDragOver" @dragleave.prevent="onDragLeave" @drop.prevent="onDrop" :class="{ 'drag-active': isDragging }">
        <input type="file" ref="fileInput" @change="handleFileSelect" multiple class="file-input" />
        <div class="upload-icon">
          <span class="icon">⬆️</span>
        </div>
        <p class="upload-text">Déposez vos fichiers ici ou <span class="highlight">parcourir</span></p>
        <p class="upload-subtext">Support pour PDF, DOCX, XLSX, Images (limite: 10MB par fichier)</p>
      </div>

      <div class="selected-files" v-if="files.length > 0">
        <h3 class="files-header">Fichiers sélectionnés</h3>
        
        <div class="file-list">
          <div v-for="(file, index) in files" :key="index" class="file-item">
            <div class="file-info">
              <div class="file-icon">
                <span v-if="file.type.includes('pdf')">📄</span>
                <span v-else-if="file.type.includes('image')">🖼️</span>
                <span v-else-if="file.type.includes('spreadsheet') || file.type.includes('excel')">📊</span>
                <span v-else-if="file.type.includes('document') || file.type.includes('word')">📝</span>
                <span v-else>📁</span>
              </div>
              <div class="file-details">
                <div class="file-name">{{ file.name }}</div>
                <div class="file-size">{{ formatFileSize(file.size) }}</div>
              </div>
            </div>
            <button class="remove-file" @click="removeFile(index)">×</button>
          </div>
        </div>

        <div class="upload-actions">
          <button class="cancel-btn">Annuler</button>
          <button class="upload-btn">Uploader les fichiers</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
 name: 'FileUpload',
export default {
  data() {
    return {
      files: [],
      isDragging: false
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileSelect(event) {
      const newFiles = Array.from(event.target.files);
      this.addFiles(newFiles);
    },
    onDragOver(event) {
      this.isDragging = true;
    },
    onDragLeave(event) {
      this.isDragging = false;
    },
    onDrop(event) {
      this.isDragging = false;
      const newFiles = Array.from(event.dataTransfer.files);
      this.addFiles(newFiles);
    },
    addFiles(newFiles) {
      // Filtre pour limiter la taille des fichiers à 10MB
      const validFiles = newFiles.filter(file => file.size <= 10 * 1024 * 1024);
      
      if (validFiles.length < newFiles.length) {
        alert("Certains fichiers dépassent la limite de 10MB et ont été ignorés.");
      }
      
      this.files = [...this.files, ...validFiles];
    },
    removeFile(index) {
      this.files.splice(index, 1);
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
  }
}
</script>

<style scoped>
.upload-container {
  width: 100%;
  max-width: 1000px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  font-family: 'Inter', 'Roboto', sans-serif;
  color: #333;
}

.upload-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  border-bottom: 1px solid #eaeaea;
}

.back-button, .settings-button {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  border: 1px solid #eaeaea;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 18px;
  cursor: pointer;
  color: #555;
}

.back-button:hover, .settings-button:hover {
  background-color: rgba(211, 168, 252, 0.1);
}

.header-title {
  font-size: 22px;
  font-weight: 600;
  margin: 0;
  color: #333;
}

.upload-content {
  padding: 25px;
}

.dropzone {
  border: 2px dashed #d8d8d8;
  border-radius: 6px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  background-color: #f9f9f9;
}

.dropzone:hover {
  border-color: rgb(211, 168, 252);
  background-color: rgba(211, 168, 252, 0.05);
}

.drag-active {
  border-color: rgb(211, 168, 252);
  background-color: rgba(211, 168, 252, 0.1);
}

.file-input {
  display: none;
}

.upload-icon {
  font-size: 36px;
  margin-bottom: 15px;
}

.upload-text {
  font-size: 16px;
  margin: 0 0 8px 0;
  color: #444;
}

.highlight {
  color: rgb(211, 168, 252);
  font-weight: 500;
}

.upload-subtext {
  font-size: 14px;
  color: #777;
  margin: 5px 0 0 0;
}

.selected-files {
  margin-top: 24px;
}

.files-header {
  font-size: 18px;
  font-weight: 500;
  margin: 0 0 15px 0;
  color: #333;
}

.file-list {
  max-height: 300px;
  overflow-y: auto;
  border-radius: 6px;
  border: 1px solid #eaeaea;
}

.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #eaeaea;
}

.file-item:last-child {
  border-bottom: none;
}

.file-info {
  display: flex;
  align-items: center;
  overflow: hidden;
}

.file-icon {
  font-size: 20px;
  margin-right: 15px;
  min-width: 24px;
  text-align: center;
}

.file-details {
  overflow: hidden;
}

.file-name {
  font-size: 15px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 500px;
  color: #333;
}

.file-size {
  font-size: 13px;
  color: #777;
  margin-top: 3px;
}

.remove-file {
  background: none;
  border: none;
  color: #999;
  font-size: 18px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.remove-file:hover {
  background-color: rgba(252, 103, 103, 0.1);
  color: #fc6767;
}

.upload-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  gap: 15px;
}

.cancel-btn {
  padding: 10px 20px;
  background-color: #f1f3f5;
  border: 1px solid #ddd;
  color: #333;
  border-radius: 4px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s;
}

.cancel-btn:hover {
  background-color: #e9ecef;
}

.upload-btn {
  padding: 10px 20px;
  background: linear-gradient(to right, rgb(211, 168, 252), #fcc7d3);
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: 0 5px 15px rgba(211, 168, 252, 0.3);
}

.upload-btn:hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
}

.upload-btn:active {
  transform: translateY(0);
}
</style>