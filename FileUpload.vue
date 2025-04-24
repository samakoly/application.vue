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
 
export default {
    name: 'FileUpload',
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
/* Styles pour le composant d'upload avec un thème professionnel élégant et moderne */
.upload-container {
  width: 100%;
  max-width: 1000px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08), 0 6px 12px rgba(211, 168, 252, 0.04);
  font-family: 'Inter', 'Roboto', sans-serif;
  color: #2d2d3a;
  overflow: hidden;
}

.upload-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 22px 28px;
  background: linear-gradient(135deg, rgba(211, 168, 252, 0.03), rgba(252, 199, 211, 0.05));
  border-bottom: 1px solid rgba(211, 168, 252, 0.1);
  position: relative;
}

.upload-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, rgb(211, 168, 252), #fcc7d3, rgb(255, 255, 158));
  opacity: 0.7;
}

.back-button, .settings-button {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: none;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 18px;
  cursor: pointer;
  color: #555;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.back-button:hover, .settings-button:hover {
  background: linear-gradient(135deg, rgba(211, 168, 252, 0.1), rgba(252, 199, 211, 0.1));
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(211, 168, 252, 0.15);
  color: rgb(211, 168, 252);
}

.header-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  color: #2d2d3a;
  background: linear-gradient(90deg, rgb(211, 168, 252), #fcc7d3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

.upload-content {
  padding: 36px;
}

.dropzone {
  border: 2px dashed rgba(211, 168, 252, 0.3);
  border-radius: 16px;
  padding: 50px 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s ease;
  position: relative;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(250, 250, 255, 0.9));
  overflow: hidden;
}

.dropzone::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(211, 168, 252, 0.03), rgba(252, 199, 211, 0.03), rgba(255, 255, 158, 0.03));
  z-index: -1;
}

.dropzone:hover {
  border-color: rgb(211, 168, 252);
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(211, 168, 252, 0.1);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(250, 250, 255, 0.95));
}

.drag-active {
  border-color: rgb(211, 168, 252);
  background: linear-gradient(135deg, rgba(211, 168, 252, 0.05), rgba(252, 199, 211, 0.05));
  box-shadow: 0 10px 25px rgba(211, 168, 252, 0.15), inset 0 0 30px rgba(211, 168, 252, 0.03);
}

.file-input {
  display: none;
}

.upload-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(211, 168, 252, 0.1), rgba(252, 199, 211, 0.1));
  box-shadow: 0 10px 20px rgba(211, 168, 252, 0.1);
}

.upload-icon .icon {
  font-size: 32px;
  background: linear-gradient(90deg, rgb(211, 168, 252), #fcc7d3);
  color:black;
}

.upload-text {
  font-size: 18px;
  margin: 0 0 12px 0;
  color: #444;
  font-weight: 500;
}

.highlight {
  background: linear-gradient(90deg, rgb(211, 168, 252), #fcc7d3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  position: relative;
  padding: 0 3px;
}

.highlight::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, rgb(211, 168, 252), #fcc7d3);
  opacity: 0.7;
  border-radius: 10px;
}

.upload-subtext {
  font-size: 14px;
  color: #888;
  margin: 10px 0 0 0;
}

.selected-files {
  margin-top: 36px;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.files-header {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 20px 0;
  color: #2d2d3a;
  display: flex;
  align-items: center;
}

.files-header::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 20px;
  background: linear-gradient(180deg, rgb(211, 168, 252), #fcc7d3);
  margin-right: 12px;
  border-radius: 10px;
}

.file-list {
  max-height: 350px;
  overflow-y: auto;
  border-radius: 14px;
  border: 1px solid rgba(211, 168, 252, 0.15);
  background-color: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
  scrollbar-width: thin;
  scrollbar-color: rgba(211, 168, 252, 0.3) rgba(211, 168, 252, 0.05);
}

.file-list::-webkit-scrollbar {
  width: 6px;
}

.file-list::-webkit-scrollbar-track {
  background: rgba(211, 168, 252, 0.05);
  border-radius: 10px;
}

.file-list::-webkit-scrollbar-thumb {
  background: rgba(211, 168, 252, 0.3);
  border-radius: 10px;
}

.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(211, 168, 252, 0.08);
  transition: all 0.3s ease;
}

.file-item:hover {
  background: linear-gradient(135deg, rgba(211, 168, 252, 0.03), rgba(252, 199, 211, 0.03));
  transform: translateX(3px);
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
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(211, 168, 252, 0.1), rgba(252, 199, 211, 0.1));
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 18px;
  color: rgb(211, 168, 252);
  box-shadow: 0 4px 10px rgba(211, 168, 252, 0.1);
}

.file-details {
  overflow: hidden;
}

.file-name {
  font-size: 15px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 500px;
  color: #2d2d3a;
  margin-bottom: 4px;
}

.file-size {
  font-size: 13px;
  color: #888;
  display: flex;
  align-items: center;
}

.file-size::before {
  content: '';
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: linear-gradient(90deg, rgb(211, 168, 252), #fcc7d3);
  margin-right: 6px;
  opacity: 0.7;
}

.remove-file {
  width: 30px;
  height: 30px;
  background: white;
  border: 1px solid rgba(252, 103, 103, 0.2);
  color: #fc6767;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(252, 103, 103, 0.05);
}

.remove-file:hover {
  background-color: rgba(252, 103, 103, 0.1);
  transform: scale(1.1);
  box-shadow: 0 4px 10px rgba(252, 103, 103, 0.15);
}

.upload-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
  gap: 16px;
}

.cancel-btn {
  padding: 14px 28px;
  background-color: white;
  border: 1px solid rgba(211, 168, 252, 0.15);
  color: #555;
  border-radius: 12px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.cancel-btn:hover {
  background-color: #f8f9ff;
  color: rgb(211, 168, 252);
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(211, 168, 252, 0.1);
}

.upload-btn {
  padding: 14px 32px;
  background: linear-gradient(135deg, rgb(211, 168, 252), #fcc7d3);
  border: none;
  color: white;
  border-radius: 12px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.3px;
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px rgba(211, 168, 252, 0.25);
  position: relative;
  overflow: hidden;
}

.upload-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    rgba(255, 255, 255, 0), 
    rgba(255, 255, 255, 0.2), 
    rgba(255, 255, 255, 0));
  transform: skewX(-25deg);
  transition: all 0.5s ease;
}

.upload-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 25px rgba(211, 168, 252, 0.35);
  background-image: linear-gradient(135deg, rgb(221, 178, 255), #ffd0dc);
}

.upload-btn:hover::before {
  left: 100%;
  transition: all 0.5s ease;
}

.upload-btn:active {
  transform: translateY(-1px);
  box-shadow: 0 8px 15px rgba(211, 168, 252, 0.25);
}

/* Animation pour interaction avec la zone de dépôt */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(211, 168, 252, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(211, 168, 252, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(211, 168, 252, 0);
  }
}

.drag-active .upload-icon {
  animation: pulse 1.5s infinite;
}
</style>